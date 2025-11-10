import os
import telebot
import google.generativeai as genai
import http.server
import socketserver
import threading

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

# Простой HTTP-сервер для Render
class SimpleHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Bot is running!')

def run_http_server():
    with socketserver.TCPServer(("", 5000), SimpleHandler) as httpd:
        print("HTTP сервер запущен на порту 5000")
        httpd.serve_forever()

# Запускаем HTTP-сервер в отдельном потоке
http_thread = threading.Thread(target=run_http_server)
http_thread.daemon = True
http_thread.start()

print("🚀 Бот запущен!")
bot.infinity_polling()