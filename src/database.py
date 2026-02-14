from sqlmodel import SQLModel, Session, create_engine
import os
from .config import get_settings


settings = get_settings()
db_file_path = settings.DB_PATH.replace("sqlite:///", "")
os.makedirs(os.path.dirname(os.path.abspath(db_file_path)), exist_ok=True)

engine = create_engine(settings.DB_PATH)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
