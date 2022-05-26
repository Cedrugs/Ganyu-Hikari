from utils import CONSUME_REST, banner_code, Colour, Paginator, get_wish


import lightbulb
import logging
import tabulate
import genshin


genshin_ext = lightbulb.Plugin('Genshin Impact')
genshin_ext.add_checks(lightbulb.guild_only)


logger = logging.getLogger(__name__)


@genshin_ext.command
@lightbulb.option('banner', "Banner to check (standard, event, weapon)", required=True, modifier=CONSUME_REST)
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


@genshin_ext.command
@lightbulb.option('authkey', 'Authkey you need in order to fetch wish history', required=True, modifier=CONSUME_REST)
@wish_cmd.child
@lightbulb.command(
    name='update',
    aliases=['renew', 'setup'],
    description='Update your Genshin Impact wish history'
)
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def wish_update(ctx: lightbulb.Context) -> None:
    """Example: {prefix}wish update Qmt8nwQMjAThvHex1ypzU6ZFevePqgaGTDs2IEZ7wrT/4G4vnsTAG2l7Y3pdAs9fP6SWUEhBtvA
    For tutorial on how to get authentication key (authkey) run the {prefix}wish authkey command"""
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


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(genshin_ext)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(genshin_ext)
