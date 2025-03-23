import telebot
from datetime import datetime
from dotenv import load_dotenv
import os

LOG_DIR = os.getenv("LOG_DIR") or "logs"
load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

def get_monthly_log_file():
	now = datetime.now()
	year = now.year
	month = now.month

	os.makedirs(LOG_DIR, exist_ok=True)
	log_file = os.path.join(LOG_DIR, f"{year}_{month}.md")
	# Crear archivo de log si no existe
	if not os.path.exists(log_file):
		with open(log_file, "w") as file:
			file.write(f"# Registro de mensajes - Año: {year}, mes: {month}\n")
	return log_file

def log_msg(message, cat = "INFO"):
	log_file = get_monthly_log_file()
	with open(log_file, "a") as file:
		timestamp = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
		file.write(f"\n{timestamp}\t{cat}\t{message.text}")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Welcome to the bot!")

@bot.message_handler(func=lambda m: True)
def echo_and_log(message):
	log_msg(message)
	bot.reply_to(message, f"msg guardado")

if __name__ == '__main__':
	print('Bot is running...')
	bot.polling(none_stop=True)