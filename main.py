import os
import telebot
import google.generativeai as genai
import time

# Получаем токены из переменных окружения
BOT_TOKEN = os.getenv('BOT_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Проверяем токены
if not BOT_TOKEN:
    print("ОШИБКА: BOT_TOKEN не найден")
    exit(1)
if not GEMINI_API_KEY:
    print("ОШИБКА: GEMINI_API_KEY не найден")
    exit(1)

# Инициализируем бота и Gemini
bot = telebot.TeleBot(BOT_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

print("=== НАСТРОЙКИ БОТА ===")
print(f"BOT_TOKEN: {BOT_TOKEN[:10]}...")
print(f"GEMINI_API_KEY: {GEMINI_API_KEY[:10]}...")

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🤖 Привет! Я бот с искусственным интеллектом Gemini.\n\nПросто напиши мне любой вопрос или сообщение, и я постараюсь помочь!")

# Обработчик всех текстовых сообщений
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        print(f"Получено сообщение от {message.from_user.first_name}: {message.text}")
        
        # Показываем, что бот печатает
        bot.send_chat_action(message.chat.id, 'typing')
        
        # Отправляем запрос в Gemini
        response = model.generate_content(message.text)
        
        # Отправляем ответ пользователю
        bot.reply_to(message, response.text)
        print("Ответ отправлен успешно")
        
    except Exception as e:
        error_msg = f"Произошла ошибка: {str(e)}"
        print(error_msg)
        bot.reply_to(message, "⚠️ Извините, произошла ошибка при обработке вашего запроса. Попробуйте позже.")

# Запускаем бота
if __name__ == "__main__":
    print("🔄 Ожидание 10 секунд перед запуском...")
    time.sleep(10)  # Ждем чтобы старые подключения разорвались
    
    print("🚀 Бот запускается...")
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        print("Перезапуск через 30 секунд...")
        time.sleep(30)