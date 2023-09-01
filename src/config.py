import os
from pathlib import Path

from aiogram import Bot
from decouple import config

ROOT = Path(__file__).parent.parent

BOT_TOKEN = config('BOT_TOKEN')
REDIS_STATE_DB_NUMBER = config('REDIS_STATE_DB', cast=int)
REDIS_MAIN_DB_NUMBER = config('REDIS_MAIN_DB', cast=int)
REDIS_MAIN_DB_URL = f'redis://localhost/{REDIS_MAIN_DB_NUMBER}'


TMP_DIR = os.path.join(ROOT, 'tmp')
if not os.path.exists(TMP_DIR):
    os.makedirs(TMP_DIR)


bot = Bot(token=BOT_TOKEN, parse_mode='HTML')

CHAT_ID = config('CHAT_ID')

NOTIFICATION_MINUTES = 120
