"""
Telegram Bot Frontend for StudyBuddy
Provides a clean, minimal Telegram interface for the chatbot.
Handles only Telegram-specific functionality.
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
from src.chatbot import ChatbotManager

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class TelegramBot:
    """
    Telegram Bot class for managing the bot lifecycle and handlers.
    
    This class encapsulates all bot-related functionality including:
    - Bot initialization and configuration
    - Command handlers (/start, /reset)
    - Message handlers
    - Error handling
    """
    
    def __init__(self, token: str = None):
        """
        Initialize the Telegram bot.
        
        Args:
            token: Telegram bot token. If not provided, will attempt to read from
                   TELEGRAM_BOT_TOKEN environment variable.
        
        Raises:
            ValueError: If token is not provided and not found in environment.
        """
        self.token = token or os.getenv("TELEGRAM_BOT_TOKEN")
        
        if not self.token:
            raise ValueError(
                "TELEGRAM_BOT_TOKEN not found in environment variables.\n"
                "Please set it in your .env file or environment."
            )
        
        self.chatbot_manager = ChatbotManager()
        self.application = None
        logger.info("TelegramBot initialized successfully")
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    
    async def reset_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Clear the user's conversation history."""
        user_id = update.effective_user.id
        self.chatbot_manager.reset_session(str(user_id))
        await update.message.reply_text(
            "✅ Conversation history cleared! Let's start fresh."
        )
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming messages."""
        user_id = update.effective_user.id
        user_message = update.message.text
        
        # Show typing indicator
        await update.message.chat.send_action("typing")
        
        try:
            # Get response from chatbot manager
            response = self.chatbot_manager.get_response(str(user_id), user_message)
            
            # Send response
            await update.message.reply_text(response)
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            await update.message.reply_text(
                "Sorry, I encountered an error processing your message. Please try again."
            )
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Log errors caused by updates."""
        logger.error(f"Update {update} caused error {context.error}")
    
    def setup_handlers(self):
        """Register all command and message handlers."""
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("reset", self.reset_command))
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )
        self.application.add_error_handler(self.error_handler)
        logger.info("Handlers registered successfully")
    
    def run(self):
        """
        Start the Telegram bot.
        
        Creates the application, registers handlers, and starts polling for updates.
        """
        # Create the Application
        self.application = Application.builder().token(self.token).build()
        
        # Register handlers
        self.setup_handlers()
        
        # Start the bot
        logger.info("Starting Telegram bot polling...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)
    
    def stop(self):
        """Stop the bot gracefully."""
        if self.application:
            logger.info("Stopping Telegram bot...")
            self.application.stop()


