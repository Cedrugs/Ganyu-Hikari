import lightbulb
import logging


error = lightbulb.Plugin("Error")
logger = logging.getLogger(__name__)


@error.listener(lightbulb.CommandErrorEvent)
async def on_error(event: lightbulb.CommandErrorEvent) -> None:
    more_help = f"For more help, please run `{event.context.prefix}help {event.context.command.name}` :)"
    if isinstance(event.exception, lightbulb.OnlyInGuild):
        pass
    elif isinstance(event.exception, lightbulb.CommandInvocationError):
        logger.error(event.exception.original)
    elif isinstance(event.exception, lightbulb.NotEnoughArguments):
        missing_options = ', '.join([f'`{x.name}`' for x in event.exception.missing_options])
        await event.context.respond(f'You are missing required argument: {missing_options}. {more_help}')
    else:
        logger.error(type(event.exception))


def load(bot):
    bot.add_plugin(error)


def unload(bot):
    bot.remove_plugin(error)
