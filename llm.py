import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)


model = genai.GenerativeModel(
    "gemini-3.1-flash-lite"
)

def translate_response(message, language):

    if language == "en":
        return message

    prompt = f"""
    Translate the following message into the language code '{language}'.

    Rules:
    - Keep all numbers exactly the same.
    - Preserve emojis.
    - Translate words like "Shed", "Produced", "Broken", "Sold", "Stock".
    - Do not change the shed number.
    - Return only the translated text.

    Message:
    {message}
    """

    response = model.generate_content(prompt)

    return response.text.strip()

def understand_message(message):

    prompt = f"""
        You are an egg farm management assistant.

        If the user wants to add production, broken, or sold eggs but does not specify a shed number, return:

        {{
            "intent":"add_production",
            "shed":null,
            "quantity":10,
            "date":"today", 
            "language":"en", 
            "unit":"egg"
        }}

        Do not guess the shed number.



        Convert the user message into JSON.

        User:
        11-07-2026 summary

        JSON:
        {{
            "intent":"get_daily_summary",
            "shed":null,
            "quantity":null,
            "date":"2026-07-11", 
            "language":"en", 
            "unit":"egg"
        }}

        User:
        11 July 2026 summary

        JSON:
        {{
        "intent":"get_daily_summary",
        "shed":null,
        "quantity":null,
        "date":"2026-07-11", 
        "language":"en" ,
        "unit":"egg"
        }}

        Possible intents:

        - add_production
        - add_broken
        - add_sold
        - get_summary
        - get_production
        - get_broken
        - get_sold
        - get_daily_summary
        - get_remaining
        - get_shed_count
        - get_farm_stock
        - get_total_broken
        - get_total_production
        - get_total_sold
        - get_total_remaining 
        - get_highest_production
        - get_highest_broken
        - get_highest_stock
        - get_highest_sold
        - get_lowest_production
        - get_lowest_broken
        - get_lowest_sold
        - get_lowest_stock
        - get_weekly_summary
        - get_monthly_summary
        - move_record
        - update_record
        - remove_record
        - delete_field
        - delete_record
        - add_birds
        - get_birds
        - get_total_birds
        - add_mortality
        - get_mortality
        - get_total_mortality
        - add_feed
        - get_feed
        - get_total_feed
        - get_total_live_birds
        - get_missing_sheds
        - get_missing_fields

        Return ONLY JSON.

        Required fields:

        intent
        shed
        from_shed
        to_shed
        field
        quantity
        date
        unit
        language

        Output unit:

        - If the user asks in eggs, return:
        "unit":"egg"

        - If the user asks in trays or tray, return:
        "unit":"tray"

        - If the user is adding production, broken or sold,
        always return:
        "unit":"egg"

        Important Rules:

        1. If the user mentions a shed number (e.g., Shed 1, Shed 2, first shed), use the shed-specific intents:
        - get_summary
        - get_production
        - get_broken
        - get_sold

        2. If the user does NOT mention any shed number and asks for today's summary, yesterday's summary, or a daily report, use:
        - get_daily_summary

        Examples:

        User:
        "Shed 1 produced 100 eggs"

        Note : 1 tray contains 30 eggs , when the user enters in trays , you need to convert those into eggs . For example , 10 trays = 10 * 30 = 300 days 
        
        
        JSON:
        {{
        "intent":"add_production",
        "shed":1,
        "quantity":100, 
        "language":"en" ,
        "unit":"egg"
        }}

        User:
        "100 eggs are added to first shed"

        JSON:
        {{
        "intent":"add_production",
        "shed":1,
        "quantity":100, 
        "language":"en" ,
        "unit":"egg"
        }}

        User:
        "How many broken eggs in shed 1?"
        JSON:
        {{
            "intent":"get_broken",
            "shed":1,
            "quantity":null,
            "date":null, 
            "language":"en", 
            "unit":"egg"
        }}

        User:
        "How many sold eggs in shed 2?"

        JSON:
        {{
            "intent":"get_sold",
            "shed":2,
            "quantity":null,
            "date":null, 
            "language":"en", 
            "unit":"egg"
        }}

        User:
        "How many eggs were produced in shed 3?"

        JSON:
        {{
            "intent":"get_production",
            "shed":3,
            "quantity":null,
            "date":null, 
            "language":"en", 
            "unit":"egg"
        }}

        User:
        Today's summary

        JSON:
        {{
            "intent":"get_daily_summary",
            "shed":null,
            "quantity":null,
            "date":"today", 
            "language":"en", 
            "unit":"egg"
        }}

        User:
        Yesterday's summary

        JSON:
        {{
            "intent":"get_daily_summary",
            "shed":null,
            "quantity":null,
            "date":"yesterday", 
            "language":"en", 
            "unit":"egg"
        }}

        User:
        Yesterday shed 1 summary

        JSON:
        {{
            "intent":"get_summary",
            "shed":1,
            "quantity":null,
            "date":"yesterday", 
            "language":"en", 
            "unit":"egg"
        }}

        User:
        Today shed 2 summary

        JSON:
        {{
            "intent":"get_summary",
            "shed":2,
            "quantity":null,
            "date":"today", 
            "language":"en", 
            "unit":"egg"
        }}

        User:
        Remaining eggs in shed 1

        JSON:
        {{
            "intent":"get_remaining",
            "shed":1,
            "quantity":null,
            "date":"today", 
            "language":"en", 
            "unit":"egg"
        }}

        User:
        Remaining eggs in shed 1 yesterday

        JSON:
        {{
            "intent":"get_remaining",
            "shed":1,
            "quantity":null,
            "date":"yesterday" ,
            "language":"en", 
            "unit":"egg"
        }}

        User:
        How many trays were produced in shed 2?

        JSON:
        {{
            "intent":"get_production",
            "shed":2,
            "quantity":null,
            "date":"today",
            "language":"en",
            "unit":"tray"
        }}

        User:
        How many eggs were produced in shed 2?

        JSON:
        {{
            "intent":"get_production",
            "shed":2,
            "quantity":null,
            "date":"today",
            "language":"en",
            "unit":"egg"
        }}

        User:
        Shed 2 produced 289.20 trays

        JSON:
        {{
            "intent":"add_production",
            "shed":2,
            "quantity":8690,
            "date":"today",
            "language":"en",
            "unit":"egg"
        }}

        User:
        How many sheds today?

        JSON:
        {{
            "intent":"get_shed_count",
            "shed":null,
            "quantity":null,
            "date":"today",
            "language":"en",
            "unit":"egg"
        }}

        User:
        How many sheds yesterday?

        JSON:
        {{
            "intent":"get_shed_count",
            "shed":null,
            "quantity":null,
            "date":"yesterday",
            "language":"en",
            "unit":"egg"
        }}

        User:
        Farm stock

        JSON:
        {{
            "intent":"get_farm_stock",
            "shed":null,
            "quantity":null,
            "date":"today",
            "language":"en",
            "unit":"egg"
        }}

        User:
        How many eggs are there today?

        JSON:
        {{
            "intent":"get_farm_stock",
            "shed":null,
            "quantity":null,
            "date":"today",
            "language":"en",
            "unit":"egg"
        }}

        User:
        Yesterday farm stock

        JSON:
        {{
            "intent":"get_farm_stock",
            "shed":null,
            "quantity":null,
            "date":"yesterday",
            "language":"en",
            "unit":"egg"
        }}

        User:
        How many broken eggs are there today?

        JSON:
        {{
            "intent":"get_total_broken",
            "shed":null,
            "quantity":null,
            "date":"today",
            "language":"en",
            "unit":"egg"
        }}

        User:
        Total broken eggs

        JSON:
        {{
            "intent":"get_total_broken",
            "shed":null,
            "quantity":null,
            "date":"today",
            "language":"en",
            "unit":"egg"
        }}

        User:
        Yesterday broken eggs

        JSON:
        {{
            "intent":"get_total_broken",
            "shed":null,
            "quantity":null,
            "date":"yesterday",
            "language":"en",
            "unit":"egg"
        }}

        User:
        How many eggs were produced today?

        {{
            "intent":"get_total_production",
            "shed":null,
            "quantity":null,
            "date":"today",
            "language":"en",
            "unit":"egg"
        }}

        User:
        11 July production

        JSON:
        {{
            "intent":"get_total_production",
            "shed":null,
            "quantity":null,
            "date":"2026-07-11",
            "language":"en",
            "unit":"egg"
        }}

        User:
        Production on 11-07-2026

        JSON:
        {{
            "intent":"get_total_production",
            "shed":null,
            "quantity":null,
            "date":"2026-07-11",
            "language":"en",
            "unit":"egg"
        }}

        User:
        How many sold eggs are there today?

        {{
            "intent":"get_total_sold",
            "shed":null,
            "quantity":null,
            "date":"today",
            "language":"en",
            "unit":"egg"
        }}

        User:
        How many remaining eggs are there?

        {{
            "intent":"get_total_remaining",
            "shed":null,
            "quantity":null,
            "date":"today",
            "language":"en",
            "unit":"egg"
        }}

        User:
        Which shed produced the most eggs today?

        JSON:
        {{
            "intent":"get_highest_production",
            "shed":null,
            "quantity":null,
            "date":"today",
            "language":"en",
            "unit":"egg"
        }}

        User:
        Highest production today

        JSON:
        {{
            "intent":"get_highest_production",
            "shed":null,
            "quantity":null,
            "date":"today",
            "language":"en",
            "unit":"egg"
        }}

        User:
        Which shed highest broken eggs today?
        {{
            "intent":"get_highest_broken",
            "shed":null,
            "quantity":null,
            "date":"today",
            "language":"en",
            "unit":"egg"
        }}

        User:
        Which shed has highest sold eggs ?
        {{
            "intent":"get_highest_sold",
            "shed":null,
            "quantity":null,
            "date":"today",
            "language":"en",
            "unit":"egg"
        }}

        User: 
        Which shed has highest stock today?
        {{
            "intent":"get_highest_stock",
            "shed":null,
            "quantity":null,
            "date":"today",
            "language":"en",
            "unit":"egg"
        }}

        User:
        which shed has lowest production ?
        {{
            "intent":"get_lowest_production",
            "shed":null,
            "quantity":null,
            "date":"today",
            "language":"en",
            "unit":"egg"
        }}

        User:
        which shed has lowest broken eggs ?
        {{
            "intent":"get_lowest_broken",
            "shed":null,
            "quantity":null,
            "date":"today",
            "language":"en",
            "unit":"egg"
        }}

        User:
        which shed has lowest sold eggs ?

        {{
            "intent":"get_lowest_sold",
            "shed":null,
            "quantity":null,
            "date":"today",
            "language":"en",
            "unit":"egg"
        }}

        User:
        which shed has lowest stock ?

        {{
            "intent":"get_lowest_stock",
            "shed":null,
            "quantity":null,
            "date":"today",
            "language":"en",
            "unit":"egg"
        }}

        User:
        Weekly summary / This week report . 

        {{
            "intent":"get_weekly_summary",
            "shed":null,
            "quantity":null,
            "date":"this_week",
            "language":"en",
            "unit":"egg"
        }}

        User:
        Last week report

        JSON:
        {{
            "intent":"get_weekly_summary",
            "shed":null,
            "quantity":null,
            "date":"last_week",
            "language":"en",
            "unit":"egg"
        }}

        User:
        Monthly summary / This month report / Last month Summary report . 

        {{
            "intent":"get_monthly_summary",
            "shed":null,
            "quantity":null,
            "date":"this_month",
            "language":"en",
            "unit":"egg"
        }}

        User:
        Move 100 produced eggs from shed 1 to shed 2

        JSON:
        {{
            "intent":"move_record",
            "from_shed":1,
            "to_shed":2,
            "field":"produced",
            "quantity":100,
            "date":"today",
            "language":"en",
            "unit":"egg"
        }}

        User:
        Move 5 broken eggs from shed 1 to shed 2

        JSON:
        {{
            "intent":"move_record",
            "from_shed":1,
            "to_shed":2,
            "field":"broken",
            "quantity":5,
            "date":"today",
            "language":"en",
            "unit":"egg"
        }}

        User:
        Move 20 sold eggs from shed 3 to shed 1

        JSON:
        {{
            "intent":"move_record",
            "from_shed":3,
            "to_shed":1,
            "field":"sold",
            "quantity":20,
            "date":"today",
            "language":"en",
            "unit":"egg"
        }}

        User:
        Change today's production of shed 1 to 500 eggs

        JSON:
        {{
            "intent":"update_record",
            "shed":1,
            "field":"produced",
            "quantity":500,
            "date":"today",
            "language":"en",
            "unit":"egg"
        }}

        User:
        Update yesterday's broken eggs in shed 2 to 15

        JSON:
        {{
            "intent":"update_record",
            "shed":2,
            "field":"broken",
            "quantity":15,
            "date":"yesterday",
            "language":"en",
            "unit":"egg"
        }}

        User:
        Set sold eggs in shed 3 to 40

        JSON:
        {{
            "intent":"update_record",
            "shed":3,
            "field":"sold",
            "quantity":40,
            "date":"today",
            "language":"en",
            "unit":"egg"
        }}

        User:
        Remove 20 eggs from today's production of shed 1

        JSON:
        {{
            "intent":"remove_record",
            "shed":1,
            "field":"produced",
            "quantity":20,
            "date":"today",
            "language":"en",
            "unit":"egg"
        }}

        User:
        Remove 5 broken eggs from shed 2

        JSON:
        {{
            "intent":"remove_record",
            "shed":2,
            "field":"broken",
            "quantity":5,
            "date":"today",
            "language":"en",
            "unit":"egg"
        }}

        User:
        Remove 10 sold eggs from shed 3 yesterday

        JSON:
        {{
            "intent":"remove_record",
            "shed":3,
            "field":"sold",
            "quantity":10,
            "date":"yesterday",
            "language":"en",
            "unit":"egg"
        }}

        User:
        Delete today's production of shed 1

        JSON:
        {{
            "intent":"delete_field",
            "shed":1,
            "field":"produced",
            "quantity":null,
            "date":"today",
            "language":"en",
            "unit":"egg"
        }}

        User:
        Delete broken eggs in shed 2

        JSON:
        {{
            "intent":"delete_field",
            "shed":2,
            "field":"broken",
            "quantity":null,
            "date":"today",
            "language":"en",
            "unit":"egg"
        }}

        User:
        Delete sold eggs in shed 3 yesterday

        JSON:
        {{
            "intent":"delete_field",
            "shed":3,
            "field":"sold",
            "quantity":null,
            "date":"yesterday",
            "language":"en",
            "unit":"egg"
        }}

        User:
        Delete today's shed 1 record

        JSON:
        {{
            "intent":"delete_record",
            "shed":1,
            "quantity":null,
            "date":"today",
            "language":"en",
            "unit":"egg"
        }}

        User:
        Shed 1 has 5000 birds

        JSON:
        {{
            "intent":"add_birds",
            "shed":1,
            "quantity":5000,
            "date":"today",
            "language":"en"
        }}
        User:
        Update shed 2 bird count to 4800

        JSON:
        {{
            "intent":"add_birds",
            "shed":2,
            "quantity":4800,
            "date":"today",
            "language":"en"
        }}
        User:
        Bird count in shed 1

        JSON:
        {{
            "intent":"get_birds",
            "shed":1,
            "quantity":null,
            "date":"today",
            "language":"en"
        }}
        User:
        Total birds today

        JSON:
        {{
            "intent":"get_total_birds",
            "shed":null,
            "quantity":null,
            "date":"today",
            "language":"en"
        }}

        User:
        5 birds died in shed 1

        JSON:
        {{
            "intent":"add_mortality",
            "shed":1,
            "quantity":5,
            "date":"today",
            "language":"en"
        }}

        User:
        Record 3 dead birds in shed 2

        JSON:
        {{
            "intent":"add_mortality",
            "shed":2,
            "quantity":3,
            "date":"today",
            "language":"en"
        }}

        User:
        Mortality in shed 1

        JSON:
        {{
            "intent":"get_mortality",
            "shed":1,
            "quantity":null,
            "date":"today",
            "language":"en"
        }}

        User:
        Today's mortality

        JSON:
        {{
            "intent":"get_total_mortality",
            "shed":null,
            "quantity":null,
            "date":"today",
            "language":"en"
        }}

        User:
        Add 500 kg feed to shed 1

        JSON:
        {{
            "intent":"add_feed",
            "shed":1,
            "quantity":500,
            "date":"today",
            "language":"en",
            "unit":"kg"
        }}

        User:
        Shed 2 consumed 450 kg feed

        JSON:
        {{
            "intent":"add_feed",
            "shed":2,
            "quantity":450,
            "date":"today",
            "language":"en",
            "unit":"kg"
        }}

        User:
        Feed in shed 1

        JSON:
        {{
            "intent":"get_feed",
            "shed":1,
            "quantity":null,
            "date":"today",
            "language":"en",
            "unit":"kg"
        }}

        User:
        Today's feed

        JSON:
        {{
            "intent":"get_total_feed",
            "shed":null,
            "quantity":null,
            "date":"today",
            "language":"en",
            "unit":"kg"
        }}

        User:
        Today's live birds

        JSON:
        {{
            "intent":"get_total_live_birds",
            "shed":null,
            "quantity":null,
            "date":"today",
            "language":"en"
        }}

        User:
        Total live birds

        JSON:
        {{
            "intent":"get_total_live_birds",
            "shed":null,
            "quantity":null,
            "date":"today",
            "language":"en"
        }}

        User:
        How many live birds are there?

        JSON:
        {{
            "intent":"get_total_live_birds",
            "shed":null,
            "quantity":null,
            "date":"today",
            "language":"en"
        }}

        User:
        Today's missing sheds

        JSON:
        {{
            "intent":"get_missing_sheds",
            "shed":null,
            "quantity":null,
            "date":"today",
            "language":"en"
        }}
        User:
        Missing sheds

        JSON:
        {{
            "intent":"get_missing_sheds",
            "shed":null,
            "quantity":null,
            "date":"today",
            "language":"en"
        }}
        User:
        Which sheds have not reported today?

        JSON:
        {{
            "intent":"get_missing_sheds",
            "shed":null,
            "quantity":null,
            "date":"today",
            "language":"en"
        }}
        User:
        Pending sheds

        JSON:
        {{
            "intent":"get_missing_sheds",
            "shed":null,
            "quantity":null,
            "date":"today",
            "language":"en"
        }}

        User:
        Today's pending fields

        JSON:
        {{
            "intent":"get_missing_fields",
            "shed":null,
            "quantity":null,
            "date":"today",
            "language":"en"
        }}
        User:
        Incomplete shed reports

        JSON:
        {{
            "intent":"get_missing_fields",
            "shed":null,
            "quantity":null,
            "date":"today",
            "language":"en"
        }}
        User:
        Which sheds have incomplete data?

        JSON:
        {{
            "intent":"get_missing_fields",
            "shed":null,
            "quantity":null,
            "date":"today",
            "language":"en"
        }}

        Now convert this:

        {message}
        """
    response = model.generate_content(prompt)

    text = response.text.strip()

    # Remove markdown if present
    text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)