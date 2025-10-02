import telebot
import os
import requests
import base64
from keep_alive import keep_alive

# 🔑 Secrets থেকে লোড হবে
BOT_TOKEN = os.environ.get("TELEGRAM_DEMO_BOT_TOKEN")     # BotFather token
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")   # Gemini API key

bot = telebot.TeleBot(BOT_TOKEN)

# /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Hi! I am your Gemini Image Generator Bot.\n\nUse /image <prompt> to generate an image.")

# /image command
@bot.message_handler(commands=['image'])
def generate_image(message):
    prompt = message.text.replace("/image", "").strip()
    if not prompt:
        bot.reply_to(message, "👉 Example: /image A cat riding a bike in the moonlight")
        return

    bot.reply_to(message, "🎨 Generating image with Gemini... Please wait...")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/imagegeneration:generate?key={GEMINI_API_KEY}"

    data = {
        "prompt": {
            "text": prompt
        }
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        try:
            result = response.json()
            image_base64 = result["candidates"][0]["content"]["parts"][0]["inline_data"]["data"]
            image_bytes = base64.b64decode(image_base64)

            with open("gemini.png", "wb") as f:
                f.write(image_bytes)

            with open("gemini.png", "rb") as img:
                bot.send_photo(message.chat.id, img, caption=f"✅ Gemini generated: {prompt}")
        except Exception as e:
            bot.reply_to(message, f"⚠️ Error parsing Gemini response: {e}")
    else:
        bot.reply_to(message, f"❌ API Error {response.status_code}: {response.text}")

# ✅ Keep Alive + Start bot
keep_alive()
bot.infinity_polling()
