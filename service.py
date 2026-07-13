from datetime import date, timedelta
from database import (
    add_production,
    add_broken,
    add_sold,
    get_summary,
    get_daily_summary
)


def process_request(data):

    intent = data["intent"]
    shed = data["shed"]

    # ---------------- ADD PRODUCTION ----------------

    if intent == "add_production":
        if shed is None:
            return (
                "Please specify the shed number.\n"
                "Example: 'Shed 1 produced 10 eggs'."
            )

        quantity = data["quantity"]

        report_date = data.get("date")

        if report_date is None or report_date == "today":
            report_date = str(date.today())

        elif report_date == "yesterday":
            report_date = str(date.today() - timedelta(days=1))
        add_production(shed, quantity, report_date) 
        return f"✅ Added {quantity} produced eggs to Shed {shed}"

    # ---------------- ADD BROKEN ----------------

    elif intent == "add_broken":

        quantity = data["quantity"]

        report_date = data.get("date")

        if report_date is None or report_date == "today":
            report_date = str(date.today())

        elif report_date == "yesterday":
            report_date = str(date.today() - timedelta(days=1))

        record = get_summary(shed, report_date)

        if record is None:
            return f"No production record found for Shed {shed} on {report_date}."

        available = record.produced - record.broken - record.sold

        if quantity > available:
            return (
                f"❌ Cannot record {quantity} broken eggs.\n"
                f"Only {available} eggs are available in Shed {shed}."
            )

        add_broken(
            shed,
            quantity,
            report_date
        )

        return f"✅ Recorded {quantity} broken eggs in Shed {shed}"
    # ---------------- ADD SOLD ----------------

    elif intent == "add_sold":

        quantity = data["quantity"]

        report_date = data.get("date")

        if report_date is None or report_date == "today":
            report_date = str(date.today())

        elif report_date == "yesterday":
            report_date = str(date.today() - timedelta(days=1))

        record = get_summary(shed, report_date)

        if record is None:
            return f"No production record found for Shed {shed} on {report_date}."

        available = record.produced - record.broken - record.sold

        if quantity > available:
            return (
                f"❌ Cannot sell {quantity} eggs.\n"
                f"Only {available} eggs are available in Shed {shed}."
            )

        add_sold(
            shed,
            quantity,
            report_date
        )

        return f"✅ Recorded {quantity} sold eggs from Shed {shed}"    # ---------------- SHED SUMMARY ----------------

    elif intent == "get_summary":

        if shed is None:
            return (
                "Please specify the shed number.\n"
                "Example: 'Give summary of shed 1'."
            )

        report_date = data.get("date")

        if report_date is None or report_date == "today":
            report_date = str(date.today())

        elif report_date == "yesterday":
            report_date = str(date.today() - timedelta(days=1))

        record = get_summary(shed, report_date)

        if record is None:
            return f"No data found for Shed {shed} on {report_date}."

        stock = record.produced - record.broken - record.sold

        return (
            f"📊 Shed {shed} Summary ({report_date})\n\n"
            f"Produced: {record.produced}\n"
            f"Broken: {record.broken}\n"
            f"Sold: {record.sold}\n"
            f"Stock: {stock}"
        )

    # ---------------- BROKEN ----------------

    elif intent == "get_broken":

        if shed is None:
            return "Please specify the shed number."

        report_date = str(date.today())

        record = get_summary(shed, report_date)

        if record is None:
            return f"No data found for Shed {shed} today."

        return f"Shed {shed} has {record.broken} broken eggs today."

    # ---------------- SOLD ----------------

    elif intent == "get_sold":

        if shed is None:
            return "Please specify the shed number."

        report_date = str(date.today())

        record = get_summary(shed, report_date)

        if record is None:
            return f"No data found for Shed {shed} today."

        return f"Shed {shed} has {record.sold} sold eggs today."

    # ---------------- PRODUCTION ----------------

    elif intent == "get_production":

        if shed is None:
            return "Please specify the shed number."

        report_date = str(date.today())

        record = get_summary(shed, report_date)

        if record is None:
            return f"No data found for Shed {shed} today."

        return f"Shed {shed} produced {record.produced} eggs today."

    # ---------------- DAILY SUMMARY ----------------

    elif intent == "get_daily_summary":

        report_date = data.get("date")

        if report_date is None or report_date == "today":
            report_date = str(date.today())

        elif report_date == "yesterday":
            report_date = str(date.today() - timedelta(days=1))

        records = get_daily_summary(report_date)

        if not records:
            return f"No data found for {report_date}."

        reply = f"📊 Farm Summary ({report_date})\n\n"

        total_produced = 0
        total_broken = 0
        total_sold = 0

        for record in records:

            stock = record.produced - record.broken - record.sold

            reply += (
                f"🐔 Shed {record.shed_no}\n"
                f"Produced : {record.produced}\n"
                f"Broken   : {record.broken}\n"
                f"Sold     : {record.sold}\n"
                f"Stock    : {stock}\n\n"
            )

            total_produced += record.produced
            total_broken += record.broken
            total_sold += record.sold

        total_stock = total_produced - total_broken - total_sold

        reply += (
            "--------------------------\n"
            f"Total Produced : {total_produced}\n"
            f"Total Broken   : {total_broken}\n"
            f"Total Sold     : {total_sold}\n"
            f"Current Stock  : {total_stock}"
        )

        return reply
    
    elif intent == "get_remaining":

        if shed is None:
            return "Please specify the shed number."

        report_date = data.get("date")

        if report_date is None or report_date == "today":
            report_date = str(date.today())

        elif report_date == "yesterday":
            report_date = str(date.today() - timedelta(days=1))

        record = get_summary(shed, report_date)

        if record is None:
            return f"No data found for Shed {shed} on {report_date}."

        remaining = record.produced - record.broken - record.sold

        return (
            f"🥚 Remaining eggs in Shed {shed} ({report_date}): "
            f"{remaining}"
        )

    # ---------------- UNKNOWN ----------------

    else:
        return "Unknown operation."