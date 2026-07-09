import torch
import torch.nn as nn
from torchvision.models import resnet50, ResNet50_Weights

class MultiTaskResNet50(nn.Module):
    def __init__(self):
        super().__init__()

        # Предобученная ResNet-50
        self.backbone = resnet50(weights=ResNet50_Weights.DEFAULT)

        in_features = self.backbone.fc.in_features

        # Убираем последний слой
        self.backbone.fc = nn.Identity()

        # Голова для определения пола (binary classification)
        self.gender_head = nn.Sequential(
            nn.Linear(in_features, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, 1)
        )

        # Голова для определения возраста (regression)
        self.age_head = nn.Sequential(
            nn.Linear(in_features, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, 1)
        )

    def forward(self, x):
        features = self.backbone(x)

        gender = self.gender_head(features)
        age = self.age_head(features)

        return gender, age