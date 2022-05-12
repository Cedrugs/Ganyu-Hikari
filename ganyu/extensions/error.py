import lightbulb
import logging


error = lightbulb.Plugin("Error")
logger = logging.getLogger(__name__)


@error.listener(lightbulb.CommandErrorEvent)
async def on_error(event: lightbulb.CommandErrorEvent) -> None:
    if isinstance(event.exception, lightbulb.OnlyInGuild):
        pass
    if isinstance(event.exception, lightbulb.CommandInvocationError):
        logger.error(event.exception.original)
    else:
        logger.error(event.exception)


def load(bot):
    bot.add_plugin(error)


def unload(bot):
    bot.remove_plugin(error)
