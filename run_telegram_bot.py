#!/usr/bin/env python3
"""
Entry point for running the Telegram bot frontend.
"""

if __name__ == "__main__":
    from src.telegram_bot import TelegramBot

    bot = TelegramBot()
    bot.run()
