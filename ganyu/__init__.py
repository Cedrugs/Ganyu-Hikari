from utils.json import *
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from glob import glob


import lightbulb
import hikari
import logging
import asyncio


logger = logging.getLogger(__name__)
extensions_path = [x.split('\\')[-1][:-3] for x in [x.split('/')[-1] for x in glob("ganyu/extensions/*.py")]]


class Extension(object):

    def __init__(self):
        for ext in extensions_path:
            setattr(self, ext, False)

    def ready_up(self, extension):
        setattr(self, extension, True)

    def all_ready(self):
        return all([getattr(self, ext) for ext in extensions_path if ext])


# noinspection PyAbstractClass
class Ganyu(lightbulb.BotApp):

    def __init__(self):
        self._ready = False
        self._extension_ready = Extension
        self.startup_time = None
        self.mongo = AsyncIOMotorClient(read_json('config.json')['mongodbConnection'])

        intents = (
            hikari.Intents.GUILDS
            | hikari.Intents.ALL_MESSAGE_REACTIONS
            | hikari.Intents.ALL_MESSAGES
            | hikari.Intents.GUILD_MEMBERS
        )

        token = read_json('config.json')['token']
        owner_ids = read_json('config.json')['teamId']

        super().__init__(
            token=token,
            owner_ids=owner_ids,
            prefix='>',
            intents=intents
        )

    def build(self):

        self.subscribe(hikari.StartingEvent, self.on_starting)
        self.subscribe(hikari.StartedEvent, self.on_started)
        self.subscribe(lightbulb.CommandInvocationEvent, self.on_message)

        self.setup_extensions()

        self.run(activity=hikari.Activity(
                name='>help | Running on lightbulb hikari',
                type=hikari.ActivityType.PLAYING)
        )

    def setup_extensions(self):
        if not extensions_path:
            logger.info('No extensions to load')
        for ext in extensions_path:
            try:
                self.load_extensions(f'ganyu.extensions.{ext}')
            except Exception as exc:
                logger.error(msg=f'Error while loading ganyu.extensions.{ext}', exc_info=exc)

    @staticmethod
    async def on_starting(event: hikari.StartingEvent) -> None:
        logger.info(f'Bot is starting')

    async def on_started(self, event: hikari.StartedEvent) -> None:
        if not self._ready:
            while not self._extension_ready:
                await asyncio.sleep(0.4)

        self.startup_time = datetime.utcnow()
        self._ready = True
        logger.info(f'Bot started and connected to {self.get_me()} ({self.heartbeat_latency*1000:.2f}ms)')

    async def on_message(self, event: lightbulb.CommandInvocationEvent) -> None:
        if not event.context.author.is_bot and event.context.command and not self._ready:
            await event.context.respond('Bot is not ready, please try again later.', delete_after=10)


bot = Ganyu()
