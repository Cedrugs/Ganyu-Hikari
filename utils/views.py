from miru.ext import nav
from utils import get_syntax, PartialCommand


import hikari
import miru
import typing as t


__all__ = ('HelpView', 'Paginator', 'ValueView')


class HelpView(nav.NavigatorView):

    def __init__(self, source, title, color, page, timeout=30, footer="{page}"):
        self.source: t.Union[list, tuple] = source
        self.title: str = title
        self.color: str = color
        self.page: int = page
        self.footer: str = footer
        self.embeds = self._format_page()

        super().__init__(timeout=timeout, pages=self.embeds)

    def _build_embed(self, data: t.List[PartialCommand], footer: str) -> hikari.Embed:
        embed = hikari.Embed(color=self.color, title=self.title)
        embed.set_footer(text=footer)

        fields = [(command.name.title(), f'{command.description}\n`{get_syntax(command)}`', False) for command in data]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        return embed

    def _format_page(self) -> t.List[hikari.Embed]:
        divided_source = [self.source[i:i + self.page] for i in range(0, len(self.source), self.page)]
        result_embeds = []

        for idx, x in enumerate(divided_source, 1):
            embed = self._build_embed(
                x, footer=f"Page {idx} of {len(divided_source)}"
                if self.footer == '{page}' else self.footer
            )
            result_embeds.append(embed)

        return result_embeds


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


class ValueView(miru.View):

    def __init__(
            self, buttons, timeout=30, disable_after_respond=False, delete_after_respond=False,
            disable_after_timeout=False, delete_after_tiemout=False, **kwargs
    ):
        self.value: str = None
        self.disable_after_respond = disable_after_respond
        self.delete_after_respond = delete_after_respond
        self.delete_after_timeout = delete_after_tiemout
        self.disable_after_timeout = disable_after_timeout
        self.buttons: t.List[t.Union[str, miru.Button]] = buttons

        super().__init__(timeout=timeout, **kwargs)
        self.add_button()

    def add_button(self) -> None:
        for item in self.buttons:
            if not isinstance(item, miru.Button):
                item = miru.Button(label=item, custom_id=item, style=hikari.ButtonStyle.SECONDARY)
            item.callback = self._callback
            self.add_item(item)

    async def _callback(self, context: miru.Context) -> None:
        self.value = context.interaction.custom_id

        if self.delete_after_respond:
            await self.message.delete()

        elif self.disable_after_respond:
            for child in self.children:
                if isinstance(child, miru.Button):
                    child.disabled = True
            await self.message.edit(components=self.build())

        else:
            await self.message.edit(components=None)

        super().stop()

    async def on_timeout(self) -> None:
        await self.stop()

    async def stop(self) -> None:
        if self.delete_after_timeout:
            await self.message.delete()

        elif self.disable_after_timeout:
            for child in self.children:
                if isinstance(child, miru.Button):
                    child.disabled = True
            await self.message.edit(components=self.build())

        else:
            await self.message.edit(components=None)
