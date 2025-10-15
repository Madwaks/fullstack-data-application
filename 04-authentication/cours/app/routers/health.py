from fastapi import APIRouter

health_router = APIRouter()


@health_router.get("/")
def read_root():
    return {"Hello": "World"}


@health_router.get("/api")
def read_hello():
    return {"Hello": "Api"}


@health_router.get("/health")
def read_root():
    return {"message": "Api is running fine!"}
