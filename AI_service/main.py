from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf
import uvicorn

from controllers.traffic_sign import router as traffic_sign_router
from services.model_service import initialize_default_model

tf.config.set_visible_devices([], 'GPU')

app = FastAPI(
    title="Traffic Sign Recognition API",
    description="API for detecting and classifying traffic signs with multiple model options",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(traffic_sign_router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    """Khởi tạo model khi ứng dụng khởi động"""
    initialize_default_model()

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "Traffic Sign Recognition API",
        "docs": "/docs",
        "health": "/api/health"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
