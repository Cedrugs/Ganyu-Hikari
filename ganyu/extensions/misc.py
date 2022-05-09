from time import time
from platform import python_version
from utils import format_uptime, Colour


import lightbulb
import logging
import hikari


misc = lightbulb.Plugin("Miscellaneous")
logger = logging.getLogger(__name__)


@lightbulb.add_checks(lightbulb.guild_only)
@misc.command
@lightbulb.command(
    name='ping',
    aliases=['latency'],
    description="Check Ganyu's latency",
)
@lightbulb.implements(lightbulb.PrefixCommand)
async def ping_cmd(ctx: lightbulb.Context):
    await ctx.respond(f"My current ping is {ctx.bot.heartbeat_latency*1000:.2f}ms")


# noinspection PyUnresolvedReferences
@lightbulb.add_checks(lightbulb.guild_only)
@misc.command
@lightbulb.command(
    name='statistics',
    aliases=['stats', 'stat'],
    description="Check Ganyu's statistics"
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def statistics_cmd(ctx: lightbulb.Context):
    start = time()
    await ctx.bot.rest.trigger_typing(ctx.channel_id)
    end = time()
    ping = (end - start)*1000
    embed = hikari.Embed(colour=Colour.Blue, description=f'Created by {ctx.bot.cache.get_user(563287825882021893)}')
    embed.set_author(name="Ganyu's Statistics")
    embed.set_footer(text=f"Ping: {ctx.bot.heartbeat_latency*1000:,.2f}ms | Response Time: {ping:,.2f}ms")
    fields = [
        ('Python', f'`{python_version()}`', False),
        ('Total Users', f'`{len(ctx.bot.cache.get_users_view())}` Users', False),
        ('Total Servers', f'`{len(await ctx.bot.rest.fetch_my_guilds())}` Servers', False),
        ('Uptime', f'`{format_uptime(ctx.bot.startup_time)}`', False)
    ]
    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)
    await ctx.respond(embed=embed)


def load(bot):
    bot.add_plugin(misc)


def unload(bot):
    bot.remove_plugin(misc)
