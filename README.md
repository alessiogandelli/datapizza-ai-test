# Template project Python Data Science using poetry

!!!
this is a project template, you can use this template clicking on the green button "use this template" on the top right of the page, this will create your repo with this structure 
!!!



install poetry [here](https://python-poetry.org/docs/#installing-with-the-official-installer)


## create the virtual environment and install the dependencies

```bash
poetry env use python3.12
```

```bash
poetry install
```

## activate the virtual environment

```bash
poetry shell
```

now you created an isolated enviroment, everything you install will not affect your system python installation, you can experiment freely and delete the .venv folder to start over. 
(if you cannot find the .env folder )


## install a new package

```bash
poetry add <package_name>
```
what you usually do with ```pip install pandas``` is now ```poetry add pandas```

## using .env file

if you have to handle sensitive data put it in the ```.env ```file, it will be ignored by git and you can access it with ```os.getenv('VARIABLE_NAME')```

### Required Environment Variables

Create a `.env` file in the project root with:

```
OPENAI_API_KEY=your_openai_api_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
```

To get a Telegram bot token:
1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Send `/newbot` and follow the instructions
3. Copy the token to your `.env` file

## Running the Application

### Terminal Chatbot (Console)
```bash
poetry run python main.py
```

### Telegram Bot Frontend
```bash
poetry run python run_telegram_bot.py
```

Or directly:
```bash
poetry run python -m src.telegram_bot
```


## suggestion 
open the folder with vscode and you should see 
```#%%``` lines, these are the cell division, you can run a cell with ```shift+enter``` or pressing the play button on the left of the cell.



if something breaks reclone the repo and start over, it's a good practice to have a clean environment to work with.

```bash