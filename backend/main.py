from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from model.delay_prediction import router as delay_router
from model.fare_prediction import router as fare_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(fare_router, prefix="/api")
app.include_router(delay_router, prefix="/api")
