"""
Telegram Bot Frontend for StudyBuddy
Provides a clean, minimal Telegram interface for the chatbot.
"""
import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from datapizza.memory import Memory
from datapizza.type import ROLE, TextBlock
from datapizza.agents import Agent
from src import client
from src.agent_calendar import calendar_agent

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Store user sessions (memory per user)
user_sessions = {}


def get_or_create_session(user_id: int):
    """Get or create a memory session for a user."""
    if user_id not in user_sessions:
        memory = Memory()
        agent = Agent(
            name="studybuddy",
            system_prompt="You are a helpful study assistant for university students.",
            client=client,
            memory=memory,
        )
        agent.can_call(calendar_agent)
        user_sessions[user_id] = {
            'memory': memory,
            'agent': agent
        }
    return user_sessions[user_id]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_text(
        f"Hello {user.first_name}! 👋\n\n"
        "I'm your StudyBuddy assistant. I can help you with:\n"
        "• Study questions and concepts\n"
        "• Calendar management\n"
        "• Planning your schedule\n\n"
        "Just send me a message to get started!\n\n"
        "Commands:\n"
        "/start - Show this message\n"
        "/reset - Clear conversation history"
    )


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Clear the user's conversation history."""
    user_id = update.effective_user.id
    if user_id in user_sessions:
        del user_sessions[user_id]
    await update.message.reply_text(
        "✅ Conversation history cleared! Let's start fresh."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages."""
    user_id = update.effective_user.id
    user_message = update.message.text
    
    # Get or create session for this user
    session = get_or_create_session(user_id)
    agent = session['agent']
    memory = session['memory']
    
    # Show typing indicator
    await update.message.chat.send_action("typing")
    
    try:
        # Get AI response
        response = agent.run(user_message)
        
        # Update conversation memory
        memory.add_turn(TextBlock(content=user_message), role=ROLE.USER)
        memory.add_turn(response.content, role=ROLE.ASSISTANT)
        
        # Send response
        await update.message.reply_text(response.text)
        
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        await update.message.reply_text(
            "Sorry, I encountered an error processing your message. Please try again."
        )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors caused by updates."""
    logger.error(f"Update {update} caused error {context.error}")


def run_telegram_bot():
    """Start the Telegram bot."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not token:
        raise ValueError(
            "TELEGRAM_BOT_TOKEN not found in environment variables.\n"
            "Please set it in your .env file or environment."
        )
    
    # Create the Application
    application = Application.builder().token(token).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("reset", reset))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)
    
    # Start the bot
    logger.info("Starting Telegram bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    run_telegram_bot()
