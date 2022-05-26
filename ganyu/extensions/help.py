from utils import Colour, HelpView, get_syntax, arg_type, get_command_extra, CONSUME_REST


import logging
import lightbulb
import hikari


help_ext = lightbulb.Plugin('Help')
help_ext.add_checks(lightbulb.guild_only)


logger = logging.getLogger(__name__)


@lightbulb.option('command_name', "The command/category you want to ask for help", default=None, modifier=CONSUME_REST)
@help_ext.command
@lightbulb.command('help', "A list of Ganyu's command or help for specific command")
@lightbulb.implements(lightbulb.PrefixCommand)
async def help_cmd(ctx: lightbulb.Context) -> None:
    """Example: {prefix}help wish"""
    command_name = ctx.options.command_name
    bot = ctx.bot
    if not command_name:
        embed = hikari.Embed(
            color=Colour.blue,
            description=f"For more detailed help, use `{ctx.prefix}help <command>`"
        )

        embed.set_author(name="Ganyu's command list", icon=bot.get_me().avatar_url)
        embed.set_footer(text=f'Requested by {ctx.author}')

        plugins = bot.plugins
        plugins.pop('Error')
        plugins.pop('Help')

        # Help and error is removed because there's no command on help plugin and we don't want to show help command.

        fields = [
            (plugin.name, ", ".join([f'`{x.name}`' for x in bot.d.commands[plugin.name]]), False)
            for plugin in list(plugins.values())
        ]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        await ctx.respond(embed=embed)
    else:
        hidden_ext = ['Error', 'Help']
        if (ext := command_name.lower()) in (name.lower() for name in bot.plugins.keys() if name not in hidden_ext):
            commands = [cmd for cmd in bot.d.commands[ext.title()]]

            view = HelpView(source=commands, title=f'Help for {ext.title()}', color=Colour.blue, page=5)
            await view.send(ctx.channel_id)
        else:
            command = bot.get_prefix_command(command_name)

            if not command:
                return await ctx.respond(f"Sorry but, there's no help for `{command_name}`")

            docstring = command.callback.__doc__
            example = f'```{ctx.prefix}{get_syntax(command)}```'

            embed = hikari.Embed(
                title=f'Help for {command.name}', color=Colour.blue,
                description=command.description if command.description else 'No description for this command'
            )

            fields = [
                ('Usage', f'`{get_syntax(command)}`', True),
                ('Aliases', ', '.join(f"`{x}`" for x in command.aliases) if command.aliases else '`None`', True)
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
                    example = f'```{extra.example.format(prefix=ctx.prefix)}```'

                else:
                    fields.append(('Example', f'```{ctx.prefix}{get_syntax(command)}```', False))

                if extra.notes:
                    fields.append(('Notes', extra.notes, False))

            fields.append(('Example', example, False))

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            embed.set_footer(text="💡 [] sign for optional and <> sign for required.")
            await ctx.respond(embed=embed)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(help_ext)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(help_ext)
