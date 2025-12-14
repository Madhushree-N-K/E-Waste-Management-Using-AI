# backend/app/core/model_utils.py
import os
import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image

# ------------------------
# Paths
# ------------------------
BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..")
MODEL_PATH = os.path.join(BASE_DIR, "ewaste_model.pth")
TRAIN_FOLDER = os.path.join(BASE_DIR, "dataset", "modified-dataset", "train")

# ------------------------
# Device
# ------------------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ------------------------
# Image transforms (same as training)
# ------------------------
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        [0.485, 0.456, 0.406],
        [0.229, 0.224, 0.225]
    )
])

# ------------------------
# Class names (leave as-is for now)
# ------------------------
def get_class_names():
    return [
        "Battery",
        "Keyboard",
        "Mobile",
        "Mouse",
        "PCB",
        "Player",
        "Printer",
        "Television",
        "Washing Machine"
    ]

# ------------------------
# Load model safely
# ------------------------
def load_model():
    classes = get_class_names()
    num_classes = len(classes)

    model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
    model.fc = nn.Linear(model.fc.in_features, num_classes)

    if os.path.exists(MODEL_PATH):
        try:
            checkpoint = torch.load(MODEL_PATH, map_location=device)

            # Handle dict-based save
            if isinstance(checkpoint, dict) and "model_state" in checkpoint:
                model.load_state_dict(checkpoint["model_state"])
            else:
                model.load_state_dict(checkpoint)

            print("Model loaded successfully")

        except Exception as e:
            print("Error loading model:", e)
    else:
        print("Warning: ewaste_model.pth not found")

    model.to(device)
    model.eval()
    return model, classes

# ------------------------
# Load at import
# ------------------------
MODEL, CLASS_NAMES = load_model()

# ------------------------
# Prediction function
# ------------------------
def classify_image_pil(pil_image: Image.Image):
    """
    Input : PIL Image (RGB)
    Output: (label, confidence, probability_dict)
    """
    img = pil_image.convert("RGB")
    x = transform(img).unsqueeze(0).to(device)

    with torch.no_grad():
        logits = MODEL(x)
        probs = torch.softmax(logits, dim=1).cpu().numpy()[0]

    top_idx = int(probs.argmax())
    label = CLASS_NAMES[top_idx] if top_idx < len(CLASS_NAMES) else "Unknown"
    confidence = float(probs[top_idx])

    probs_dict = {
        CLASS_NAMES[i]: float(probs[i])
        for i in range(len(CLASS_NAMES))
    }

    return label, confidence, probs_dict
