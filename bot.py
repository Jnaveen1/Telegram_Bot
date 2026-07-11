from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters
from config import TELEGRAM_BOT_TOKEN
from database import add_production, add_broken, add_sold

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message = update.message.text.lower()

    print("Received:", message)


    words = message.split()


    shed_no = int(words[1])

    quantity = int(words[3])


    if "produced" in message:

        add_production(
            shed_no,
            quantity
        )

        reply = f"Shed {shed_no}: Added production {quantity} eggs"


    elif "broken" in message:

        add_broken(
            shed_no,
            quantity
        )

        reply = f"Shed {shed_no}: Added broken eggs {quantity}"


    elif "sold" in message:

        add_sold(
            shed_no,
            quantity
        )

        reply = f"Shed {shed_no}: Added sold eggs {quantity}"


    else:

        reply = "I don't understand this format yet."


    await update.message.reply_text(reply)
    message = update.message.text.lower()

    print("Received:", message)

    if "produced" in message:

        words = message.split()

        shed_no = int(words[1])

        quantity = int(words[3])

        add_production(
            shed_no,
            quantity
        )

        await update.message.reply_text(
            f"Shed {shed_no}: Added production of {quantity} eggs"
        )

    else:

        await update.message.reply_text(
            "I don't understand this format yet."
        )
    message = update.message.text

    print("Received:", message)

    await update.message.reply_text(
        "I received your message: " + message
    )


def start_bot():

    app = Application.builder().token(
        TELEGRAM_BOT_TOKEN
    ).build()


    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )


    print("Bot is running...")

    app.run_polling()