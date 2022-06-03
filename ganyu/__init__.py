from utils.json import *
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from glob import glob
from .database import Document


import lightbulb
import hikari
import logging
import asyncio
import miru
import utils as ut


logger = logging.getLogger(__name__)
extensions_path = [x.split('\\')[-1][:-3] for x in [x.split('/')[-1] for x in glob("ganyu/extensions/*.py")]]


class Extension(object):

    def __init__(self):
        for ext in extensions_path:
            setattr(self, ext, False)

    def ready_up(self, extension) -> None:
        setattr(self, extension, True)

    def all_ready(self) -> bool:
        return all([getattr(self, ext) for ext in extensions_path if ext])


# noinspection PyAbstractClass
class Ganyu(lightbulb.BotApp):

    def __init__(self):
        self._ready = False
        self._extension_ready = Extension
        self.startup_time = None

        self.mongo = AsyncIOMotorClient(read_json('config.json')['mongodbConnection'])
        self.genshin_db = self.mongo['genshinImpact']

        self.genshin_wishes = Document(self.genshin_db, 'wishes')
        self.genshin_weapons = Document(self.genshin_db, 'weapons')
        self.genshin_weapons_list = []
        self.genshin_emojis = read_json('data/emojis/material_emojis.json')

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
            intents=intents,
            help_class=None
        )

        miru.load(self)

    def build(self) -> None:

        self.subscribe(hikari.StartingEvent, self.on_starting)
        self.subscribe(hikari.StartedEvent, self.on_started)
        self.subscribe(lightbulb.CommandInvocationEvent, self.on_message)

        self.setup_extensions()
        self.extension_commands()

        self.run(activity=hikari.Activity(
                name='>help | Running on lightbulb hikari',
                type=hikari.ActivityType.PLAYING)
        )

    def extension_commands(self):
        extensions = [self.get_plugin(x) for x in self.plugins]

        all_commands = {}

        for extension in extensions:

            commands = [
                ut.PartialCommand(name=x.name, description=x.description, is_subcommand=False, options=x.options)
                for x in extension.all_commands if isinstance(x, lightbulb.PrefixCommand)
            ]

            commands_w_sub = [x for x in extension.raw_commands]

            for command in commands_w_sub:
                if command.subcommands:
                    for cmd in command.subcommands:
                        commands.append(
                            ut.PartialCommand(
                                name=f'{command.name} {cmd.name}',
                                description=cmd.description,
                                options=cmd.options,
                                is_subcommand=True
                            )
                        )

            all_commands.update({extension.name: commands})

        self.d.commands = all_commands

    def setup_extensions(self) -> None:
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

        self.genshin_weapons_list = [x['_id'] for x in await self.genshin_weapons.get_all()]

        logger.info(f'Bot started and connected to {self.get_me()} ({self.heartbeat_latency*1000:.2f}ms)')

    async def on_message(self, event: lightbulb.CommandInvocationEvent) -> None:
        if not event.context.author.is_bot and event.context.command and not self._ready:
            await event.context.respond('Bot is not ready, please try again later.', delete_after=10)


bot = Ganyu()
