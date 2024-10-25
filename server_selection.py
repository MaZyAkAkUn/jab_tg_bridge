# server_selection.py

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    CommandHandler, MessageHandler, ConversationHandler,
    ContextTypes, filters
)
from account_manager import user_accounts
import logging

logger = logging.getLogger(__name__)

async def select_server(update: Update, context: ContextTypes.DEFAULT_TYPE):
    servers = ['jabber.org', 'example.com', 'custom']
    keyboard = [[s] for s in servers]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text('Select a server:', reply_markup=reply_markup)
    return 'GET_SERVER'

async def get_server(update: Update, context: ContextTypes.DEFAULT_TYPE):
    server = update.message.text
    if server == 'custom':
        await update.message.reply_text('Enter the server address:')
        return 'CUSTOM_SERVER'
    else:
        user_id = update.effective_user.id
        if user_id in user_accounts:
            user_accounts[user_id]['server'] = server
            await update.message.reply_text(f'Server set to {server}')
        else:
            await update.message.reply_text('Please add an account first.')
        return ConversationHandler.END

async def custom_server(update: Update, context: ContextTypes.DEFAULT_TYPE):
    server = update.message.text
    user_id = update.effective_user.id
    if user_id in user_accounts:
        user_accounts[user_id]['server'] = server
        await update.message.reply_text(f'Custom server set to {server}')
    else:
        await update.message.reply_text('Please add an account first.')
    return ConversationHandler.END

server_selection_handler = ConversationHandler(
    entry_points=[CommandHandler('select_server', select_server)],
    states={
        'GET_SERVER': [MessageHandler(filters.TEXT & ~filters.COMMAND, get_server)],
        'CUSTOM_SERVER': [MessageHandler(filters.TEXT & ~filters.COMMAND, custom_server)],
    },
    fallbacks=[]
)
