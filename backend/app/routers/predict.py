from fastapi import APIRouter, UploadFile, File
from app.models.sneaker_model import SneakerModel
from app.schemas.prediction import PredictionResponse
from app.core.utils import read_image_from_bytes, get_transform

router = APIRouter(prefix="/predict", tags=["Prediction"])

# Example labels – replace these with the actual ones from your training dataset
CLASS_NAMES = ['Adidas', 'Alexander', 'Amiri', 'Asics', 'Autry', 'BAPE', 'Balenciaga', 'Birkenstock', 'Camper', 'Clarks', 'Converse', 'Crocs', 'Diadora', 'Dr.', 'Ewing', 'Hoka', 'Jordan', 'KangaROOS', 'Karhu', 'Keen', 'Lacoste', 'Lanvin', 'Le', 'Mizuno', 'Moon', 'New', 'Nike', 'ON', 'Off-White', 'Onitsuka', 'Puma', 'Reebok', 'Salomon', 'Saucony', 'Suicoke', 'Timberland', 'Vans', 'Veja', 'adidas', 'alexander']

# Initialize model and transformation pipeline once at startup
model = SneakerModel(model_path="best_sneaker_model.pth", class_names=CLASS_NAMES)
transform = get_transform()


@router.post("/", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...)):
    """
    Predict sneaker brand/model from an uploaded image.

    Workflow:
    1. Read the uploaded image bytes.
    2. Preprocess into a normalized tensor.
    3. Run inference with the trained model.
    4. Return top-3 predictions with confidence scores.

    Args:
        file (UploadFile): Image file (JPG/PNG).

    Returns:
        PredictionResponse: JSON response with predictions.
    """
    image_bytes = await file.read()
    image = read_image_from_bytes(image_bytes)
    input_tensor = transform(image).unsqueeze(0)

    predictions = model.predict(input_tensor)
    return {"predictions": predictions}