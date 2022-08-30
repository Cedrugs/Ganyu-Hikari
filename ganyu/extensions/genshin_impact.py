from utils import Colour, Paginator, WeaponPaginator, WeaponButtonType
from utils.collections import chinese_ps_script, global_ps_script, CONSUME_REST, banner_code
from utils.genshin_impact import get_wish


import hikari
import lightbulb
import logging
import tabulate
import genshin


genshin_ext = lightbulb.Plugin('Genshin Impact')
genshin_ext.add_checks(lightbulb.guild_only)


logger = logging.getLogger(__name__)


@lightbulb.option('banner', "Banner to check (standard, event, weapon)", required=True, modifier=CONSUME_REST)
@genshin_ext.command
@lightbulb.command(
    name='wish',
    description='Check your Genshin Impact wish history including 3,4, and 5*'
)
@lightbulb.implements(lightbulb.PrefixCommandGroup)
async def wish_cmd(ctx: lightbulb.Context) -> None:
    """Example: {prefix}wish standard"""
    banner = ctx.options.banner
    if (selected_banner := banner.lower()) in ('event', 'standard', 'weapon'):
        wish_history = await ctx.bot.genshin_wishes.find_by_id(ctx.author.id)

        if not wish_history:
            return await ctx.respond(
                f"You must setup your wish history before running this, please use `{ctx.prefix}wish update` command."
            )
        else:
            wish = wish_history['wishHistory'][str(banner_code[selected_banner])]

            result_raw = []
            for x in wish:
                result_raw.append([x['Name'], f'{x["Rarity"]}*', x['Time'], x['Pity']])

            divided_page = [result_raw[i:i + 10] for i in range(0, len(result_raw), 10)]

            table = lambda m: tabulate.tabulate(
                m, headers=['Name', 'Rarity', 'Time', 'Pity'],
                colalign=['left', 'center', 'center', 'center'],
                tablefmt='fancy_grid'
            )

            tables = [f'```\n{table(x)}\n```' for x in divided_page]

            view = Paginator(
                tables, color=Colour.blue,
                title=f'Wish History for {ctx.author} (UID {wish_history["wishHistory"]["UID"]})',
                footer='The table may appear differently depending on the size of your screen. '
                       'Please rotate your phone to see the table correctly if you are using a '
                       'mobile device.\n{page}',
                timeout=60
            )
            return await view.send(ctx.channel_id)
    await ctx.respond("Invalid banner, available banner: `event`, `weapon`, `standard`")


@lightbulb.option('authkey', 'Authkey you need in order to fetch wish history', required=True, modifier=CONSUME_REST)
@genshin_ext.command
@wish_cmd.child()
@lightbulb.command(
    name='update',
    aliases=['renew', 'setup'],
    description='Update your Genshin Impact wish history'
)
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def wish_update(ctx: lightbulb.Context) -> None:
    """Example: {prefix}wish update Qmt8nwQMjAThvHex1ypzU6ZFevePqgaGTDs2IEZ7wrT/4G4vnsTAG2l7Y3pdAs9fP6SWUEhBtvA
    For tutorial on how to get authentication key (authkey) run the `{prefix}wish` authkey command"""
    authkey = ctx.options.authkey
    try:
        genshin.GenshinClient(authkey=authkey)
    except ValueError:
        return await ctx.respond(
            'Your authkey is invalid, please re-enter your authkey. for more information about authkey, '
            'please run the command `g!wish authkey`'
        )

    message = await ctx.respond('Please wait, this may take a while depending on your wish history size.')
    check = await ctx.bot.genshin_wishes.find_by_id(ctx.author.id)
    wish = await get_wish(authkey, banner_type=[200, 301, 302])

    if check and check['wishHistory'] == wish:
        return await message.edit('Nothing changed, your wish history is still the same.')

    await ctx.bot.genshin_wishes.upsert({"_id": ctx.author.id, "wishHistory": wish})

    return await message.edit(content='Your authkey has been updated.')


@genshin_ext.command
@wish_cmd.child()
@lightbulb.command(
    name='authkey',
    aliases=['key'],
    description='Short tutorial on how to get your authentication key for wish history'
)
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def authkey_cmd(ctx: lightbulb.Context):
    embed = hikari.Embed(
        title='How to get authkey?',
        description="Authkey is used to access your wish history, it's safe to share, and resets every 24 hours",
        colour=Colour.blue
    )

    fields = [
        ('1. Open Genshin Impact on your PC', 'If you use multiple accounts please restart the game.', False),
        ('2. Open Wish History', "Wait for it to load, any banner don't matter", False),
        (
            '3. Open Windows Powershell',
            f'Paste the following command to powershell:\n *Chinese Server*\n```ps\n{chinese_ps_script}```\n'
            f'*Global Server (NA/EU/ASIA)*\n```ps\n{global_ps_script}```', False
        ),
        ('4. Press ENTER', 'The authkey should be copied to clipboard', False),
        ('5. Run the wish command', f'Now you have to run the command `{ctx.prefix}wish update <authkey>`', False)
    ]

    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)

    await ctx.respond(embed=embed)


@lightbulb.option('weapon_name', 'Name of the weapon you want to see the details', default=None, modifier=CONSUME_REST)
@genshin_ext.command
@lightbulb.command(
    name='weapon',
    aliases=['w'],
    description="Get weapon details by it's name"
)
@lightbulb.implements(lightbulb.PrefixCommandGroup)
async def weapon_group(ctx: lightbulb.Context, weapon_name=None) -> None:
    """Example: {prefix}weapon amos bow"""
    weapon_name = ctx.options.weapon_name or weapon_name

    paginator = WeaponPaginator(ctx, weapon_name, WeaponButtonType.details)
    if not paginator:
        return await ctx.respond(f'{weapon_name} was not found.')

    await paginator.start()


@weapon_group.child()
@lightbulb.option('weapon_name', 'Name of the weapon you want to see the details', default=None, modifier=CONSUME_REST)
@genshin_ext.command
@lightbulb.command(
    name='statistic',
    aliases=['statistics', 'stats', 'stat', 's'],
    description="Get weapon statistic by it's name"
)
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def weapon_statistic(ctx: lightbulb.Context, weapon_name=None) -> None:
    """Example: {prefix}weapon statistic amos bow"""
    weapon_name = ctx.options.weapon_name or weapon_name

    paginator = WeaponPaginator(ctx, weapon_name, WeaponButtonType.statistic)
    if not paginator:
        return await ctx.respond(f'{weapon_name} was not found.')

    await paginator.start()


@lightbulb.option('weapon_name', 'Name of the weapon you want to see the details', default=None, modifier=CONSUME_REST)
@genshin_ext.command
@weapon_group.child()
@lightbulb.command(
    name='ascension',
    aliases=['asc', 'a'],
    description="Get weapon ascension material by it's name"
)
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def weapon_ascension(ctx: lightbulb.Context, weapon_name=None):
    weapon_name = ctx.options.weapon_name or weapon_name

    paginator = WeaponPaginator(ctx, weapon_name, WeaponButtonType.ascension)
    if not paginator:
        return await ctx.respond(f'{weapon_name} was not found.')

    await paginator.start()


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(genshin_ext)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(genshin_ext)
