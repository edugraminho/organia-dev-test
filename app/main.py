from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.routes import review_route

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(review_route.router)


@app.get("/")
def get_health_check(request: Request):
    return {"message": "Health check successful"}
