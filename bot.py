from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters
)

from config import TELEGRAM_BOT_TOKEN
from llm import understand_message, translate_response 
from service import process_request

from telegram.constants import ParseMode

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # print("CHAT ID:", update.effective_chat.id)
    message = update.message.text

    print("Received:", message)

    try:
        data = understand_message(message)
        
        print("LLM Output:", data)

        reply = process_request(data)

        language = data.get("language", "en")

        reply = translate_response(
            reply,
            language
        )

        await update.message.reply_text(reply ,parse_mode=ParseMode.MARKDOWN)

    except Exception as e:
        print(e)
        await update.message.reply_text(
            f"Error: {e}"
        )


def start_bot():

    app = (
        Application.builder()
        .token(TELEGRAM_BOT_TOKEN)
        .build()
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    print("Bot is running...")

    app.run_polling()