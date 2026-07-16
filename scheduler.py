import asyncio
from datetime import date

from apscheduler.schedulers.background import BackgroundScheduler
from telegram import Bot

from config import TELEGRAM_BOT_TOKEN
from service import generate_daily_reminder


BOT_TOKEN = TELEGRAM_BOT_TOKEN

# Replace with your Telegram chat ID
CHAT_ID = -1004484451785

bot = Bot(token=BOT_TOKEN)


async def send_daily_reminder():
    print("Running reminder...")

    report_date = str(date.today())

    message = generate_daily_reminder(report_date)

    if message:

        await bot.send_message(
            chat_id=CHAT_ID,
            text=message
        )

        print("✅ Daily reminder sent successfully.")

    else:

        print("No reminder to send.")


def run_daily_reminder():

    asyncio.run(send_daily_reminder())


scheduler = BackgroundScheduler()

scheduler.add_job(
    run_daily_reminder,
    trigger="cron",
    hour=18,
    minute=30
)

scheduler.start()

print("✅ Reminder scheduler started. Daily reminder will be sent at 7:00 PM.")

print("✅ Scheduler Started...")