import pandas as pd
from sklearn .model_selection import train_test_split
import torch
import torchvision
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms.v2 as tfs
import torch.nn as nn
from PIL import Image
from torchvision.datasets import ImageFolder

import matplotlib.pyplot as plt


data = pd.read_csv(filepath_or_buffer='data.csv')
data['age_group'] = data['age'].apply(lambda x: '1-2' if x<=2 else '3-20' if 3<=x<=20 else '20-40' if 20<x<=40 else '40-60' if 40<x<=60 else '60-80' if 60<x<=80 else '80+')
data['strat_key'] = data['gender'].astype(str)+'_'+data['age_group']

train_val, test_data = train_test_split(data, stratify= data['strat_key'], test_size=0.15, train_size=0.85, random_state=42, shuffle=True)
train_data, val_data = train_test_split(train_val, stratify= train_val['strat_key'], test_size=0.176, random_state=42, shuffle=True)


IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD  = [0.229, 0.224, 0.225]


    

train_transform = tfs.Compose([
                         tfs.ToImage(),
                         tfs.Resize((224,224)),
                         tfs.RandomHorizontalFlip(p=0.5),
                         tfs.RandomRotation(degrees = 15),
                         tfs.ColorJitter(brightness=0.2, contrast = 0.2),
                         tfs.ToDtype(torch.float32, scale=True),
                         tfs.Normalize(mean = IMAGENET_MEAN, std=IMAGENET_STD)
                        ])

val_transform = tfs.Compose([
    tfs.ToImage(),
    tfs.Resize((224, 224)),
    tfs.ToDtype(torch.float32, scale=True),
    tfs.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
])



class UTKFaceDataset(Dataset):
    def __init__(self, df, transform = None):
        self.transform = transform
        self.df = df.reset_index(drop=True)


    def __len__(self):
        return len(self.df)
    
    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        img = Image.open(row['img_path']).convert('RGB')
        if self.transform:
            img = self.transform(img)
        gender = torch.tensor(row['gender'],dtype=torch.float32)
        age = torch.tensor(row['age'], dtype = torch.float32)
        return img, gender, age
    

d_train = UTKFaceDataset(df = train_data, transform=train_transform)
d_val = UTKFaceDataset(df = val_data, transform=val_transform)
d_test = UTKFaceDataset(df = test_data, transform=val_transform)

TRAIN_DATA = DataLoader(d_train, batch_size=64, shuffle=True)# указать num_worker
VAL_DATA= DataLoader(d_val, batch_size=64, shuffle=False)
TEST_DATA= DataLoader(d_test, batch_size=64, shuffle=False)

