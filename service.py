from datetime import date, timedelta
from database import (
    add_production,
    add_broken,
    add_sold,
    get_summary,
    get_daily_summary, 
    get_shed_count, 
    get_farm_stock, 
    get_records_by_date, 
)

def eggs_to_trays(eggs):
    trays = eggs // 30
    remaining_eggs = eggs % 30
    return f"{trays}.{remaining_eggs:02d}"

def get_report_date(data):

    report_date = data.get("date")

    if report_date is None or report_date == "today":
        return str(date.today())

    elif report_date == "yesterday":
        return str(date.today() - timedelta(days=1))

    return report_date

def format_quantity(eggs, unit):

    if unit == "tray":
        return f"{eggs_to_trays(eggs)} trays"

    return f"{eggs} eggs"

def process_request(data):

    intent = data["intent"]
    shed = data["shed"]
    unit = data.get("unit", "egg")

    # ---------------- ADD PRODUCTION ----------------

    if intent == "add_production":
        if shed is None and intent not in [
            "get_daily_summary",
            "get_shed_count",
            "get_farm_stock", 
            "get_total_broken"
        ]:
            return (
                "Please specify the shed number.\n"
                "Example: 'Give summary of shed 1'."
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

        report_date = get_report_date(data)

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

        report_date = get_report_date(data)

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

        report_date = get_report_date(data)

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

        if unit == "tray":
            trays = eggs_to_trays(record.produced)
            return (
                f"Shed {shed} produced "
                f"{trays} trays."
            )

        return (
            f"Shed {shed} produced "
            f"{format_quantity(record.produced, unit)} today."
        )

    # ---------------- DAILY SUMMARY ----------------

    elif intent == "get_daily_summary":

        report_date = get_report_date(data)

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

        report_date = get_report_date(data)

        record = get_summary(shed, report_date)

        if record is None:
            return f"No data found for Shed {shed} on {report_date}."

        remaining = record.produced - record.broken - record.sold

        if unit == "tray":
            trays = eggs_to_trays(remaining)
            return (
                f"Shed {shed} has "
                f"{trays} trays remaining."
            )

        return (
            f"Shed {shed} has "
            f"{remaining} eggs remaining."
        )

    elif intent == "get_shed_count":

        report_date = get_report_date(data)

        count = get_shed_count(report_date)

        return f"There are {count} sheds on {report_date}."
    
    elif intent == "get_farm_stock":

        report_date = get_report_date(data)

        records = get_farm_stock(report_date)

        if not records:
            return f"No data found for {report_date}."

        reply = f"📦 Farm Stock ({report_date})\n\n"

        total_stock = 0

        for record in records:

            stock = record.produced - record.broken - record.sold

            if unit == "tray":
                stock_display = f"{eggs_to_trays(stock)} trays"
            else:
                stock_display = f"{stock} eggs"

            reply += (
                f"🐔 Shed {record.shed_no} : {stock_display}\n"
            )

            total_stock += stock

        if unit == "tray":
            total_display = f"{eggs_to_trays(total_stock)} trays"
        else:
            total_display = f"{total_stock} eggs"

        reply += (
            "\n--------------------------\n"
            f"Total Stock : {total_display}"
        )

        return reply

    elif intent == "get_total_broken":

        report_date = get_report_date(data)

        records = get_records_by_date(report_date)

        if not records:
            return f"No data found for {report_date}."

        total_broken = sum(record.broken for record in records)

        return (
            f"🥚 Total Broken Eggs ({report_date})\n\n"
            f"{format_quantity(total_broken, unit)}"
        )
    
    elif intent == "get_total_production":

        report_date = get_report_date(data)

        records = get_records_by_date(report_date)

        # report_date = get_report_date(data)

        total = sum(record.produced for record in records)

        return (
            f"🥚 Total Production ({report_date})\n\n"
            f"{format_quantity(total, unit)}"
        )

    elif intent == "get_total_sold":

        report_date = get_report_date(data)
        if report_date is None or report_date == "today":
            report_date = str(date.today())

        elif report_date == "yesterday":
            report_date = str(date.today() - timedelta(days=1))

        records = get_records_by_date(report_date)

        total = sum(record.sold for record in records)

        return (
            f"🥚 Total Sold ({report_date})\n\n"
            f"{format_quantity(total, unit)}"
        )

    elif intent == "get_total_remaining":

        report_date = get_report_date(data)

        records = get_records_by_date(report_date)

        total = sum(
            record.produced - record.broken - record.sold
            for record in records
        )

        return (
            f"🥚 Total Remaining ({report_date})\n\n"
            f"{format_quantity(total, unit)}"
        )    

    elif intent == "get_highest_production":

        report_date = get_report_date(data)

        records = get_records_by_date(report_date)

        if not records:
            return f"No data found for {report_date}."

        highest = max(records, key=lambda r: r.produced)

        return (
            f"🏆 Highest Production ({report_date})\n\n"
            f"🐔 Shed {highest.shed_no}\n"
            f"Produced : {format_quantity(highest.produced, unit)}"
        )
    
    elif intent == "get_highest_broken":

        report_date = get_report_date(data)

        records = get_records_by_date(report_date)

        if not records:
            return f"No data found for {report_date}."

        highest = max(records, key=lambda r: r.broken)

        return (
            f"🥚 Highest Broken Eggs ({report_date})\n\n"
            f"🐔 Shed {highest.shed_no}\n"
            f"Broken : {format_quantity(highest.broken, unit)}"
        )

    elif intent == "get_highest_sold":

        report_date = get_report_date(data)

        records = get_records_by_date(report_date)

        if not records:
            return f"No data found for {report_date}."

        highest = max(records, key=lambda r: r.sold)

        return (
            f"🥚 Highest Sold Eggs ({report_date})\n\n"
            f"🐔 Shed {highest.shed_no}\n"
            f"Sold : {format_quantity(highest.sold, unit)}"
        )

    elif intent == "get_highest_stock":

        report_date = get_report_date(data)

        records = get_records_by_date(report_date)

        if not records:
            return f"No data found for {report_date}."

        highest = max(
            records,
            key=lambda r: r.produced - r.broken - r.sold
        )

        stock = highest.produced - highest.broken - highest.sold

        return (
            f"📦 Highest Stock ({report_date})\n\n"
            f"🐔 Shed {highest.shed_no}\n"
            f"Stock : {format_quantity(stock, unit)}"
        )

    elif intent == "get_lowest_production":

        report_date = get_report_date(data)

        records = get_records_by_date(report_date)

        if not records:
            return f"No data found for {report_date}."

        lowest = min(records, key=lambda r: r.produced)

        return (
            f"📉 Lowest Production ({report_date})\n\n"
            f"🐔 Shed {lowest.shed_no}\n"
            f"Produced : {format_quantity(lowest.produced, unit)}"
        )

    elif intent == "get_lowest_broken":

        report_date = get_report_date(data)

        records = get_records_by_date(report_date)

        if not records:
            return f"No data found for {report_date}."

        lowest = min(records, key=lambda r: r.broken)

        return (
            f"📉 Lowest Broken Eggs ({report_date})\n\n"
            f"🐔 Shed {lowest.shed_no}\n"
            f"Broken : {format_quantity(lowest.broken, unit)}"
        )

    elif intent == "get_lowest_sold":

        report_date = get_report_date(data)

        records = get_records_by_date(report_date)

        if not records:
            return f"No data found for {report_date}."

        lowest = min(records, key=lambda r: r.sold)

        return (
            f"📉 Lowest Sold Eggs ({report_date})\n\n"
            f"🐔 Shed {lowest.shed_no}\n"
            f"Sold : {format_quantity(lowest.sold, unit)}"
        )

    elif intent == "get_lowest_stock":

        report_date = get_report_date(data)

        records = get_records_by_date(report_date)

        if not records:
            return f"No data found for {report_date}."

        lowest = min(
            records,
            key=lambda r: r.produced - r.broken - r.sold
        )

        stock = lowest.produced - lowest.broken - lowest.sold

        return (
            f"📉 Lowest Stock ({report_date})\n\n"
            f"🐔 Shed {lowest.shed_no}\n"
            f"Stock : {format_quantity(stock, unit)}"
        )
