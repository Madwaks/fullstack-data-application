from fastapi import FastAPI
from contextlib import asynccontextmanager

from routers.post import post_router
from routers.user import user_router
from routers.health import health_router
from database import BaseSQL, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    BaseSQL.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="My title",
    description="My description",
    version="0.0.1",
    lifespan=lifespan,
)


app.include_router(post_router)
app.include_router(user_router)
app.include_router(health_router)
