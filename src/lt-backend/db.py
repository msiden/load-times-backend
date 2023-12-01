from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import OperationalError
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
import os


ENVIRONMENT = os.getenv("NGDB_ENV")
IS_PROD = ENVIRONMENT == "prod"
PASSWORD = os.getenv("NGDB_PASSWORD") if IS_PROD else "abc123"
URL = os.getenv("NGDB_URL") if IS_PROD else "localhost"
DB_CONFIG = f"postgresql+psycopg2://postgres:{PASSWORD}@{URL}:5432/scores"

engine = create_engine(DB_CONFIG)


class Base(DeclarativeBase):
    pass


class Scores(Base):
    __tablename__ = "scores"
    id: Mapped[str] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String(30))
    score: Mapped[int] = mapped_column(Integer)
    level: Mapped[int] = mapped_column(Integer)

    def __repr__(self) -> str:
        return f"id:{self.id!r}, user_name:{self.user_name!r}, score:{self.score!r}, level:{self.level!r}"


class ScoresSchema(SQLAlchemySchema):
    class Meta:
        model = Scores
        load_instance = True

    id = auto_field()
    user_name = auto_field()
    score = auto_field()
    level = auto_field()


def create_all():
    try:
        Base.metadata.create_all(engine)
    except OperationalError:
        print("DB connection failed")


def insert_data(id: str, score: int, level: int, user_name: str) -> int:
    with Session(engine) as session:

        new_score = Scores(
            id=id,
            score=score,
            level=level,
            user_name=user_name
        )

        session.add(new_score)
        session.commit()


def get_data(chunk_size: int, level: int) -> dict:
    scores_schema = ScoresSchema(many=True)

    with Session(engine) as session:
        statement = select(Scores).where(Scores.level == level).order_by(Scores.score.desc()).limit(chunk_size)
        result = session.scalars(statement).all()
        return scores_schema.dump(result)


create_all()
