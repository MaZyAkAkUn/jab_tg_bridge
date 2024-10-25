# bot.py
from dotenv import dotenv_values
config = dotenv_values(".env")  # config = {"USER": "foo", "EMAIL": "foo@example.org"}


import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ConversationHandler, ContextTypes, filters
)
from account_manager import (
    add_account, get_jid, get_password, create_account,
    create_jid, create_password, add_account_handler, create_account_handler
)
from contacts_manager import (
    add_contact, remove_contact, list_contacts
)
from messaging import (
    send_message_to_xmpp, set_contact
)
from xmpp_client import XMPPClient
from connection_manager import connect, disconnect
from server_selection import (
    select_server, get_server, custom_server, server_selection_handler
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory user accounts store
user_accounts = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Welcome to the XMPP Bridge Bot!')

def main():
    TOKEN =config['BOT_API_TOKEN']  # Replace with your bot's token
    app = ApplicationBuilder().token(TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler('start', start))

    # Account management handlers
    app.add_handler(add_account_handler)
    app.add_handler(create_account_handler)

    # Server selection handler
    app.add_handler(server_selection_handler)

    # Connection handlers
    app.add_handler(CommandHandler('connect', connect))
    app.add_handler(CommandHandler('disconnect', disconnect))

    # Messaging handlers
    app.add_handler(CommandHandler('set_contact', set_contact))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,
                                   send_message_to_xmpp))

    # Contacts management handlers
    app.add_handler(CommandHandler('add_contact', add_contact))
    app.add_handler(CommandHandler('remove_contact', remove_contact))
    app.add_handler(CommandHandler('list_contacts', list_contacts))

    app.run_polling()

if __name__ == '__main__':
    main()
