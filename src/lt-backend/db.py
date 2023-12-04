from sqlalchemy import String, Integer, Float
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import OperationalError
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
import uuid



engine = create_engine("sqlite:///database.db")


class Base(DeclarativeBase):
    pass


class LoadTimes(Base):
    __tablename__ = "load_times"
    id: Mapped[str] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String)
    search_phrase: Mapped[str] = mapped_column(String)
    start_time: Mapped[str] = mapped_column(String)
    response_time: Mapped[str] = mapped_column(Float)
    occurencies: Mapped[int] = mapped_column(Integer)

class LoadTimesSchema(SQLAlchemySchema):
    class Meta:
        model = LoadTimes
        load_instance = True

    id = auto_field()
    url = auto_field()
    search_phrase = auto_field()
    start_time = auto_field()
    response_time = auto_field()
    occurencies = auto_field()


def create_all():
    try:
        Base.metadata.create_all(engine)
    except OperationalError:
        print("DB connection failed")


def insert_data(url: str, search_phrase: str, start_time: str, response_time: float, occurencies: int) -> uuid.uuid4:
    with Session(engine) as session:

        id = str(uuid.uuid4())

        new_entry = LoadTimes(
            id=id,
            url=url,
            search_phrase=search_phrase,
            start_time=start_time,
            response_time=response_time,
            occurencies=occurencies
        )

        session.add(new_entry)
        session.commit()

    return id


def get_data(chunk_size: int) -> dict:
    load_times_schema = LoadTimesSchema(many=True)

    with Session(engine) as session:
        statement = select(LoadTimes).order_by(LoadTimes.start_time.desc()).limit(chunk_size)
        result = session.scalars(statement).all()
        return load_times_schema.dump(result)


create_all()
