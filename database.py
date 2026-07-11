from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from datetime import date
from models import EggRecord


DATABASE_URL = "sqlite:///egg_database.db"


engine = create_engine(
    DATABASE_URL,
    echo=False
)


SessionLocal = sessionmaker(
    bind=engine
)


def create_database():

    Base.metadata.create_all(engine)


def add_production(shed_no, quantity):

    db = SessionLocal()

    today = str(date.today())

    record = db.query(EggRecord).filter(
        EggRecord.shed_no == shed_no,
        EggRecord.date == today
    ).first()


    if record:
        record.produced += quantity

    else:
        record = EggRecord(
            date=today,
            shed_no=shed_no,
            produced=quantity,
            broken=0,
            sold=0
        )

        db.add(record)


    db.commit()
    db.close()

def add_broken(shed_no, quantity):

    db = SessionLocal()

    today = str(date.today())


    record = db.query(EggRecord).filter(
        EggRecord.shed_no == shed_no,
        EggRecord.date == today
    ).first()


    if record:

        record.broken += quantity

    else:

        record = EggRecord(
            date=today,
            shed_no=shed_no,
            produced=0,
            broken=quantity,
            sold=0
        )

        db.add(record)


    db.commit()
    db.close()

def add_sold(shed_no, quantity):

    db = SessionLocal()

    today = str(date.today())


    record = db.query(EggRecord).filter(
        EggRecord.shed_no == shed_no,
        EggRecord.date == today
    ).first()


    if record:

        record.sold += quantity

    else:

        record = EggRecord(
            date=today,
            shed_no=shed_no,
            produced=0,
            broken=0,
            sold=quantity
        )

        db.add(record)


    db.commit()
    db.close()