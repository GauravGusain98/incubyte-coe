from fastapi import APIRouter

router = APIRouter(tags=["Generic"])

@router.get("/hello-world")
def hello():
    return {"message": "Hello World from COE app"}