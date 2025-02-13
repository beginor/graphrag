from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.staticfiles import StaticFiles

from .models import router as models_router
from .completions import router as completions_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f'\t App startup')
    # await create_db_pool()
    yield
    print(f'\t App shutdown')
    # await close_db_pool()


app = FastAPI()

app.include_router(models_router)
app.include_router(completions_router)

app.mount('/', StaticFiles(directory='wwwroot', html=True), name='static')
