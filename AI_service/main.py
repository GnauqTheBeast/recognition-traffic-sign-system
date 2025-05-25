from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.traffic_sign import router as traffic_sign_router
from services.model_service import ModelService

class TrafficSignAPI:
    def __init__(self):
        self.app = FastAPI()
        self.model_service = ModelService()
        self.configure_middleware()
        self.include_routers()

    def configure_middleware(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def include_routers(self):
        self.app.include_router(traffic_sign_router, prefix="/api", tags=["traffic-sign"])

    def add_routes(self):
        @self.app.get("/")
        async def root():
            return {"message": "Traffic Sign Detection API"}


def create_app():
    api = TrafficSignAPI()
    api.add_routes()
    return api.app

if __name__ == "__main__":
    import uvicorn
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)
