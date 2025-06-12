from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from database.db_connection import test_db_connection,create_db_and_tables

from routers.user import router as user_router
from routers.master_data import router as master_data_router


origins = [
    "http://localhost:4200",
]



@asynccontextmanager
async def lifespan(app:FastAPI):
    # startup operation
    test_db_connection()
    create_db_and_tables()
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


app.include_router(master_data_router)
app.include_router(user_router, prefix="/users",tags=["users"])


@app.get("/")
async def check_server():
    return {"success" : True, "message" : "Server is working fine"}