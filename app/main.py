from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import review_route

app = FastAPI(
    title="API de Análise de Sentimentos",
    description="API para análise automática de sentimentos em avaliações de clientes.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(review_route.router)


@app.get("/")
def get_health_check():
    """
    Health check endpoint to verify if the API is running properly.

    Returns:
        dict: A message confirming that the API is operational.
    """
    return {"message": "Health check successful"}
