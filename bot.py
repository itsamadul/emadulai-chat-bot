import os
import telebot
import requests
import base64
from keep_alive import keep_alive

# 🔑 Secrets
BOT_TOKEN = os.environ.get("TELEGRAM_DEMO_BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not BOT_TOKEN or not GEMINI_API_KEY:
    raise ValueError("❌ Please set TELEGRAM_DEMO_BOT_TOKEN and GEMINI_API_KEY in Secrets!")

bot = telebot.TeleBot(BOT_TOKEN)

# /start command
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 Hi! I am your Google Gemini Image Bot.\nUse /image <prompt> to generate images.")

# /image command
@bot.message_handler(commands=['image'])
def generate_image(message):
    prompt = message.text.replace("/image", "").strip()
    if not prompt:
        bot.reply_to(message, "👉 Example: /image A cute cat riding a skateboard in the rain")
        return

    bot.reply_to(message, "🎨 Generating image... Please wait...")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/image-bison-001:generateImage?key={GEMINI_API_KEY}"

    data = {
        "prompt": {
            "text": prompt
        },
        "image_size": "1024x1024"
    }

    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            image_base64 = result["candidates"][0]["content"]["image"]["b64"]
            image_bytes = base64.b64decode(image_base64)

            with open("gemini.png", "wb") as f:
                f.write(image_bytes)

            with open("gemini.png", "rb") as img:
                bot.send_photo(message.chat.id, img, caption=f"✅ Gemini generated: {prompt}")
        else:
            bot.reply_to(message, f"❌ API Error {response.status_code}: {response.text}")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {e}")

# Keep Alive + Start Bot
keep_alive()
bot.infinity_polling()
