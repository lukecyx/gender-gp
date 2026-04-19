from sqlmodel import SQLModel, create_engine, Session
from config import Settings

settings = Settings()  # type: ignore[call-arg]

engine = create_engine(settings.db_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
