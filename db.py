from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.orm import sessionmaker, DeclarativeBase


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DATABASE_URL = "sqlite:///./sports.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    ...

class Result(Base):
    __tablename__ = "sport"

    id = Column(Integer, primary_key=True, index=True)
    competition_name = Column(String)
    place = Column(String)
    date = Column(Date)
    participants = Column(Integer)
    ticket_price = Column(Float)
    prize_pool = Column(Float)
    best_result = Column(Float)

    def __repr__(self):
        return f"|id={self.id}| name={self.competition_name}, date={self.date}"
