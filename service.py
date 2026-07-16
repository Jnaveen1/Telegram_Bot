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
    get_weekly_summary, 
    get_monthly_summary , 
    move_record , 
    update_record ,
    remove_record , 
    delete_field,
    delete_record , 
    add_birds,
    get_birds,
    get_total_birds, 
    add_mortality,
    get_mortality,
    get_total_mortality , 
    add_feed,
    get_feed,
    get_total_feed ,
    get_total_live_birds , 
    get_missing_sheds,
    get_missing_fields
)

def _safe_quantity(value):
    if value is None:
        return None

    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _safe_number(value):
    if value is None:
        return 0

    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def generate_daily_reminder(report_date):

    missing_sheds = get_missing_sheds(report_date)

    missing_fields = get_missing_fields(report_date)

    reply = f"⏰ Daily Reminder ({report_date})\n\n"

    if missing_sheds:

        reply += "❌ Missing Shed Reports\n"

        for shed in missing_sheds:
            reply += f"• Shed {shed}\n"

        reply += "\n"

    incomplete = False

    for shed, fields in missing_fields.items():

        if fields == ["No report submitted"]:
            continue

        incomplete = True

        reply += (
            f"🐔 Shed {shed}\n"
            f"Missing : {', '.join(fields)}\n\n"
        )

    if not missing_sheds and not incomplete:

        return "✅ All 9 sheds have submitted complete reports."

    return reply

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

def generate_period_summary(records, title):

    if not records:
        return "No records found."

    reply = f"{title}\n\n"

    total_birds = 0
    total_mortality = 0
    total_feed = 0

    total_produced = 0
    total_broken = 0
    total_sold = 0

    current_date = None

    day_birds = 0
    day_mortality = 0
    day_feed = 0

    day_produced = 0
    day_broken = 0
    day_sold = 0

    for record in records:

        if current_date != record.date:

            if current_date is not None:

                stock = day_produced - day_broken - day_sold

                reply += (
                    f"Birds      : {day_birds}\n"
                    f"Mortality  : {day_mortality}\n"
                    f"Feed       : {day_feed} kg\n"
                    f"Produced   : {day_produced}\n"
                    f"Broken     : {day_broken}\n"
                    f"Sold       : {day_sold}\n"
                    f"Stock      : {stock}\n\n"
                )

            current_date = record.date

            reply += f"📅 {current_date}\n"

            day_birds = 0
            day_mortality = 0
            day_feed = 0

            day_produced = 0
            day_broken = 0
            day_sold = 0

        birds = _safe_number(record.birds)
        mortality = _safe_number(record.mortality)
        feed = _safe_number(record.feed)

        produced = _safe_number(record.produced)
        broken = _safe_number(record.broken)
        sold = _safe_number(record.sold)

        day_birds += birds
        day_mortality += mortality
        day_feed += feed

        day_produced += produced
        day_broken += broken
        day_sold += sold

        total_birds += birds
        total_mortality += mortality
        total_feed += feed

        total_produced += produced
        total_broken += broken
        total_sold += sold

    stock = day_produced - day_broken - day_sold

    reply += (
        f"Birds      : {day_birds}\n"
        f"Mortality  : {day_mortality}\n"
        f"Feed       : {day_feed} kg\n"
        f"Produced   : {day_produced}\n"
        f"Broken     : {day_broken}\n"
        f"Sold       : {day_sold}\n"
        f"Stock      : {stock}\n\n"
    )

    total_stock = total_produced - total_broken - total_sold

    reply += (
        "--------------------------\n"
        f"Total Birds      : {total_birds}\n"
        f"Total Mortality  : {total_mortality}\n"
        f"Total Feed       : {total_feed} kg\n\n"
        f"Total Produced   : {total_produced}\n"
        f"Total Broken     : {total_broken}\n"
        f"Total Sold       : {total_sold}\n"
        f"Current Stock    : {total_stock}"
    )

    return reply

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
            "get_total_broken", 
            "get_weekly_summary",
            "get_monthly_summary",
        ]:
            return (
                "Please specify the shed number.\n"
                "Example: 'Give summary of shed 1'."
            )

        quantity = _safe_quantity(data.get("quantity"))

        if quantity is None:
            return "Please provide a valid quantity."

        report_date = data.get("date")

        if report_date is None or report_date == "today":
            report_date = str(date.today())

        elif report_date == "yesterday":
            report_date = str(date.today() - timedelta(days=1))
        add_production(shed, quantity, report_date) 
        return f"✅ Added {quantity} produced eggs to Shed {shed}"

    # ---------------- ADD BROKEN ----------------

    elif intent == "add_broken":

        quantity = _safe_quantity(data.get("quantity"))

        if quantity is None:
            return "Please provide a valid quantity."

        report_date = get_report_date(data)

        record = get_summary(shed, report_date)

        if record is None:
            return f"No production record found for Shed {shed} on {report_date}."

        produced = _safe_number(record.produced)
        broken = _safe_number(record.broken)
        sold = _safe_number(record.sold)

        available = produced - broken - sold

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

        quantity = _safe_quantity(data.get("quantity"))

        if quantity is None:
            return "Please provide a valid quantity."

        report_date = get_report_date(data)

        record = get_summary(shed, report_date)

        if record is None:
            return f"No production record found for Shed {shed} on {report_date}."

        produced = _safe_number(record.produced)
        broken = _safe_number(record.broken)
        sold = _safe_number(record.sold)

        available = produced - broken - sold

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

        produced = _safe_number(record.produced)
        broken = _safe_number(record.broken)
        sold = _safe_number(record.sold)

        stock = produced - broken - sold

        return (
            f"📊 Shed {shed} Summary ({report_date})\n\n"
            f"🐔 Birds       : {record.birds}\n"
            f"💀 Mortality  : {record.mortality}\n"
            f"🌾 Feed       : {record.feed} kg\n\n"
            f"🥚 Produced   : {record.produced}\n"
            f"❌ Broken     : {record.broken}\n"
            f"📦 Sold       : {record.sold}\n"
            f"📦 Stock      : {stock}"
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

        total_birds = 0
        total_mortality = 0
        total_feed = 0

        total_produced = 0
        total_broken = 0
        total_sold = 0

        for record in records:

            birds = _safe_number(record.birds)
            mortality = _safe_number(record.mortality)
            feed = _safe_number(record.feed)

            produced = _safe_number(record.produced)
            broken = _safe_number(record.broken)
            sold = _safe_number(record.sold)

            stock = produced - broken - sold

            reply += (
                f"🐔 Shed {record.shed_no}\n"
                f"Birds      : {birds}\n"
                f"Mortality  : {mortality}\n"
                f"Feed       : {feed} kg\n"
                f"Produced   : {produced}\n"
                f"Broken     : {broken}\n"
                f"Sold       : {sold}\n"
                f"Stock      : {stock}\n\n"
            )

            total_birds += birds
            total_mortality += mortality
            total_feed += feed

            total_produced += produced
            total_broken += broken
            total_sold += sold

        total_stock = total_produced - total_broken - total_sold

        reply += (
            "--------------------------\n"
            f"Total Birds      : {total_birds}\n"
            f"Total Mortality  : {total_mortality}\n"
            f"Total Feed       : {total_feed} kg\n\n"
            f"Total Produced   : {total_produced}\n"
            f"Total Broken     : {total_broken}\n"
            f"Total Sold       : {total_sold}\n"
            f"Current Stock    : {total_stock}"
        )

        return reply
    
    elif intent == "get_remaining":

        if shed is None:
            return "Please specify the shed number."

        report_date = get_report_date(data)

        record = get_summary(shed, report_date)

        if record is None:
            return f"No data found for Shed {shed} on {report_date}."
        
        produced = _safe_number(record.produced)
        broken = _safe_number(record.broken)
        sold = _safe_number(record.sold)

        remaining = produced - broken - sold

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

            produced = _safe_number(record.produced)
            broken = _safe_number(record.broken)
            sold = _safe_number(record.sold)

            stock = produced - broken - sold

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

        total_broken = sum(_safe_number(record.broken) for record in records)

        return (
            f"🥚 Total Broken Eggs ({report_date})\n\n"
            f"{format_quantity(total_broken, unit)}"
        )
    
    elif intent == "get_total_production":

        report_date = get_report_date(data)

        records = get_records_by_date(report_date)

        # report_date = get_report_date(data)

        total = sum(_safe_number(record.produced) for record in records)

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

        total = sum(_safe_number(record.sold) for record in records)

        return (
            f"🥚 Total Sold ({report_date})\n\n"
            f"{format_quantity(total, unit)}"
        )

    elif intent == "get_total_remaining":

        report_date = get_report_date(data)

        records = get_records_by_date(report_date)

        total = sum(
            (_safe_number(record.produced))
            - (_safe_number(record.broken))
            - (_safe_number(record.sold))
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

        highest = max(records, key=lambda r: _safe_number(r.produced))

        return (
            f"🏆 Highest Production ({report_date})\n\n"
            f"🐔 Shed {highest.shed_no}\n"
            f"Produced : {format_quantity(_safe_number(highest.produced), unit)}"
        )
    
    elif intent == "get_highest_broken":

        report_date = get_report_date(data)

        records = get_records_by_date(report_date)

        if not records:
            return f"No data found for {report_date}."

        highest = max(records, key=lambda r: _safe_number(r.broken))

        return (
            f"🥚 Highest Broken Eggs ({report_date})\n\n"
            f"🐔 Shed {highest.shed_no}\n"
            f"Broken : {format_quantity(_safe_number(highest.broken), unit)}"
        )

    elif intent == "get_highest_sold":

        report_date = get_report_date(data)

        records = get_records_by_date(report_date)

        if not records:
            return f"No data found for {report_date}."

        highest = max(records, key=lambda r: _safe_number(r.sold))

        return (
            f"🥚 Highest Sold Eggs ({report_date})\n\n"
            f"🐔 Shed {highest.shed_no}\n"
            f"Sold : {format_quantity(_safe_number(highest.sold), unit)}"
        )

    elif intent == "get_highest_stock":

        report_date = get_report_date(data)

        records = get_records_by_date(report_date)

        if not records:
            return f"No data found for {report_date}."

        highest = max(
            records,
            key=lambda r: _safe_number(r.produced) - _safe_number(r.broken) - _safe_number(r.sold)
        )

        stock = _safe_number(highest.produced) - _safe_number(highest.broken) - _safe_number(highest.sold)

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

        lowest = min(records, key=lambda r: _safe_number(r.produced))

        return (
            f"📉 Lowest Production ({report_date})\n\n"
            f"🐔 Shed {lowest.shed_no}\n"
            f"Produced : {format_quantity(_safe_number(lowest.produced), unit)}"
        )

    elif intent == "get_lowest_broken":

        report_date = get_report_date(data)

        records = get_records_by_date(report_date)

        if not records:
            return f"No data found for {report_date}."

        lowest = min(records, key=lambda r: _safe_number(r.broken))

        return (
            f"📉 Lowest Broken Eggs ({report_date})\n\n"
            f"🐔 Shed {lowest.shed_no}\n"
            f"Broken : {format_quantity(_safe_number(lowest.broken), unit)}"
        )

    elif intent == "get_lowest_sold":

        report_date = get_report_date(data)

        records = get_records_by_date(report_date)

        if not records:
            return f"No data found for {report_date}."

        lowest = min(records, key=lambda r: _safe_number(r.sold))

        return (
            f"📉 Lowest Sold Eggs ({report_date})\n\n"
            f"🐔 Shed {lowest.shed_no}\n"
            f"Sold : {format_quantity(_safe_number(lowest.sold), unit)}"
        )

    elif intent == "get_lowest_stock":

        report_date = get_report_date(data)

        records = get_records_by_date(report_date)

        if not records:
            return f"No data found for {report_date}."

        lowest = min(
            records,
            key=lambda r: _safe_number(r.produced) - _safe_number(r.broken) - _safe_number(r.sold)
        )

        stock = _safe_number(lowest.produced) - _safe_number(lowest.broken) - _safe_number(lowest.sold)

        return (
            f"📉 Lowest Stock ({report_date})\n\n"
            f"🐔 Shed {lowest.shed_no}\n"
            f"Stock : {format_quantity(stock, unit)}"
        )

    elif intent == "get_weekly_summary":

        period = data.get("date", "this_week")

        records = get_weekly_summary(period)

        if period == "last_week":
            title = "📅 Last Week Report"
        else:
            title = "📅 This Week Report"

        return generate_period_summary(records, title)

    elif intent == "get_monthly_summary":

        records = get_monthly_summary()

        return generate_period_summary(
            records,
            "📅 Monthly Report"
        )

    elif intent == "move_record":

        from_shed = data["from_shed"]
        to_shed = data["to_shed"]
        field = data["field"]
        quantity = data["quantity"]

        report_date = data.get("date")

        result = move_record(
            from_shed,
            to_shed,
            field,
            quantity,
            report_date
        )

        if result == "SUCCESS":

            return (
                f"✅ Successfully moved {quantity} {field} eggs\n\n"
                f"From Shed {from_shed}\n"
                f"To Shed {to_shed}"
            )

        return result
    
    elif intent == "update_record":

        shed = data["shed"]
        field = data["field"]
        quantity = data["quantity"]

        report_date = data.get("date")

        result = update_record(
            shed,
            field,
            quantity,
            report_date
        )

        if result == "SUCCESS":

            return (
                f"✅ Updated {field} of Shed {shed} "
                f"to {quantity} eggs."
            )

        return result
    
    elif intent == "remove_record":

        shed = data["shed"]
        field = data["field"]
        quantity = data["quantity"]

        report_date = data.get("date")

        result = remove_record(
            shed,
            field,
            quantity,
            report_date
        )

        if result == "SUCCESS":

            return (
                f"✅ Removed {quantity} {field} eggs "
                f"from Shed {shed}"
            )

        return result

    elif intent == "delete_field":

        shed = data["shed"]
        field = data["field"]

        report_date = data.get("date")

        result = delete_field(
            shed,
            field,
            report_date
        )

        if result == "SUCCESS":

            return (
                f"✅ Deleted {field} data "
                f"from Shed {shed}"
            )

        return result

    elif intent == "delete_record":

        shed = data["shed"]

        report_date = data.get("date")

        result = delete_record(
            shed,
            report_date
        )

        if result == "SUCCESS":

            return (
                f"✅ Deleted all records "
                f"of Shed {shed} "
                f"for {report_date}"
            )

        return result

    elif intent == "add_birds":

        shed = data["shed"]
        quantity = data["quantity"]

        report_date = data.get("date")

        result = add_birds(
            shed,
            quantity,
            report_date
        )

        return result

    elif intent == "get_birds":

        shed = data["shed"]
        
        report_date = data.get("date")

        # <-- This part must be OUTSIDE the if/elif

        birds = get_birds(
            shed,
            report_date
        )

        if birds is None:
            return f"No bird count found for Shed {shed} on {report_date}."

        return (
            f"🐔 Bird Count ({report_date})\n\n"
            f"Shed {shed} : {birds} birds"
        )

    elif intent == "get_total_birds":
        report_date = data.get("date")

        if report_date is None or report_date == "today":
            report_date = str(date.today())

        elif report_date == "yesterday":
            report_date = str(date.today() - timedelta(days=1))

        total = get_total_birds(report_date)

        return (
            f"🐔 Total Birds ({report_date})\n\n"
            f"{total} birds"
        )

    elif intent == "add_mortality":

        shed = data["shed"]
        report_date = get_report_date(data)
        quantity = data["quantity"]

        result = add_mortality(
            shed,
            quantity,
            report_date
        )

        return result
    
    elif intent == "get_mortality":

        shed = data["shed"]
        report_date = get_report_date(data)
        mortality = get_mortality(
            shed,
            report_date
        )

        return (
            f"🐔 Shed {shed}\n\n"
            f"Mortality : {mortality} birds"
        )
    
    elif intent == "get_total_mortality":
        report_date = get_report_date(data)
        total = get_total_mortality(report_date)

        return (
            f"🐔 Total Mortality ({report_date})\n\n"
            f"{total} birds"
        )
    
    elif intent == "add_feed":

        shed = data["shed"]
        quantity = data["quantity"]

        report_date = get_report_date(data)
        
        result = add_feed(
            shed,
            quantity,
            report_date
        )

        return result
    
    elif intent == "get_feed":

        shed = data["shed"]

        report_date = get_report_date(data)

        feed = get_feed(
            shed,
            report_date
        )

        return (
            f"🌾 Feed Consumption ({report_date})\n\n"
            f"Shed {shed} : {feed} kg"
        )
    
    elif intent == "get_total_feed":

        report_date = get_report_date(data)

        total = get_total_feed(report_date)

        return (
            f"🌾 Total Feed ({report_date})\n\n"
            f"{total} kg"
        )
    
    elif intent == "get_total_live_birds":

        report_date = get_report_date(data)

        live_birds = get_total_live_birds(report_date)

        return (
            f"🐓 Total Live Birds ({report_date})\n\n"
            f"{live_birds} birds"
        )
    
    elif intent == "get_missing_sheds":

        report_date = get_report_date(data)

        missing = get_missing_sheds(report_date)

        if not missing:
            return (
                f"✅ All 9 sheds have submitted today's report."
            )

        reply = f"⚠️ Missing Shed Reports ({report_date})\n\n"

        for shed in missing:
            reply += f"• Shed {shed}\n"

        reply += f"\nTotal Missing : {len(missing)}"

        return reply
    
    elif intent == "get_missing_fields":

        report_date = get_report_date(data)

        result = get_missing_fields(report_date)

        if not result:
            return (
                f"✅ All 9 sheds have completed today's report."
            )

        reply = f"⚠️ Pending Report Fields ({report_date})\n\n"

        for shed in sorted(result.keys()):

            reply += f"🐔 Shed {shed}\n"

            for field in result[shed]:
                reply += f"• {field}\n"

            reply += "\n"

        return reply