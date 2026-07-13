from sqlalchemy import create_engine , func
from sqlalchemy.orm import sessionmaker
from base import Base
from datetime import date , timedelta
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

def add_production(shed_no, quantity, report_date):
    db = SessionLocal()
    today = report_date
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

def add_broken(shed_no, quantity, report_date):
    db = SessionLocal()
    today = report_date
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

def add_sold(shed_no, quantity, report_date):
    db = SessionLocal()
    today = report_date
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

def get_summary(shed_no, report_date):
    db = SessionLocal()

    # today = str(date.today())

    print("Searching for:")
    print("Shed:", shed_no)
    print("Date:", report_date)

    record = (
        db.query(EggRecord)
        .filter(
            EggRecord.shed_no == shed_no,
            EggRecord.date == report_date
        )
        .first()
    )

    db.close()

    return record

def get_daily_summary(report_date):

    db = SessionLocal()

    records = (
        db.query(EggRecord)
        .filter(EggRecord.date == report_date)
        .order_by(EggRecord.shed_no.asc())
        .all()
    )

    db.close()

    return records

def get_shed_count(report_date):

    db = SessionLocal()

    count = (
        db.query(func.count(func.distinct(EggRecord.shed_no)))
        .filter(EggRecord.date == report_date)
        .scalar()
    )

    db.close()

    return count

def get_farm_stock(report_date):

    db = SessionLocal()

    records = (
        db.query(EggRecord)
        .filter(EggRecord.date == report_date)
        .order_by(EggRecord.shed_no)
        .all()
    )

    db.close()

    return records

def get_records_by_date(report_date):

    db = SessionLocal()

    records = (
        db.query(EggRecord)
        .filter(EggRecord.date == report_date)
        .order_by(EggRecord.shed_no)
        .all()
    )

    db.close()

    return records

def get_weekly_summary(period):

    db = SessionLocal()

    today = date.today()

    if period == "last_week":

        this_week_start = today - timedelta(days=today.weekday())

        start_date = this_week_start - timedelta(days=7)

        end_date = this_week_start - timedelta(days=1)

    else:

        start_date = today - timedelta(days=today.weekday())

        end_date = today

    records = (
        db.query(EggRecord)
        .filter(
            EggRecord.date >= str(start_date),
            EggRecord.date <= str(end_date)
        )
        .order_by(EggRecord.date, EggRecord.shed_no)
        .all()
    )

    db.close()

    return records

def get_monthly_summary():

    db = SessionLocal()

    today = date.today()

    start_date = today.replace(day=1)

    records = (
        db.query(EggRecord)
        .filter(
            EggRecord.date >= str(start_date),
            EggRecord.date <= str(today)
        )
        .order_by(EggRecord.date, EggRecord.shed_no)
        .all()
    )

    db.close()

    return records
