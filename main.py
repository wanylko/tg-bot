import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import yt_dlp

TOKEN = os.getenv("BOT_TOKEN")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    if "soundcloud.com" not in url:
        await update.message.reply_text("Пришли ссылку SoundCloud")
        return

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "song.%(ext)s",
        "quiet": True
    }

    await update.message.reply_text("Скачиваю...")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    await update.message.reply_audio(audio=open(filename, "rb"))

app = Application.builder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
