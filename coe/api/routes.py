from fastapi import APIRouter

router = APIRouter(tags=["Generic"])

@router.get("/hello-world")
def index():
    return {"message": "Hello World from COE app"}