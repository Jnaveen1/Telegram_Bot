from sqlalchemy import create_engine , func , or_
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

    record = (
        db.query(EggRecord)
        .filter(
            EggRecord.shed_no == shed_no,
            EggRecord.date == report_date
        )
        .first()
    )

    if record:
        record.produced = (record.produced or 0) + quantity
    else:
        record = EggRecord(
            date=report_date,
            shed_no=shed_no,
            produced=quantity,
        )
        db.add(record)

    db.commit()
    db.close()


def add_broken(shed_no, quantity, report_date):

    db = SessionLocal()

    record = (
        db.query(EggRecord)
        .filter(
            EggRecord.shed_no == shed_no,
            EggRecord.date == report_date
        )
        .first()
    )

    if record:
        record.broken = (record.broken or 0) + quantity
    else:
        record = EggRecord(
            date=report_date,
            shed_no=shed_no,
            broken=quantity,
        )
        db.add(record)

    db.commit()
    db.close()


def add_sold(shed_no, quantity, report_date):

    db = SessionLocal()

    record = (
        db.query(EggRecord)
        .filter(
            EggRecord.shed_no == shed_no,
            EggRecord.date == report_date
        )
        .first()
    )

    if record:
        record.sold = (record.sold or 0) + quantity
    else:
        record = EggRecord(
            date=report_date,
            shed_no=shed_no,
            sold=quantity,
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

def move_record(from_shed, to_shed, field, quantity, report_date):

    db = SessionLocal()

    try:

        source = (
            db.query(EggRecord)
            .filter(
                EggRecord.shed_no == from_shed,
                EggRecord.date == report_date
            )
            .first()
        )

        if source is None:
            db.close()
            return f"No record found for Shed {from_shed} on {report_date}."

        destination = (
            db.query(EggRecord)
            .filter(
                EggRecord.shed_no == to_shed,
                EggRecord.date == report_date
            )
            .first()
        )

        if destination is None:

            destination = EggRecord(
                shed_no=to_shed,
                date=report_date
            )

            db.add(destination)

        available = getattr(source, field) or 0

        if available < quantity:
            db.close()
            return (
                f"Cannot move {quantity} eggs.\n"
                f"Shed {from_shed} has only {available} {field}."
            )

        setattr(source, field, available - quantity)

        current = getattr(destination, field) or 0

        setattr(destination, field, current + quantity)

        db.commit()

        db.close()

        return "SUCCESS"

    except Exception as e:

        db.rollback()
        db.close()

        return str(e)
    
def update_record(shed, field, quantity, report_date):

    db = SessionLocal()

    try:

        record = (
            db.query(EggRecord)
            .filter(
                EggRecord.shed_no == shed,
                EggRecord.date == report_date
            )
            .first()
        )

        if record is None:
            db.close()
            return f"No record found for Shed {shed} on {report_date}."

        setattr(record, field, quantity)

        db.commit()

        db.close()

        return "SUCCESS"

    except Exception as e:

        db.rollback()

        db.close()

        return str(e)    
    
def remove_record(shed, field, quantity, report_date):

    db = SessionLocal()

    try:

        record = (
            db.query(EggRecord)
            .filter(
                EggRecord.shed_no == shed,
                EggRecord.date == report_date
            )
            .first()
        )

        if record is None:
            db.close()
            return f"No record found for Shed {shed} on {report_date}."

        current = getattr(record, field) or 0

        if quantity > current:
            db.close()
            return (
                f"❌ Cannot remove {quantity} eggs.\n"
                f"Shed {shed} has only {current} {field} eggs."
            )

        setattr(
            record,
            field,
            current - quantity
        )

        db.commit()

        db.close()

        return "SUCCESS"

    except Exception as e:

        db.rollback()

        db.close()

        return str(e)
    
def delete_field(shed, field, report_date):

    db = SessionLocal()

    try:

        record = (
            db.query(EggRecord)
            .filter(
                EggRecord.shed_no == shed,
                EggRecord.date == report_date
            )
            .first()
        )

        if record is None:
            db.close()
            return f"No record found for Shed {shed} on {report_date}."

        setattr(record, field, None)

        db.commit()

        db.close()

        return "SUCCESS"

    except Exception as e:

        db.rollback()
        db.close()

        return str(e)
    
def delete_record(shed, report_date):

    db = SessionLocal()

    try:

        record = (
            db.query(EggRecord)
            .filter(
                EggRecord.shed_no == shed,
                EggRecord.date == report_date
            )
            .first()
        )

        if record is None:
            db.close()
            return f"No record found for Shed {shed} on {report_date}."

        db.delete(record)

        db.commit()

        db.close()

        return "SUCCESS"

    except Exception as e:

        db.rollback()
        db.close()

        return str(e)

def add_birds(shed_no, birds, report_date):

    db = SessionLocal()

    try:

        record = (
            db.query(EggRecord)
            .filter(
                EggRecord.shed_no == shed_no,
                EggRecord.date == report_date
            )
            .first()
        )

        if record is None:

            record = EggRecord(
                shed_no=shed_no,
                date=report_date,
                birds=birds
            )

            db.add(record)

        else:
            record.birds = birds

        db.commit()

        db.close()

        return f"✅ Bird count updated to {birds} for Shed {shed_no}"

    except Exception as e:

        db.rollback()
        db.close()

        return str(e)
    
def get_birds(shed_no, report_date):

    db = SessionLocal()

    record = (
        db.query(EggRecord)
        .filter(
            EggRecord.shed_no == shed_no,
            EggRecord.date == report_date
        )
        .first()
    )

    db.close()

    if record is None:
        return None

    return record.birds

def get_total_birds(report_date):

    db = SessionLocal()

    total = (
        db.query(func.sum(EggRecord.birds))
        .filter(EggRecord.date == report_date)
        .scalar()
    )

    db.close()

    return total or 0

def get_total_live_birds(report_date):

    total_birds = get_total_birds(report_date)
    total_mortality = get_total_mortality(report_date)

    return total_birds - total_mortality

def add_mortality(shed_no, quantity, report_date):

    db = SessionLocal()

    try:

        record = (
            db.query(EggRecord)
            .filter(
                EggRecord.shed_no == shed_no,
                EggRecord.date == report_date
            )
            .first()
        )

        if record is None:

            record = EggRecord(
                shed_no=shed_no,
                date=report_date,
                mortality=quantity
            )

            db.add(record)

        else:

            record.mortality = (record.mortality or 0) + quantity

        db.commit()
        db.close()

        return f"✅ Recorded {quantity} bird deaths in Shed {shed_no}"

    except Exception as e:

        db.rollback()
        db.close()

        return str(e)
    
def get_mortality(shed_no, report_date):

    db = SessionLocal()

    record = (
        db.query(EggRecord)
        .filter(
            EggRecord.shed_no == shed_no,
            EggRecord.date == report_date
        )
        .first()
    )

    db.close()

    if record is None:
        return 0

    return record.mortality or 0

def get_total_mortality(report_date):

    db = SessionLocal()

    total = (
        db.query(func.sum(EggRecord.mortality))
        .filter(EggRecord.date == report_date)
        .scalar()
    )

    db.close()

    return total or 0

def add_feed(shed_no, quantity, report_date):

    db = SessionLocal()

    try:

        record = (
            db.query(EggRecord)
            .filter(
                EggRecord.shed_no == shed_no,
                EggRecord.date == report_date
            )
            .first()
        )

        if record is None:

            record = EggRecord(
                shed_no=shed_no,
                date=report_date,
                feed=quantity
            )

            db.add(record)

        else:

            record.feed = (record.feed or 0) + quantity

        db.commit()
        db.close()

        return f"✅ Added {quantity} kg feed to Shed {shed_no}"

    except Exception as e:

        db.rollback()
        db.close()

        return str(e)

def get_feed(shed_no, report_date):

    db = SessionLocal()

    record = (
        db.query(EggRecord)
        .filter(
            EggRecord.shed_no == shed_no,
            EggRecord.date == report_date
        )
        .first()
    )

    db.close()

    if record is None:
        return 0

    return record.feed or 0 

def get_total_feed(report_date):

    db = SessionLocal()

    total = (
        db.query(func.sum(EggRecord.feed))
        .filter(EggRecord.date == report_date)
        .scalar()
    )

    db.close()

    return total or 0

def get_missing_sheds(report_date):

    db = SessionLocal()

    all_sheds = set(range(1, 10))   # 1 to 9

    reported_sheds = {
        record.shed_no
        for record in db.query(EggRecord)
        .filter(EggRecord.date == report_date)
        .all()
    }

    db.close()

    missing = sorted(all_sheds - reported_sheds)

    return missing

def get_missing_fields(report_date):

    db = SessionLocal()

    all_sheds = range(1, 10)

    records = (
        db.query(EggRecord)
        .filter(EggRecord.date == report_date)
        .all()
    )

    record_map = {
        record.shed_no: record
        for record in records
    }

    db.close()

    result = {}

    for shed in all_sheds:

        if shed not in record_map:

            result[shed] = ["No report submitted"]
            continue

        record = record_map[shed]

        missing = []

        if record.birds is None:
            missing.append("Bird Count")

        if record.mortality is None:
            missing.append("Mortality")

        if record.feed is None:
            missing.append("Feed")

        if record.produced is None:
            missing.append("Production")

        if record.broken is None:
            missing.append("Broken")

        if record.sold is None:
            missing.append("Sold")

        if missing:
            result[shed] = missing

    return result

