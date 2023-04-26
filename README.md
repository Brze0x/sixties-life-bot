# Sixties-life News Bot
This is a Telegram bot that provides news updates to users. It supports multiple news sources and allows users to customize their settings.

## Getting Started
#### Prerequisites
To run the bot, you'll need the following software installed on your machine:
- Python 3.9+

#### Installation
- Clone this repository:
```
git clone https://github.com/your-username/news-bot.git
```
- Install the required Python packages:
```
pip install -r requirements.txt
```

#### Usage
- Create a token using `@BotFather` in telegram
- Create a `.env` file in the main directory and add the received token there:
```
BOT_TOKEN = '7775588:HV8QQ3dnLfqSf4'
```
- To start the bot, run the following command:
```
python main.py
```

Once the bot is running, users can interact with it by sending messages to its Telegram handle.
## Commands
The bot supports the following commands:
- `/start`: Starts the bot and displays the main menu.

## Features
The bot has the following features:
- Supports multiple news sources.
- Allows users to customize their news settings.
- Implements pagination to avoid flooding users with too many messages.

## License
This project is licensed under the MIT License
