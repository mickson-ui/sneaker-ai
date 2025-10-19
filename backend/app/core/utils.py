from PIL import Image
import io
from torchvision import transforms

def read_image_from_bytes(image_bytes: bytes) -> Image.Image:
    # Convert raw image bytes into a PIL Image object.
    # Return RGB image ready for preprocessing
    return Image.open(io.BytesIO(image_bytes)).convert("RGB") 

def get_transform():
    # Return the preprocessing transformtion pipeline

    return transforms.Compose([
        transforms.Resize((244, 244)),
        transforms.ToTensor(),
    ])