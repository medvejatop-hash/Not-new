import os
import telebot
import google.generativeai as genai
import threading
from flask import Flask

# Получаем токены
BOT_TOKEN = os.getenv('BOT_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Инициализируем бота и Gemini
bot = telebot.TeleBot(BOT_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Обработчики сообщений
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🤖 Привет! Я новый бот с ИИ Gemini. Работаю!")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {str(e)}")

# Простой веб-сервер для Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    app.run(host='0.0.0.0', port=5000, debug=False)

# Запускаем веб-сервер в отдельном потоке
web_thread = threading.Thread(target=run_web)
web_thread.daemon = True
web_thread.start()

print("🚀 Бот запущен!")
bot.infinity_polling()