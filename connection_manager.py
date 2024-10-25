# connection_manager.py

from telegram import Update
from telegram.ext import ContextTypes
import logging
from xmpp_client import XMPPClient
from account_manager import user_accounts

logger = logging.getLogger(__name__)

async def connect(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    account = user_accounts.get(user_id)
    if account:
        jid = account['jid']
        password = account['password']
        server = account.get('server')
        bot = context.bot
        chat_id = update.effective_chat.id
        xmpp_client = XMPPClient(jid, password, bot, chat_id)
        if server:
            await xmpp_client.connect(address=(server, 5222))
        else:
            await xmpp_client.connect()
        xmpp_client.process(forever=False)
        account['xmpp_client'] = xmpp_client
        await update.message.reply_text('Connected to XMPP server.')
    else:
        await update.message.reply_text('Please add an account first.')

async def disconnect(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    account = user_accounts.get(user_id)
    if account and 'xmpp_client' in account:
        account['xmpp_client'].disconnect()
        del account['xmpp_client']
        await update.message.reply_text('Disconnected from XMPP server.')
    else:
        await update.message.reply_text('You are not connected.')
