from sqlalchemy import Column, Integer, String
from base import Base


class EggRecord(Base):

    __tablename__ = "egg_records"

    id = Column(Integer, primary_key=True)

    date = Column(String)

    shed_no = Column(Integer)

    produced = Column(Integer, default=0)

    broken = Column(Integer, default=0)

    sold = Column(Integer, default=0)