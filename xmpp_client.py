# xmpp_client.py

import slixmpp
import logging

logger = logging.getLogger(__name__)

class XMPPClient(slixmpp.ClientXMPP):
    def __init__(self, jid, password, bot, chat_id):
        super().__init__(jid, password)
        self.bot = bot
        self.chat_id = chat_id
        self.add_event_handler('session_start', self.start)
        self.add_event_handler('message', self.message)

    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        logger.info('XMPP session started')

    async def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            sender = str(msg['from'])
            body = msg['body']
            await self.bot.send_message(chat_id=self.chat_id,
                                        text=f"From {sender}: {body}")

    def send_xmpp_message(self, to_jid, message_body):
        self.send_message(mto=to_jid, mbody=message_body, mtype='chat')
