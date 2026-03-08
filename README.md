# FAB Scraper Bot

Searches the online market for the cheapest Flesh and Blood cards and notifies you via Telegram.

## Installation


Clone this repository.

```
git clone
```

Create a new bot in Telegram by adding @BotFather, set the bot username, and copy the API token.

Create the file `.env` in the project root directory and paste the following content:

```
TOKEN = "<your_api_token>"
```

Install dependencies and run the bot.

```
uv sync
uv pip install -e .
uv run bot
```

In Telegram, add the bot by searching for its username.

Type something in the chat and it should reply to you.
