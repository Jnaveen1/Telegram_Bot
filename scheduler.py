from datetime import date
from apscheduler.schedulers.background import BackgroundScheduler

from service import generate_daily_reminder
from telegram import Bot
from config import TELEGRAM_BOT_TOKEN

BOT_TOKEN = TELEGRAM_BOT_TOKEN
CHAT_ID = "YOUR_CHAT_ID"

bot = Bot(token=BOT_TOKEN)


def send_daily_reminder():

    today = str(date.today())

    message = generate_daily_reminder(today)

    if message:
        bot.send_message(
            chat_id=CHAT_ID,
            text=message
        )


scheduler = BackgroundScheduler()

scheduler.add_job(
    send_daily_reminder,
    "cron",
    hour=19,
    minute=0
)

scheduler.start()