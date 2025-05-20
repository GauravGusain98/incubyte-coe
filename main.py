from fastapi import FastAPI
from coe.api.routes import router as api_router
from config import settings

app = FastAPI(title=settings.app_name)

app.include_router(api_router)