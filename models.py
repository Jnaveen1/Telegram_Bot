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

class MedicineStock(Base):

    __tablename__ = "medicine_stock"

    id = Column(Integer, primary_key=True)

    shed_no = Column(Integer, nullable=False)

    medicine_name = Column(String, nullable=False)

    available = Column(Float, default=0)

    used = Column(Float, default=0)

    unit = Column(String, default="ml")

class FeedStock(Base):

    __tablename__ = "feed_stock"

    id = Column(Integer, primary_key=True)

    date = Column(String, nullable=False)

    shed_no = Column(Integer, nullable=False)

    feed_name = Column(String, nullable=False)

    available = Column(Float, default=0)

    used = Column(Float, default=0)

    unit = Column(String, default="kg")