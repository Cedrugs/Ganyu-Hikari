from dataclasses import dataclass, field


import lightbulb
import typing as t


__all__ = ('Colour', 'CommandExtra', 'PartialCommand')


@dataclass(frozen=True)
class Colour:
    blue: str = '#99ebec'


@dataclass(frozen=True)
class CommandExtra:
    """Strings extracted from `commands.callback` function, and parsed to fill the example, and notes field?
    Why? because it's not really available on hikari-lightbulb"""
    example: str = field(default_factory=str)
    notes: str = field(default=None)

@dataclass(frozen=True)
class PartialCommand:
    """Partial command which only store partial of the data of command object, in order to get the full Command object
    you have to fetch it by yourself using the get_command method. And also the name property will return parent if
    the command has parent"""
    name: str = field(default_factory=str)
    description: str = field(default="No description")
    options: t.List[lightbulb.OptionLike] = field(default_factory=dict)
    is_subcommand: bool = field(default=False)