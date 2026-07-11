from database import (
    add_production,
    add_broken,
    add_sold, 
    get_summary
)


def process_request(data):

    intent = data["intent"]
    shed = data["shed"]
    if intent == "add_production":
        quantity = data["quantity"]
        add_production(shed, quantity)
        return f"✅ Added {quantity} produced eggs to Shed {shed}"

    elif intent == "add_broken":
        quantity = data["quantity"]
        add_broken(shed, quantity)
        return f"✅ Recorded {quantity} broken eggs in Shed {shed}"

    elif intent == "add_sold":
        quantity = data["quantity"]
        add_sold(shed, quantity)
        return f"✅ Recorded {quantity} sold eggs from Shed {shed}"

    elif intent == "get_summary":
        record = get_summary(shed)

        if record is None:
            return f"No data found for Shed {shed} today."

        stock = record.produced - record.broken - record.sold

        return (
            f"📊 Shed {shed} Summary\n\n"
            f"Produced: {record.produced}\n"
            f"Broken: {record.broken}\n"
            f"Sold: {record.sold}\n"
            f"Stock: {stock}"
        )
    
    elif intent == "get_broken":

        record = get_summary(shed)

        if record is None:
            return f"No data found for Shed {shed} today."

        return (
            f"Shed {shed} has "
            f"{record.broken} broken eggs today."
        )
    
    elif intent == "get_sold":

        record = get_summary(shed)

        if record is None:
            return f"No data found for Shed {shed} today."

        return (
            f"Shed {shed} has "
            f"{record.sold} sold eggs today."
        )
    
    elif intent == "get_production":

        record = get_summary(shed)

        if record is None:
            return f"No data found for Shed {shed} today."

        return (
            f"Shed {shed} produced "
            f"{record.produced} eggs today."
        )

    else:
        return "Unknown operation."