from database import SessionLocal
from models import EggRecord

db = SessionLocal()

records = db.query(EggRecord).all()

for record in records:
    print(
        f"Date: {record.date}, "
        f"Shed: {record.shed_no}, "
        f"Produced: {record.produced}, "
        f"Broken: {record.broken}, "
        f"Sold: {record.sold}"
    )

db.close()