# messaging.py

from telegram import Update
from telegram.ext import ContextTypes
import logging
from xmpp_client import XMPPClient
from account_manager import user_accounts

logger = logging.getLogger(__name__)

async def set_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    contact_jid = ' '.join(context.args)
    if user_id in user_accounts:
        user_accounts[user_id]['current_contact'] = contact_jid
        await update.message.reply_text(f'Current contact set to {contact_jid}')
    else:
        await update.message.reply_text('Please add an account first.')

async def send_message_to_xmpp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    account = user_accounts.get(user_id)
    if account and 'xmpp_client' in account:
        message_body = update.message.text
        contact_jid = account.get('current_contact')
        if contact_jid:
            account['xmpp_client'].send_xmpp_message(contact_jid, message_body)
            await update.message.reply_text('Message sent.')
        else:
            await update.message.reply_text('Set a contact using /set_contact')
    else:
        await update.message.reply_text('You are not connected.')
