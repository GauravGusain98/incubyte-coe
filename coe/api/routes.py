from fastapi import APIRouter

router = APIRouter(tags=["Generic"])

@router.get("/hello-world", openapi_extra={"is_public": True})
def hello():
    return {"message": "Hello World from COE app"}