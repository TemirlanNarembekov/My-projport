import argparse
import sys

import torch
import torchvision.transforms.v2 as tfs
from PIL import Image

from baseline import MultiTaskResNet50

IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]

inference_transform = tfs.Compose([
    tfs.ToImage(),
    tfs.Resize((224, 224)),
    tfs.ToDtype(torch.float32, scale=True),
    tfs.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
])

def parse_args():
    parser = argparse.ArgumentParser(description="Inference: predict gender and age from an image")
    parser.add_argument("--checkpoint", type=str, required=True, help="Path to a .pt checkpoint (e.g. best.pt)")
    parser.add_argument("--image", type=str, required=True, help="Path to an input image")
    return parser.parse_args()


def load_model(checkpoint_path, device):
    model = MultiTaskResNet50().to(device)
    ckpt = torch.load(checkpoint_path, map_location=device)
    state_dict = ckpt["model"] if "model" in ckpt else ckpt
    model.load_state_dict(state_dict)
    model.eval()
    return model


def predict(model, image_path, device):
    img = Image.open(image_path).convert("RGB")
    tensor = inference_transform(img).unsqueeze(0).to(device)

    with torch.no_grad():
        pred_gender, pred_age = model(tensor)
        gender_prob = torch.sigmoid(pred_gender).item()
        age = pred_age.item()

    gender_label = "female" if gender_prob >= 0.5 else "male"
    confidence = gender_prob if gender_label == "female" else 1 - gender_prob

    return gender_label, confidence, age


def main():
    args = parse_args()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    try:
        model = load_model(args.checkpoint, device)
    except FileNotFoundError:
        print(f"ERROR: чекпоинт '{args.checkpoint}' не найден.")
        sys.exit(1)

    try:
        gender_label, confidence, age = predict(model, args.image, device)
    except FileNotFoundError:
        print(f"ERROR: изображение '{args.image}' не найдено.")
        sys.exit(1)

    print("=" * 40)
    print(f"Image:      {args.image}")
    print(f"Checkpoint: {args.checkpoint}")
    print("-" * 40)
    print(f"Gender: {gender_label} (confidence: {confidence:.2%})")
    print(f"Age:    {age:.1f} years")
    print("=" * 40)


if __name__ == "__main__":
    main()