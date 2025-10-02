import os
import telebot
import requests
import base64
from keep_alive import keep_alive

BOT_TOKEN = os.environ.get("TELEGRAM_DEMO_BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 Hi! I am your Gemini Image Generator Bot.\nUse /image <prompt> to generate images.")

@bot.message_handler(commands=['image'])
def generate_image(message):
    prompt = message.text.replace("/image", "").strip()
    if not prompt:
        bot.reply_to(message, "👉 Example: /image A cute cat riding a bike on the moon")
        return

    bot.reply_to(message, "🎨 Generating image... Please wait...")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/image-bison-001:generateImage?key={GEMINI_API_KEY}"

    data = {
        "prompt": {
            "text": prompt
        },
        "image_size": "1024x1024"
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        result = response.json()
        try:
            image_base64 = result["candidates"][0]["content"]["image"]["b64"]
            image_bytes = base64.b64decode(image_base64)

            with open("gemini.png", "wb") as f:
                f.write(image_bytes)

            with open("gemini.png", "rb") as img:
                bot.send_photo(message.chat.id, img, caption=f"✅ Gemini generated: {prompt}")
        except:
            bot.reply_to(message, "⚠️ Error parsing Gemini response")
    else:
        bot.reply_to(message, f"❌ API Error {response.status_code}: {response.text}")

keep_alive()
bot.infinity_polling()
