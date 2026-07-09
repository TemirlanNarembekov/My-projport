import numpy as np
import supervision as sv
from insightface.app import FaceAnalysis
import cv2
import sys
import os
import torch
from baseline import MultiTaskResNet50
from dataset import val_transform
from PIL import Image
from collections import defaultdict

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
VIDEONAME = 'face.mp4'#'face.mp4'
video = cv2.VideoCapture(VIDEONAME)
video.set(cv2.CAP_PROP_POS_MSEC, 0)

if not video.isOpened():
    print('error')
    sys.exit()
   
w = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

VIDEORESNAME = 'inference'+VIDEONAME
videores = cv2.VideoWriter(VIDEORESNAME,cv2.VideoWriter_fourcc(*'mp4v'), fps=19, frameSize=(w, h))            



detector = FaceAnalysis(name = 'buffalo_l', allowed_modules=['detection'], providers =['CPUExecutionProvider'])#buffalo_l
detector.prepare(ctx_id=-1)
tracker = sv.ByteTrack(lost_track_buffer = 300)
box_annotator = sv.BoxAnnotator(color_lookup=sv.ColorLookup.TRACK)
label_annotator = sv.LabelAnnotator(color_lookup=sv.ColorLookup.TRACK)


net = MultiTaskResNet50()
ckpt = torch.load("best.pt", map_location=device)
net.load_state_dict(ckpt['model'])
net.eval()
net.to(device)



MARGIN_W = 0.1   # по ширине (лицо занимало ~36%, надо расширять сильнее) 0.9
MARGIN_H = 0.1   # по высоте (лицо занимало ~51%, расширять меньше) 0.4

genders = {0:'MALE', 1:'FEMALE'}
age_hist = defaultdict(list)
gender_hist = defaultdict(list)
frame_id = 0
INFER_EVERY = 1 #1



while True:
    ok,frame = video.read()
    if not ok or frame is None:
        break
    


    faces = detector.get(frame)
    bboxes = np.empty((0,4))
    scores = np.empty((0,))


    for face in faces:
        x1,y1,x2,y2 = face.bbox
        fw,fh = x2-x1,y2-y1
        nx1 = x1 - fw * MARGIN_W
        ny1 = y1 - fh * MARGIN_H
        nx2 = x2 + fw * MARGIN_W
        ny2 = y2 + fh * MARGIN_H
        bboxes = np.append(bboxes, [(nx1, ny1, nx2, ny2)], axis=0)
        scores = np.append(scores, [face.det_score])



    detections = sv.Detections(xyxy = bboxes, confidence=scores)
    detections = tracker.update_with_detections(detections)

    for i in range(len(detections)):
        tid = detections.tracker_id[i]
        bbox = detections.xyxy[i].astype(int)
        x1 = max(0, bbox[0])
        y1 = max(0, bbox[1])
        x2 = min(w, bbox[2])
        y2 = min(h, bbox[3])
        if frame_id % INFER_EVERY == 0:
            inf_frame = frame[y1:y2, x1:x2]
            inf_frame = cv2.cvtColor(inf_frame, cv2.COLOR_BGR2RGB)
            inf_frame = Image.fromarray(inf_frame)
            inf_frame = val_transform(inf_frame).unsqueeze(0).to(device)

            with torch.no_grad():
                gender_logit, age = net(inf_frame)
                female_prob = torch.sigmoid(gender_logit).item()
                pred_gender = 1 if female_prob > 0.5 else 0
                pred_age = age.item()

            age_hist[tid].append(pred_age)
            gender_hist[tid].append(pred_gender)

    
    current_tracks = [tid for tid in detections.tracker_id] if detections.tracker_id is not None else []
    
    labels = []
    for tid in current_tracks:
        if age_hist[tid]:
            avg_age = round(np.mean(age_hist[tid]))
            maj_gender = round(np.mean(gender_hist[tid]))   # >0.5 → чаще женщина
            labels.append(f"ID{tid} {genders[maj_gender]} {avg_age}")
        else:
            labels.append(f"ID{tid}")    

    
    frame = box_annotator.annotate(scene=frame,detections=detections)
    frame = label_annotator.annotate(scene=frame,detections=detections, labels=labels)
  
    cv2.imshow('video',frame)
    videores.write(frame)
    frame_id+=1
    
    
    
    if cv2.waitKey(1) & 0xFF == ord('q'):   # выход по 'q'
        break
    

video.release()
videores.release()
cv2.destroyAllWindows()


