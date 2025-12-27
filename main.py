import telebot
import google.generativeai as genai
import os
from flask import Flask
from threading import Thread

# ==========================================
# CONFIGURATION
# We get keys from the Server Environment Variables for security
# ==========================================
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
# Note: Ensure the model name is correct. Standard is "gemini-1.5-flash"
model = genai.GenerativeModel("gemini-1.5-flash") 

# Initialize Bot
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# ==========================================
# FLASK SERVER (TO KEEP BOT ALIVE)
# ==========================================
app = Flask('')

@app.route('/')
def home():
    return "I am alive!"

def run_http():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_http)
    t.start()

# ==========================================
# BOT COMMANDS
# ==========================================
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 Hi! I am a 24/7 AI bot powered by Gemini. Ask me anything!")

@bot.message_handler(func=lambda message: True)
def ai_reply(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        response = model.generate_content(
            message.text,
            generation_config={"max_output_tokens": 500}
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "⚠ AI Error. Try again later.")
        print(f"Error: {e}")

# ==========================================
# MAIN EXECUTION
# ==========================================
if __name__ == "__main__":
    print("✅ Bot is starting...")
    keep_alive()  # Start the fake web server
    bot.infinity_polling() # Start the bot