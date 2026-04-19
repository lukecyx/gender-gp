from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import patients, prescriptions
from db.session import create_db_and_tables
import models  # noqa: F401 — ensures models are registered with SQLModel metadata

from auth import auth_backend, fastapi_users
from schemas.users import UserCreate, UserRead, UserUpdate

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(patients.router)
app.include_router(prescriptions.router)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
