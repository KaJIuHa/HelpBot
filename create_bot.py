from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
TOKEN = os.getenv('TOKEN')
CHAT = os.getenv('ADMIN_CHAT')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_IP = os.getenv('DB_IP')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
PAY_TOKEN = os.getenv('PAY_TOKEN')
storage = MemoryStorage()



bot = Bot(token=TOKEN,parse_mode='html')
dp = Dispatcher(bot, storage=storage)
