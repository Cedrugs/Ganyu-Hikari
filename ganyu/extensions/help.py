from utils import Colour, get_syntax, arg_type, get_command_extra


import logging
import lightbulb
import hikari


help_ext = lightbulb.Plugin('Help')
help_ext.add_checks(lightbulb.guild_only)


logger = logging.getLogger(__name__)


@lightbulb.option(
    name='command_name',
    description='The name of the command you are looking help for',
    default=None,
    required=False,
    type=str
)
@help_ext.command
@lightbulb.command(
    name='help',
    description="List of Ganyu's command or help for specific command"
)
@lightbulb.implements(lightbulb.SlashCommand)
async def help(ctx: lightbulb.Context) -> None | lightbulb.ResponseProxy:
    """Example: help daily info"""
    command_name = ctx.options.command_name
    bot = ctx.bot

    if not command_name:
        embed = hikari.Embed(
            color=Colour.blue,
            description='For more detailed help, consider using `/help <command>`'
        )

        embed.set_author(name="Ganyu's commands", icon=bot.get_me().avatar_url)
        embed.set_footer(text='DM @cedric#8394 for more help')

        plugins = bot.plugins
        for plugin in ['Help', 'Error', 'Tasks']:
            plugins.pop(plugin)

        fields = [
            (plugin.name, ", ".join([f'`{x.name}`' for x in bot.d.commands[plugin.name]]), False)
            for plugin in list(plugins.values())
        ]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.respond(embed=embed)
    else:
        command_name_split = command_name.split(' ')
        command = bot.get_slash_command(command_name_split[0])

        if len(command_name_split) > 1:
            command = command.get_subcommand(command_name_split[1])

        if not command:
            return await ctx.respond(f"Sorry but there's no help for `{command_name}")

        embed = hikari.Embed(
            title=f'Help for {f"{command.parent.name} {command.name}" if command.is_subcommand else command.name}',
            color=Colour.blue,
            description=command.description if command.description else 'No description for this command'
        )

        docstring = command.callback.__doc__
        example = f'```/{get_syntax(command)}```'

        fields = [
            ('Usage', f'`{get_syntax(command)}`', True)
        ]

        if command.options:
            options = command.options.values()
            text = '\n'.join(
                f'`{x.name.replace("_", " ")}`: {x.description} ({arg_type[str(x.arg_type)]})' for x in options
            )

            fields.append(('Options', text, False))

        if docstring:
            extra = get_command_extra(docstring)

            if extra.example:
                example = f'```/{extra.example}```'

            else:
                fields.append(('Example', example, False))

            if extra.notes:
                fields.append(('Notes', extra.notes.format(prefix=ctx.prefix), False))

        fields.append(('Example', example, False))

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        embed.set_footer(text="💡 [] sign for optional and <> sign for required.")

        await ctx.respond(embed=embed)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(help_ext)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(help_ext)
