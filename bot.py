import os
import telebot
import openai
import base64

BOT_TOKEN = os.environ.get("TELEGRAM_DEMO_BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 Hi! I am your OpenAI Image Generator Bot.\nUse /image <prompt> to generate images.")

@bot.message_handler(commands=['image'])
def generate_image(message):
    prompt = message.text.replace("/image", "").strip()
    if not prompt:
        bot.reply_to(message, "👉 Example: /image A cat riding a bike on the moon")
        return

    bot.reply_to(message, "🎨 Generating image... Please wait!")

    try:
        response = openai.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="512x512"
        )

        image_url = response.data[0].url

        bot.send_photo(message.chat.id, image_url, caption=f"✅ Generated Image: {prompt}")

    except Exception as e:
        bot.reply_to(message, f"❌ Error: {e}")

bot.infinity_polling()
