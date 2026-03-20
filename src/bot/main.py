import logging
import os

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    filters,
    MessageHandler,
)

from data.cards import get_cards, get_matches

load_dotenv()
TOKEN = os.environ["TOKEN"]

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def init_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hello there! Search for cards using /find keyword",
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text: str = update.message.text
    response: str = f'You just typed "{text}"'
    await update.message.reply_text(response)


async def find_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # get keyword from user from /find keyword
    keyword = " ".join(context.args)
    if not keyword:
        await update.message.reply_text("Usage: /find keyword")
        return

    # get matches from card info json
    cards = get_cards()
    matches = get_matches(keyword, cards)

    # return matches as buttons
    if not matches:
        await update.message.reply_text("No matches")
        return

    keyboard = []

    for card in matches[:10]:
        if not card["color"]:
            button_text = card["name"]
        else:
            button_text = f"{card['name']} ({card['color']})"

        # callback the selected card's json
        button = InlineKeyboardButton(button_text, callback_data=card["unique_id"])
        row = [button]
        keyboard.append(row)

    await update.message.reply_text(
        f"Matches: {len(matches)}",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


def main():
    print("[bot.main.main] Starting bot...")
    app = ApplicationBuilder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("init", init_message))
    app.add_handler(CommandHandler("find", find_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Polling
    print("[bot.main.main] Polling...")
    app.run_polling()


if __name__ == "__main__":
    main()
