import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    filters,
    MessageHandler,
)

load_dotenv()
TOKEN = os.environ["TOKEN"]

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def init_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Bot initiated!"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text: str = update.message.text
    response: str = f'You just typed "{text}"'
    await update.message.reply_text(response)


def main():
    print("Starting bot...")
    app = ApplicationBuilder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("init", init_message))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Polling
    print("Polling...")
    app.run_polling()


if __name__ == "__main__":
    main()
