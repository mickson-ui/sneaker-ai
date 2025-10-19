import torch
from torch import nn
from torch.nn import functional as F
from torchvision import models

class SneakerModel:
    """
    Wrapper class for loading and running inference with the sneaker classification model.
    """

    def __init__(self, model_path: str, class_names: list[str]):
        """
        Load a ResNet18 model and apply the saved weights.

        Args:
            model_path (str): Path to the saved model weights (.pth).
            class_names (list[str]): All brand/model class names.
        """
        self.class_names = class_names
        num_classes = len(class_names)

        # Rebuild the exact mode architecture used in training
        self.model = models.resnet18(weights=None)
        in_features = self.model.fc.in_features
        self.model.fc = nn.Linear(in_features, num_classes)

        # Load the saved state disctionary (weights)
        state_dict = torch.load(model_path, map_location='cpu')

        # Handle both 'plain state_dict' and chechpoint dicts with 'state_dict' key
        if isinstance(state_dict, dict) and "state_dict" in state_dict:
            state_dict = state_dict["state_dict"]

        # Apply weights and set model to evaluation mode
        self.model.load_state_dict(state_dict, strict=False)
        self.model.eval()
    

    def predict(self, image_tensor):

        """
        Run forward inference on a single preprocessed image tensor

        Returns:
            list[dict]: Top-3 predictions with label and confidence.
        """
        with torch.no_grad():
            outputs = self.model(image_tensor)
            probs = F.softmax(outputs, dim=1)
            top_probs, top_classes = probs.topk(3, dim=1)

        # Build structured prediction list
        predictions = [
            {
                "label": self.class_names[cls.item()],
                "confidence": round(prob.item() * 100, 2)
            }
            for prob, cls in zip(top_probs[0], top_classes[0])
        ]
        return predictions