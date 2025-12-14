import os
import torch
import torch.nn as nn
from torch.optim import Adam
from torchvision import datasets, models, transforms
from torch.utils.data import DataLoader
from tqdm import tqdm

# -------------------------
# Paths (matches FastAPI)
# -------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "dataset", "modified-dataset", "train")
MODEL_PATH = os.path.join(BASE_DIR, "ewaste_model.pth")

# -------------------------
# CLASS NAMES (STRICT ALPHABETICAL)
# Must match folder names EXACTLY
# -------------------------
CLASS_NAMES = sorted([
    "Battery",
    "Keyboard",
    "Mobile",
    "Mouse",
    "PCB",
    "Player",
    "Printer",
    "Television",
    "Washing Machine"
])

print("\nTRAINING CLASS ORDER:")
for i, c in enumerate(CLASS_NAMES):
    print(f"{i} => {c}")

# -------------------------
# Device
# -------------------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("\nTraining on device:", device)

# -------------------------
# Transforms (MUST MATCH PREDICTION)
# -------------------------
train_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

# -------------------------
# Dataset
# -------------------------
train_dataset = datasets.ImageFolder(DATA_DIR, transform=train_transforms)

# Override auto-scan with FIXED class order
train_dataset.classes = CLASS_NAMES
train_dataset.class_to_idx = {c: i for i, c in enumerate(CLASS_NAMES)}

# -------------------------
# DataLoader
# -------------------------
train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)

# -------------------------
# Model (ResNet18)
# -------------------------
model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
model.fc = nn.Linear(model.fc.in_features, len(CLASS_NAMES))
model.to(device)

criterion = nn.CrossEntropyLoss()
optimizer = Adam(model.parameters(), lr=0.0003)

# -------------------------
# Training
# -------------------------
EPOCHS = 10
print("\nTraining Started...\n")

for epoch in range(EPOCHS):
    model.train()
    total_loss = 0

    loop = tqdm(train_loader, desc=f"Epoch {epoch+1}/{EPOCHS}")

    for images, labels in loop:
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        loop.set_postfix(loss=loss.item())

    print(f"Epoch {epoch+1} Completed | Avg Loss: {total_loss/len(train_loader):.4f}")

# -------------------------
# Save Model
# -------------------------
torch.save({
    "model_state": model.state_dict(),
    "class_names": CLASS_NAMES
}, MODEL_PATH)

print(f"\nModel saved successfully → {MODEL_PATH}\n")
