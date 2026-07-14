from sqlalchemy import Column, Integer, String , Float
from base import Base


class EggRecord(Base):

    __tablename__ = "egg_records"

    id = Column(Integer, primary_key=True)

    date = Column(String)
    shed_no = Column(Integer)
    birds = Column(Integer, nullable=True)
    mortality = Column(Integer, nullable=True)
    feed = Column(Float, nullable=True)

    produced = Column(Integer, nullable=True)
    broken = Column(Integer, nullable=True)
    sold = Column(Integer, nullable=True)

