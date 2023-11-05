from telegram.ext import ContextTypes
import random
from zerotwobot import OWNER_ID, application, ALIVE_TEXT


async def send_alive(context: ContextTypes.DEFAULT_TYPE):
    try:
        await context.bot.send_message(-1001765891293, random.choice(ALIVE_TEXT))
    except:
        await context.bot.send_message(OWNER_ID, "Can't send alive message to group")
        raise

def main():
    job_queue = application.job_queue
    job_queue.run_repeating(send_alive, interval=30, first=10)
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
