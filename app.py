from bot import start_bot
from database import create_database
import scheduler
if __name__ == "__main__":

    create_database()

    start_bot()