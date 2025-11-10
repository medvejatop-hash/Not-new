import os
import telebot
import google.generativeai as genai

BOT_TOKEN = os.getenv('BOT_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

bot = telebot.TeleBot(BOT_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот с ИИ Gemini. Напиши мне что-нибудь!")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {str(e)}")

# Вместо infinity_polling используем удаление webhook и запуск polling
if __name__ == "__main__":
    bot.remove_webhook()
    print("Бот запущен...")
    bot.infinity_polling()