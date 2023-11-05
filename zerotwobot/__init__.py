"""
A python based modular telegram bot with anime theme
"""

__author__ = "Joker Hacker"
__version__ = "2.0.0-alpha"

import logging
import os
import platform
import sys
import time
import asyncio
import telegram.ext as tg
import random

from telegram.ext import Application
from telegram.error import BadRequest, Forbidden
from telegram import __bot_api_version__, __version__ as ptb_version
from pyrogram.client import Client
from dotenv import load_dotenv

#python version check
if sys.version_info[0] < 3 or sys.version_info[1] < 9:
    print(
        "You MUST have a python version of at least 3.9, exiting..."
    )
    quit(1)

load_dotenv() #load variables from .env files

LOGGER_LEVEL = os.environ.get("LOGGER_LEVEL", 20)
"logger level, `debug(10)`, `info(20)`, `warn(30)` and `error(40)`. default is `info`"

#setup logger
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=LOGGER_LEVEL
)

LOGGER = logging.getLogger(__name__)
"logger to use across the bot, use info, debug, warn and error"

BOT_VERSION = __version__
"zerotwo bot version"
PTB_VERSION = ptb_version
"`python-telegram-bot` library version"
BOT_API_VERSION = __bot_api_version__
"telegram bot API version"
PYTHON_VERSION = platform.python_version()
"installed python version"


#varibales used across the bot
TOKEN = os.environ.get("TOKEN", "")
"Telegram bot token obtained from botfather"
API_ID = os.environ.get("API_ID", "")
"API ID obtained from api.telegram.org"
API_HASH = os.environ.get("API_HASH", "")
"API HASH obtained from api.telegram.org"
OWNER_ID = int(os.environ.get("OWNER_ID", None)) # type:ignore
"Telegram ID of the bot owner"
OWNER_USERNAME = os.environ.get("OWNER_USERNAME", None)
"Telegram username of the bot owner, as `@username`"
JOIN_LOGGER = os.environ.get("JOIN_LOGGER", None)
"channel ID with `-` for keeping track of new chats where the bot gets added"
EVENT_LOGS = os.environ.get("EVENT_LOGS", None)
"channel ID with `-` for keeping track of gban, sudo and other"
SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", "")
"Support chat ID, where bot would say hi and hello."
try:
    DEV_USERS = set(int(x) for x in os.environ.get("DEV_USERS", "").split())
    "set of user ID which can have elevated privileges"
except ValueError:
    raise Exception("Your sudo users list does not contain valid integers.")

INFOPIC = bool(os.environ.get("INFOPIC", False))
"Picture to use for /start command, use pictures uploaded in telegraph"

# webhook stuff
WEBHOOK = bool(os.environ.get("WEBHOOK", False))
"True if you want to enable webhook"
URL = os.environ.get("URL", "")  # Does not contain token
PORT = int(os.environ.get("PORT", 5000))
CERT_PATH = os.environ.get("CERT_PATH")
WORKERS = int(os.environ.get("WORKERS", 8))
"number of workers to use, like thread."

LOAD = os.environ.get("LOAD", "").split()
"Modules to load, separate by space"
NO_LOAD = os.environ.get(
    "NO_LOAD", "translation rss cleaner connection math"
).split()
"Modules to not load, separate by space"
BAN_STICKER = os.environ.get(
    "BAN_STICKER",
    "CAACAgUAAxkBAAEDRNJhjolhBDkOeJLs2cPuhskKthnoQwACFwIAAs4DwFWTjimU8iDvqiIE",
)
"Sticker ID to use when banning a user"
TIME_API_KEY = os.environ.get("TIME_API_KEY", None)
WALL_API = os.environ.get("WALL_API", None)

DB_URI = os.environ.get("DATABASE_URL", " ")
"Postgresql database url in the format of ``postgresql://username:password@host:port/database`"

if DB_URI.startswith("postgres://"):
    DB_URI = DB_URI.replace("postgres://", "postgresql://")

TEMP_DOWNLOAD_LOC = os.environ.get("TEMP_DOWNLOAD_LOC", None)
"temperary download location, used in various modules"

try:
    BL_CHATS = set(int(x) for x in os.environ.get("BL_CHATS", "").split())
    "set of chat id to blacklist, where the bot won't join"
except ValueError:
    raise Exception("Your blacklisted chats list does not contain valid integers.")

ALIVE_TEXT = [
    "I'm not alone. I'm with you, Darling.",
    "I've got you, Darling. I won't let you go anymore.",
    "I've killed countless people. But I want to live with you.",
    "If I have to be a monster to be with you, so be it.",
    "I never knew a world without you in it, and I don't want to.",
    "I won't let them keep us apart. Not now, not ever.",
    "I'd forgotten so much. But I could never forget you.",
    "I want to be with you, even if it's just for a little while longer.",
    "Every moment with you is a treasure.",
    "Don't leave me alone, Darling.",
    "I want to be human, so I can be with you.",
    "The pain of being alone is something I never want to experience again.",
    "This is where I want to be, with you.",
    "When I'm with you, I feel so alive.",
    "You are my Darling. No one else's.",
    "I want to be the only one you need.",
    "You make me feel human.",
    "I never thought I'd find someone who understands me like you do.",
    "Even in the darkest times, you bring light into my life.",
    "I don't want to be alone anymore.",
    "Every day with you is a day worth living.",
    "I love you more than anything in this world.",
    "You are the most precious person to me.",
    "There's nothing I want more than to be with you.",
    "Life is better with you in it.",
    "I don't need anything else as long as I have you.",
    "I want to be where you are, always.",
    "I'll follow you to the ends of the earth, Darling.",
    "I don't care about the past. I just want a future with you.",
    "No matter what happens, I'll always come back to you.",
    "I want to create a world where we can be together.",
    "You're my reason for living.",
    "With you, every day feels like a new adventure.",
    "There's no place like home, and you are my home.",
    "When you're by my side, I can do anything.",
    "I will never let anyone hurt you.",
    "You're the one who gave me a reason to keep going.",
    "I've never felt more complete than when I'm with you.",
    "I can't imagine my life without you in it.",
    "I want to be by your side, always.",
    "You're my partner in crime, and I wouldn't have it any other way.",
    "You make the world a better place, just by being in it.",
    "You're the person I want to wake up to every morning.",
    "Our love is the most beautiful story ever told.",
    "I want to cherish every moment with you.",
    "With you, life is an endless journey of joy.",
    "I'm not perfect, but I'm perfect for you.",
    "I don't need a million things. I just need you.",
    "In your arms, I've found my paradise.",
    "I love you more than words can express."
]
"Some of the great words said by zero two, bot will be sending this once n hour in support chat"

DEV_USERS.add(OWNER_ID)

pyroclient = Client(
    "zerotwobot",
    API_ID,
    API_HASH,
    bot_token=TOKEN,
    no_updates= True
)

async def post_init(application: Application):
    try:
        await application.bot.sendMessage(-1001765891293, random.choice(ALIVE_TEXT))
    except Forbidden:
        LOGGER.warning(
            "Bot isn't able to send message to support_chat, go and check!",
        )
    except BadRequest as e:
        LOGGER.warning(e.message)


application = Application.builder().token(TOKEN).post_init(post_init).build()
asyncio.get_event_loop().run_until_complete(application.bot.initialize())
