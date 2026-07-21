# from llm import understand_message


# result = understand_message(
#     "Move 100 produced eggs from shed 1 to shed 2"
# )


# print(result)

from types import SimpleNamespace
from report_generator import generate_daily_pdf

from report_generator import generate_daily_pdf

from database import (
    get_daily_summary,
    get_all_feeds,
    get_all_medicines,
    get_feed_totals_kg,
    get_medicine_totals_kg , 
    get_missing_sheds,
    get_missing_fields
)

report_date = "2026-07-20"

pending_reports = []

missing_sheds = get_missing_sheds(report_date)

for shed in missing_sheds:

    pending_reports.append({
        "shed": shed,
        "missing": ["No Report Submitted"]
    })

missing_fields = get_missing_fields(report_date)

for shed, fields in missing_fields.items():

    # Skip because already added above
    if shed in missing_sheds:
        continue

    pending_reports.append({
        "shed": shed,
        "missing": fields
    })

report_date = "2026-07-20"

report_data = {

    "report_date": report_date ,

    "production_records": get_daily_summary(report_date),

    "feed_records": get_all_feeds(report_date),

    "medicine_records": get_all_medicines(),

    "production_totals": {},

    "feed_totals": get_feed_totals_kg(),

    "medicine_totals": get_medicine_totals_kg(),

    "pending_reports": pending_reports

}

pdf = generate_daily_pdf(report_data)

print(f"PDF Generated Successfully:\n{pdf}")