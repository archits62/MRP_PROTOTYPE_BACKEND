from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

# from routers import sku
from routers.master_data import router
# from routers import router as api_router
from database.db_connection import test_db_connection

origins = [
    "http://localhost:4200",
]



@asynccontextmanager
async def lifespan(app:FastAPI):
    test_db_connection() # startup operation
    yield
    # cleanup operations, after shutdown

app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)


@app.get("/")
def read_root():
    return{"Hello": "Fast API"}
