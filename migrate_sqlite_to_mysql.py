from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import EggRecord, FeedStock, MedicineStock

# -----------------------
# SQLite
# -----------------------
sqlite_engine = create_engine("sqlite:///egg_database.db")
SQLiteSession = sessionmaker(bind=sqlite_engine)

# -----------------------
# MySQL
# Replace PASSWORD with your actual password.
# Since your password contains @, use %40
# -----------------------
mysql_engine = create_engine(
    "mysql+pymysql://root:Sunfra%40123@localhost:3306/egg_ai_agent"
)
MySQLSession = sessionmaker(bind=mysql_engine)

sqlite_db = SQLiteSession()
mysql_db = MySQLSession()

try:
    # -----------------------
    # Egg Records
    # -----------------------
    egg_count = 0

    for row in sqlite_db.query(EggRecord).all():

        mysql_db.add(
            EggRecord(
                date=row.date,
                shed_no=row.shed_no,
                birds=row.birds,
                mortality=row.mortality,
                produced=row.produced,
                broken=row.broken,
                sold=row.sold,
            )
        )

        egg_count += 1

    # -----------------------
    # Feed Stock
    # -----------------------
    feed_count = 0

    for row in sqlite_db.query(FeedStock).all():

        mysql_db.add(
            FeedStock(
                date=row.date,
                shed_no=row.shed_no,
                feed_name=row.feed_name,
                available=row.available,
                used=row.used,
                unit=row.unit,
            )
        )

        feed_count += 1

    # -----------------------
    # Medicine Stock
    # -----------------------
    med_count = 0

    for row in sqlite_db.query(MedicineStock).all():

        mysql_db.add(
            MedicineStock(
                shed_no=row.shed_no,
                medicine_name=row.medicine_name,
                available=row.available,
                used=row.used,
                unit=row.unit,
            )
        )

        med_count += 1

    mysql_db.commit()

    print("✅ Migration Completed Successfully!")
    print(f"Egg Records     : {egg_count}")
    print(f"Feed Records    : {feed_count}")
    print(f"Medicine Records: {med_count}")

except Exception as e:
    mysql_db.rollback()
    print("Migration failed:", e)

finally:
    sqlite_db.close()
    mysql_db.close()