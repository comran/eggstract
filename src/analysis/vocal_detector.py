import os

import barbar
import librosa
import librosa.display
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision.models import resnet34
from tqdm.notebook import tqdm

from src.util.constants import DATA_ROOT


def spec_to_image(spec, eps=1e-6):
    mean = spec.mean()
    std = spec.std()
    spec_norm = (spec - mean) / (std + eps)
    spec_min, spec_max = spec_norm.min(), spec_norm.max()
    spec_scaled = 255 * (spec_norm - spec_min) / (spec_max - spec_min)
    spec_scaled = spec_scaled.astype(np.uint8)
    return spec_scaled


def get_melspectrogram_db(
    file_path, sr=None, n_fft=2048, hop_length=512, n_mels=128, fmin=20, fmax=8300, top_db=80
):
    wav, sr = librosa.load(file_path, sr=sr)
    if wav.shape[0] < 5 * sr:
        wav = np.pad(wav, int(np.ceil((5 * sr - wav.shape[0]) / 2)), mode="reflect")
    else:
        wav = wav[: 5 * sr]
    spec = librosa.feature.melspectrogram(
        wav, sr=sr, n_fft=n_fft, hop_length=hop_length, n_mels=n_mels, fmin=fmin, fmax=fmax
    )
    spec_db = librosa.power_to_db(spec, top_db=top_db)
    return spec_db


class VocalDetectorData(Dataset):
    def __init__(self, base, df, in_col, out_col):
        self.df = df
        self.data = []
        self.labels = []
        self.c2i = {}
        self.i2c = {}
        self.categories = sorted(df[out_col].unique())
        for i, category in enumerate(self.categories):
            self.c2i[category] = i
            self.i2c[i] = category
        for ind in tqdm(range(len(df))):
            row = df.iloc[ind]
            file_path = os.path.join(base, row[in_col])
            self.data.append(spec_to_image(get_melspectrogram_db(file_path))[np.newaxis, ...])
            self.labels.append(self.c2i[row["category"]])

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx], self.labels[idx]


class VocalDetectorModel(nn.Module):
    def __init__(self, input_shape, batch_size=16, num_cats=50):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, stride=1, padding=1)
        self.bn1 = nn.BatchNorm2d(32)
        self.conv2 = nn.Conv2d(32, 32, kernel_size=3, stride=1, padding=1)
        self.bn2 = nn.BatchNorm2d(32)
        self.conv3 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
        self.bn3 = nn.BatchNorm2d(64)
        self.conv4 = nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1)
        self.bn4 = nn.BatchNorm2d(64)
        self.conv5 = nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1)
        self.bn5 = nn.BatchNorm2d(128)
        self.conv6 = nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1)
        self.bn6 = nn.BatchNorm2d(128)
        self.conv7 = nn.Conv2d(128, 256, kernel_size=3, stride=1, padding=1)
        self.bn7 = nn.BatchNorm2d(256)
        self.conv8 = nn.Conv2d(256, 256, kernel_size=3, stride=1, padding=1)
        self.bn8 = nn.BatchNorm2d(256)
        self.dense1 = nn.Linear(
            256 * (((input_shape[1] // 2) // 2) // 2) * (((input_shape[2] // 2) // 2) // 2), 500
        )
        self.dropout = nn.Dropout(0.5)
        self.dense2 = nn.Linear(500, num_cats)

    def forward(self, x):
        x = self.conv1(x)
        x = F.relu(self.bn1(x))
        x = self.conv2(x)
        x = F.relu(self.bn2(x))
        x = F.max_pool2d(x, kernel_size=2)
        x = self.conv3(x)
        x = F.relu(self.bn3(x))
        x = self.conv4(x)
        x = F.relu(self.bn4(x))
        x = F.max_pool2d(x, kernel_size=2)
        x = self.conv5(x)
        x = F.relu(self.bn5(x))
        x = self.conv6(x)
        x = F.relu(self.bn6(x))
        x = F.max_pool2d(x, kernel_size=2)
        x = self.conv7(x)
        x = F.relu(self.bn7(x))
        x = self.conv8(x)
        x = F.relu(self.bn8(x))
        x = x.view(x.size(0), -1)
        x = F.relu(self.dense1(x))
        x = self.dropout(x)
        x = self.dense2(x)

        return x


VOCAL_DETECTOR_LEARNING_RATE = 2e-4
VOCAL_DETECTOR_EPOCHS = 50


class VocalDetector:
    def __init__(self):
        if torch.cuda.is_available():
            self.device = torch.device("cuda:0")
        else:
            self.device = torch.device("cpu")

        self.model = VocalDetectorModel(input_shape=(1, 128, 431), batch_size=16, num_cats=50).to(
            self.device
        )

        self.resnet_model = resnet34(pretrained=True)
        self.resnet_model.fc = nn.Linear(512, 50)
        self.resnet_model.conv1 = nn.Conv2d(
            1, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False
        )
        self.resnet_model = self.resnet_model.to(self.device)

        self.df = pd.read_csv(f"{DATA_ROOT}/datasets/ESC-50-master/meta/esc50.csv")
        self.train_folds = self.df[self.df["fold"] != 5]
        self.valid_folds = self.df[self.df["fold"] == 5]

    def train(self):
        print("Train start")
        train_losses = []
        valid_losses = []

        print("Loading train data")
        train_data = VocalDetectorData(
            f"{DATA_ROOT}/datasets/ESC-50-master/audio", self.train_folds, "filename", "category"
        )

        print("Loading validation data")
        valid_data = VocalDetectorData(
            f"{DATA_ROOT}/datasets/ESC-50-master/audio", self.valid_folds, "filename", "category"
        )

        train_loader = DataLoader(train_data, batch_size=16, shuffle=True)
        valid_loader = DataLoader(valid_data, batch_size=16, shuffle=True)
        loss_fn = nn.CrossEntropyLoss()
        model = self.resnet_model

        optimizer = optim.Adam(self.resnet_model.parameters(), lr=VOCAL_DETECTOR_LEARNING_RATE)

        print("Starting training")
        for epoch in tqdm(range(1, VOCAL_DETECTOR_EPOCHS + 1)):
            print(f"Epoch {epoch}")
            model.train()
            batch_losses = []
            optimizer = self.lr_decay(optimizer, epoch)

            for i, data in enumerate(barbar.Bar(train_loader)):
                x, y = data
                optimizer.zero_grad()
                x = x.to(self.device, dtype=torch.float32)
                y = y.to(self.device, dtype=torch.long)
                y_hat = model(x)
                loss = loss_fn(y_hat, y)
                loss.backward()
                batch_losses.append(loss.item())
                optimizer.step()

            train_losses.append(batch_losses)
            print(f"Epoch - {epoch} Train-Loss : {np.mean(train_losses[-1])}")
            model.eval()
            batch_losses = []
            trace_y = []
            trace_yhat = []

            for i, data in enumerate(barbar.Bar(valid_loader)):
                x, y = data
                x = x.to(self.device, dtype=torch.float32)
                y = y.to(self.device, dtype=torch.long)
                y_hat = model(x)
                loss = loss_fn(y_hat, y)
                trace_y.append(y.cpu().detach().numpy())
                trace_yhat.append(y_hat.cpu().detach().numpy())
                batch_losses.append(loss.item())

            valid_losses.append(batch_losses)
            trace_y = np.concatenate(trace_y)
            trace_yhat_np = np.concatenate(trace_yhat)
            accuracy = np.mean(trace_yhat_np.argmax(axis=1) == trace_y)

            if (epoch - 1) % 5 == 0 or epoch == VOCAL_DETECTOR_EPOCHS:
                print("Saving a checkpoint of the model")
                with open(f"{DATA_ROOT}/trained/resnet.pth", "wb") as f:
                    torch.save(model, f)

            print(
                f"Epoch - {epoch} Valid-Loss : {np.mean(valid_losses[-1])} "
                f"Valid-Accuracy : {accuracy}"
            )

    def lr_decay(self, optimizer, epoch):
        if epoch % 10 == 0:
            new_lr = VOCAL_DETECTOR_LEARNING_RATE / (10 ** (epoch // 10))
            optimizer = self.setlr(optimizer, new_lr)
            print(f"Changed learning rate to {new_lr}")

        return optimizer

    def setlr(self, optimizer, lr):
        for param_group in optimizer.param_groups:
            param_group["lr"] = lr
        return optimizer
