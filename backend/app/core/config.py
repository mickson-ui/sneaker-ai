from fastapi.middleware.cors import CORSMiddleware

def setup_cors(app):
    # Setup cross-origin resource sharing 

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # TODO: limit to frontend domain in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
