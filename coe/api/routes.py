from fastapi import APIRouter

router = APIRouter()

@router.get("/hello-world")
def index():
    return {"message": "Hello World from COE app"}