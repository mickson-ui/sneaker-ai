from fastapi import FastAPI
from app.routers import predict
from app.core.config import setup_cors

def create_app() -> FastAPI:
    """
    Factory function to initialize and configure the FastAPI app.

    - Sets up CORS policy.
    - Includes routers (e.g., /predict).
    - Returns the application instance.
    """
    app = FastAPI(title="Sneaker AI API", version="1.0")
    setup_cors(app)
    app.include_router(predict.router)
    return app


# App instance (used by uvicorn)
app = create_app()