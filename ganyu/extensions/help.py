from utils import Colour, HelpView


import logging
import lightbulb
import hikari


logger = logging.getLogger(__name__)


help_ext = lightbulb.Plugin("Help")


@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.option('command_name', "The commands or category your want to ask for help", default=None)
@help_ext.command
@lightbulb.command('help', "A list of Ganyu's command or help for specific command")
@lightbulb.implements(lightbulb.PrefixCommand)
async def help_cmd(ctx: lightbulb.Context):
    command_name = ctx.options.command_name
    if not command_name:
        embed = hikari.Embed(
            color=Colour.Blue,
            description=f"For more detailed help, use `{ctx.prefix}help <command>`"
        )

        embed.set_author(name="Ganyu's command list", icon=ctx.bot.get_me().avatar_url)
        embed.set_footer(text=f'Requested by {ctx.author}')

        plugins = ctx.bot.plugins
        plugins.pop('Error', 'Help')

        # Help and error is removed because there's no command on help plugin and we don't want to show help command.

        fields = [
            (plugin.name, ", ".join([f'`{x.name}`' for x in plugin.raw_commands]), False)
            for plugin in list(plugins.values())
        ]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        await ctx.respond(embed=embed)
    else:
        hidden_exts = ['Error']
        if (ext := command_name.lower()) in (name.lower() for name in ctx.bot.plugins.keys() if name not in hidden_exts):
            command_list = [cmd for cmd in ctx.bot.get_plugin(ext.title()).raw_commands if not cmd.hidden]

            view = HelpView(source=command_list, title=f'Help for {ext.title()}', color=Colour.Blue, page=5)
            await view.send(ctx.channel_id)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(help_ext)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(help_ext)
