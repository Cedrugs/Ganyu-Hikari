from miru.ext import nav
from utils.genshin_impact import get_weapon_info, GenshinWeapon, WeaponButtonType
from utils import Colour


import hikari
import miru
import typing as t
import lightbulb


__all__ = ('Paginator', 'WeaponPaginator', 'DailySetupView')


class WeaponPaginator(miru.View):

    _buttons = ['Details', 'Ascension', 'Statistic']

    def __init__(self, ctx, weapon_name, start_from, timeout=60):
        self.ctx: lightbulb.Context = ctx
        self.weapon_name: str = weapon_name
        self.start_from: WeaponButtonType = start_from
        self.data: GenshinWeapon = None
        self.embeds = {}

        super().__init__(timeout=timeout)

    async def start(self, **kwargs):
        await self._get_data()
        self.add_button()

        for button in self._buttons:
            self.embeds.update({button.lower(): self._format_embed(button.lower())})

        message = await self.ctx.respond(embed=self.embeds[self.start_from], components=self.build())

        super().start(await message)

    def add_button(self) -> None:
        for button in self._buttons:
            item = miru.Button(label=button, custom_id=button.lower(), style=hikari.ButtonStyle.SECONDARY)

            if button.lower() == self.start_from:
                item.disabled = True

            item.callback = self._callback

            self.add_item(item)

    async def _callback(self, context: miru.Context) -> None:
        for item in self.children:
            if isinstance(item, miru.Button):

                if item.custom_id != context.interaction.custom_id:
                    item.disabled = False
                else:
                    item.disabled = True

        await self.message.edit(embed=self.embeds[context.interaction.custom_id], components=self.build())

    async def _get_data(self) -> None:
        self.data = await get_weapon_info(
            self.weapon_name,
            self.ctx.bot.genshin_weapons,
            self.ctx.bot.genshin_weapons_list
        )

        if not self.data:
            return None

    def _format_embed(self, page_type: WeaponButtonType) -> hikari.Embed:
        data = self.data

        if page_type == WeaponButtonType.details:

            fields = [
                ("Rarity", f"{data.rarity}★", True),
                ("Base Attack", data.base_atk, True),
                ("Type", data.type, True),
                (f"Passive ({data.passive.name})", data.passive.description, False),
                ("Substat", data.substat, True),
                ("Max Level", data.max_level, True),
                ("Obtainable from", data.location, False)
            ]

            embed = hikari.Embed(
                title=data.name,
                description=data.description,
                colour=Colour.blue
            )
            embed.set_thumbnail(data.icon)
            embed.set_footer(text='This bot is still under development, search results may not be precise.')

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

        elif page_type == WeaponButtonType.ascension:

            icons = self.ctx.bot.genshin_emojis
            icon = lambda x: icons[x.lower().replace(' ', '').replace("'", "").replace('-', '')]

            fields = []

            for level in data.ascension.levels.keys():
                material = [[list(item.keys())[0], list(item.values())[0]] for item in data.ascension.levels[level]]

                fields.append(
                    (f'Ascension Phase {level[-1:]}', '\n'.join([f' - {icon(x[0])} {x[1]} {x[0]}' for x in material]),
                     False)
                )

            summary = [[item, data.ascension.summary[item]] for item in data.ascension.summary]
            fields.append(('Summary', '\n'.join([f' - {icon(x[0])} {x[0]} {x[1]}' for x in summary]), False))

            embed = hikari.Embed(title=f'{data.name} Ascension Materials', description=data.description,
                                 colour=Colour.blue)
            embed.set_thumbnail(data.icon)

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

        elif page_type == WeaponButtonType.statistic:

            embed = hikari.Embed(
                title=data.name,
                colour=Colour.blue,
                description=f'{data.description}\n\n**Statistic Progression: {data.substat}**'
            )
            embed.set_image(data.stats.visual)

        else:
            raise TypeError('Invalid type of Weapon Button')

        return embed

    async def on_timeout(self) -> None:
        await self.message.edit(components=None)


class Paginator(nav.NavigatorView):

    def __init__(self, source, title, color, timeout=30, footer="{page}"):
        self.source: t.Union[list, tuple] = source
        self.title: str = title
        self.color: str = color
        self.footer: str = footer
        self.embeds = self._format_page()

        super().__init__(timeout=timeout, pages=self.embeds)

    def _build_embed(self, data: str, footer: str) -> hikari.Embed:
        embed = hikari.Embed(color=self.color, title=self.title, description=data)
        embed.set_footer(text=footer)

        return embed

    def _format_page(self) -> t.List[hikari.Embed]:
        result_embeds = []

        for idx, x in enumerate(self.source, start=1):
            embed = self._build_embed(x, self.footer.format(page=f'Page {idx} of {len(self.source)}'))
            result_embeds.append(embed)

        return result_embeds


class DailySetupButton(miru.Modal):

    ltuid = miru.TextInput(label="LTUID", required=True, style=hikari.TextInputStyle.PARAGRAPH)
    ltoken = miru.TextInput(label="LTOKEN", required=True, style=hikari.TextInputStyle.PARAGRAPH)

    async def callback(self, ctx: miru.ModalContext) -> None:
        await ctx.respond('Thank you! Your cookie will be processed.', flags=hikari.MessageFlag.EPHEMERAL)


class DailySetupView(miru.View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.modal = modal = DailySetupButton(title='Hoyolab Daily Checkin Claimer Setup', timeout=120)
        self.ltuid = None
        self.ltoken = None
        self.timed_out = False

    @miru.button(label="Start!", style=hikari.ButtonStyle.PRIMARY)
    async def modal_button(self, button: miru.Button, ctx: miru.ViewContext) -> None:

        await self.modal.send(ctx.interaction)
        await self.modal.wait(timeout=60)

        self.ltuid = list(self.modal.values.values())[0]
        self.ltoken = list(self.modal.values.values())[1]

        self.modal.stop()
        self.stop()

    async def on_timeout(self) -> None:
        for item in self.children:
            item.disabled = True

        self.timed_out = True
        self.modal.stop()
        await self.message.edit(components=self)
