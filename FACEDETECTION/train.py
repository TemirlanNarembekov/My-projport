import os
import sys
import time
import argparse
import random

import numpy as np
import pandas as pd

import torch
import torch.nn as nn
from torch.optim import AdamW
from torch.optim.lr_scheduler import ReduceLROnPlateau
from tqdm import tqdm

from baseline import MultiTaskResNet50
from dataset import TRAIN_DATA, VAL_DATA, TEST_DATA

parser = argparse.ArgumentParser(description="Train MultiTaskResNet50")
parser.add_argument("--epochs", type=int, default=50, help="Number of epochs")
parser.add_argument("--patience", type=int, default=7, help="Early stopping patience")
parser.add_argument("--save_every", type=int, default=5, help="Save checkpoint every N epochs")
parser.add_argument("--lr", type=float, default=3e-4, help="Learning rate")
parser.add_argument("--weight_decay", type=float, default=1e-4, help="Weight decay")
parser.add_argument("--age_loss_weight", type=float, default=0.05,
                     help="Weight applied to the age (regression) loss so it does not "
                          "dominate the gender (classification) loss")
parser.add_argument("--grad_clip", type=float, default=1.0, help="Max gradient norm (0 to disable)")
parser.add_argument("--checkpoint_dir", type=str, default="checkpoints", help="Directory for checkpoints")
parser.add_argument("--resume", type=str, default=None, help="Path to a checkpoint to resume from")
parser.add_argument("--seed", type=int, default=42, help="Random seed")
parser.add_argument("--no_amp", action="store_true", help="Disable mixed precision (AMP)")
args = parser.parse_args()


def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


set_seed(args.seed)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
use_amp = (device.type == "cuda") and (not args.no_amp)

torch.backends.cudnn.benchmark = True

print(f"Device: {device}")
if device.type == "cuda":
    gpu_name = torch.cuda.get_device_name(0)
    total_mem = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)
    print(f"GPU: {gpu_name} ({total_mem:.1f} GB)")
print(f"Mixed precision (AMP): {'on' if use_amp else 'off'}")

train_len = len(TRAIN_DATA)
val_len = len(VAL_DATA)
print(f"Train batches: {train_len}, Val batches: {val_len}")

if train_len == 0 or val_len == 0:
    print("ERROR: Empty dataset. Check dataset.py")
    sys.exit(1)

model = MultiTaskResNet50().to(device)

if use_amp:
    model = model.to(memory_format=torch.channels_last)

criterion_gender = nn.BCEWithLogitsLoss()
criterion_age = nn.SmoothL1Loss()

optimizer = AdamW(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)
scheduler = ReduceLROnPlateau(optimizer, mode="min", factor=0.5, patience=3)
scaler = torch.cuda.amp.GradScaler(enabled=use_amp)

os.makedirs(args.checkpoint_dir, exist_ok=True)

start_epoch = 1
best_loss = float("inf")
epochs_without_improve = 0
history = []

# ------------------------------------------------------------
# Resume from checkpoint (weights + optimizer + scheduler + scaler state)
# ------------------------------------------------------------
if args.resume is not None:
    if not os.path.isfile(args.resume):
        print(f"ERROR: checkpoint '{args.resume}' not found.")
        sys.exit(1)
    ckpt = torch.load(args.resume, map_location=device)
    model.load_state_dict(ckpt["model"])
    if "optimizer" in ckpt:
        optimizer.load_state_dict(ckpt["optimizer"])
    if "scheduler" in ckpt:
        scheduler.load_state_dict(ckpt["scheduler"])
    if "scaler" in ckpt and use_amp:
        scaler.load_state_dict(ckpt["scaler"])
    start_epoch = ckpt.get("epoch", 0) + 1
    best_loss = ckpt.get("val_loss", best_loss)
    print(f"Resumed from '{args.resume}' at epoch {start_epoch} (best_loss={best_loss:.4f})")


def to_device(images, gender, age):
    memory_format = torch.channels_last if use_amp else torch.contiguous_format
    images = images.to(device, non_blocking=True, memory_format=memory_format)
    gender = gender.to(device, non_blocking=True).unsqueeze(1)
    age = age.to(device, non_blocking=True).unsqueeze(1)
    return images, gender, age


def train_epoch():
    model.train()
    total_loss = 0.0
    batches = 0

    pbar = tqdm(TRAIN_DATA, desc="Training", leave=False, dynamic_ncols=True)
    for images, gender, age in pbar:
        images, gender, age = to_device(images, gender, age)

        optimizer.zero_grad(set_to_none=True)

        with torch.autocast(device_type=device.type, dtype=torch.float16, enabled=use_amp):
            pred_gender, pred_age = model(images)
            gender_loss = criterion_gender(pred_gender, gender)
            age_loss = criterion_age(pred_age, age)
            loss = gender_loss + args.age_loss_weight * age_loss

        scaler.scale(loss).backward()

        if args.grad_clip and args.grad_clip > 0:
            scaler.unscale_(optimizer)
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=args.grad_clip)

        scaler.step(optimizer)
        scaler.update()

        total_loss += loss.item()
        batches += 1

        pbar.set_postfix({
            "loss": f"{loss.item():.4f}",
            "gender": f"{gender_loss.item():.4f}",
            "age": f"{age_loss.item():.4f}",
        })

    return total_loss / batches if batches > 0 else float("inf")


@torch.no_grad()
def evaluate(loader, desc="Validating"):
    model.eval()

    total_loss = 0.0
    correct_gender = 0
    total_gender = 0
    age_error = 0.0
    batches = 0

    pbar = tqdm(loader, desc=desc, leave=False, dynamic_ncols=True)
    for images, gender, age in pbar:
        images, gender, age = to_device(images, gender, age)

        with torch.autocast(device_type=device.type, dtype=torch.float16, enabled=use_amp):
            pred_gender, pred_age = model(images)
            gender_loss = criterion_gender(pred_gender, gender)
            age_loss = criterion_age(pred_age, age)
            loss = gender_loss + args.age_loss_weight * age_loss

        total_loss += loss.item()
        batches += 1

        pred = (torch.sigmoid(pred_gender) >= 0.5).float()
        correct_gender += (pred == gender).sum().item()
        total_gender += gender.numel()

        age_error += torch.abs(pred_age - age).sum().item()

    if batches == 0:
        return float("inf"), 0.0, float("inf")

    avg_loss = total_loss / batches
    gender_acc = correct_gender / total_gender if total_gender > 0 else 0.0
    age_mae = age_error / total_gender if total_gender > 0 else float("inf")

    return avg_loss, gender_acc, age_mae


def save_checkpoint(path, epoch, val_loss):
    torch.save({
        "epoch": epoch,
        "model": model.state_dict(),
        "optimizer": optimizer.state_dict(),
        "scheduler": scheduler.state_dict(),
        "scaler": scaler.state_dict(),
        "val_loss": val_loss,
    }, path)


def format_seconds(seconds):
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def gpu_mem_str():
    if device.type != "cuda":
        return "n/a"
    allocated = torch.cuda.memory_allocated() / (1024 ** 3)
    reserved = torch.cuda.memory_reserved() / (1024 ** 3)
    return f"{allocated:.1f}/{reserved:.1f} GB"


# ============================================================
# Main loop
# ============================================================

header = (
    f"{'Epoch':<7}{'Train':<10}{'Val':<10}{'GenderAcc':<12}"
    f"{'AgeMAE':<9}{'LR':<11}{'Time':<10}{'ETA':<10}{'GPU mem':<12}"
)
print(header)
print("-" * len(header))

training_start = time.time()

for epoch in range(start_epoch, args.epochs + 1):
    epoch_start = time.time()

    train_loss = train_epoch()
    val_loss, gender_acc, age_mae = evaluate(VAL_DATA, desc="Validating")

    if not torch.isfinite(torch.tensor(val_loss)):
        print("Validation loss is inf or NaN. Stopping.")
        break

    scheduler.step(val_loss)
    lr = optimizer.param_groups[0]["lr"]

    epoch_time = time.time() - epoch_start
    remaining_epochs = args.epochs - epoch
    eta = epoch_time * remaining_epochs

    print(
        f"{epoch:<7}"
        f"{train_loss:<10.4f}"
        f"{val_loss:<10.4f}"
        f"{gender_acc:<12.4f}"
        f"{age_mae:<9.2f}"
        f"{lr:<11.6f}"
        f"{format_seconds(epoch_time):<10}"
        f"{format_seconds(eta):<10}"
        f"{gpu_mem_str():<12}"
    )

    # Сохранение last
    save_checkpoint(os.path.join(args.checkpoint_dir, "last.pt"), epoch, val_loss)

    # Сохранение best
    if val_loss < best_loss:
        best_loss = val_loss
        epochs_without_improve = 0
        save_checkpoint(os.path.join(args.checkpoint_dir, "best.pt"), epoch, val_loss)
        print("   ✓ Best model updated")
    else:
        epochs_without_improve += 1

    # Сохранение чекпоинта каждые save_every эпох
    if epoch % args.save_every == 0:
        save_checkpoint(os.path.join(args.checkpoint_dir, f"epoch_{epoch}.pt"), epoch, val_loss)

    # История
    history.append({
        "epoch": epoch,
        "train_loss": train_loss,
        "val_loss": val_loss,
        "gender_accuracy": gender_acc,
        "age_mae": age_mae,
        "lr": lr,
        "epoch_time_sec": epoch_time,
    })
    pd.DataFrame(history).to_csv("history.csv", index=False)

    if device.type == "cuda":
        torch.cuda.empty_cache()

    # Early stopping
    if epochs_without_improve >= args.patience:
        print(f"\nEarly stopping triggered after {epoch} epochs.")
        break

total_time = time.time() - training_start
print("=" * len(header))
print(f"Training finished in {format_seconds(total_time)}.")

# ------------------------------------------------------------
# Final evaluation
# ------------------------------------------------------------
best_ckpt_path = os.path.join(args.checkpoint_dir, "best.pt")
if os.path.isfile(best_ckpt_path):
    print("\nLoading best checkpoint for test evaluation...")
    ckpt = torch.load(best_ckpt_path, map_location=device)
    model.load_state_dict(ckpt["model"])

test_loss, test_gender_acc, test_age_mae = evaluate(TEST_DATA, desc="Testing")
print("=" * len(header))
print(f"Test results — loss: {test_loss:.4f} | gender_acc: {test_gender_acc:.4f} | age_mae: {test_age_mae:.2f}")
