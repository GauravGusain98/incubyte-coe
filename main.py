from fastapi import FastAPI
from coe.api.routes import router as api_router
from coe.api.user.routes import router as user_router
from coe.api.task.routes import router as task_router
from config import settings

app = FastAPI(title=settings.app_name)

app.include_router(api_router)
app.include_router(user_router)
app.include_router(task_router)