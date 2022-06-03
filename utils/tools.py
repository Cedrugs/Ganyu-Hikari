from utils.models import CommandExtra, PartialCommand


import datetime
import lightbulb
import typing as t
import textwrap


__all__ = ('strfdelta', 'format_uptime', 'get_syntax', 'get_command_extra')


def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)


def format_uptime(startuptime: datetime) -> str:
    """
    A format a datetime to startuptime date.
    Params:
     - startuptime (datetime) : Bot's startup time in Datetime object
    Return:
    - Time in format (ex: 1d 2h 3m 10s)
    """
    uptime = datetime.datetime.utcnow() - startuptime
    day, hour = strfdelta(uptime, "{days}"), strfdelta(uptime, "{hours}")
    minute, second = strfdelta(uptime, "{minutes}"), strfdelta(uptime, "{seconds}")
    days, hours, minutes, seconds = f'{day}d', f'{hour}h', f'{minute}m', f'{second}s'
    return ''.join(
        [f'{days if int(day) != 0 else ""}', f'{hours if int(hour) != 0 else ""}',
         f'{minutes if int(minute) != 0 else ""}' f'{seconds if int(second) != 0 else ""}']
    )


def get_syntax(command: t.Union[lightbulb.Command, lightbulb.CommandLike, PartialCommand]) -> str:
    """
    A function to get syntax from CommandLike object
    Params:
     - cmd (Command, CommandLike) : Command object to retrieve property
    Return:
    - Command syntax in str
    """

    params = []

    for value in command.options.values():
        key = value.name.replace('_', ' ')
        params.append(f"[{key}]" if not value.required else f"<{key}>")

    param = " ".join(params)

    if command.parent:
        return f'{command.parent.name} {command.name} {param}'

    return command.name if param == '' else f'{command.name} {param}'


def get_command_extra(docstring: str) -> CommandExtra:
    """
    A function to format docstring for discord, because sometime it also shows the code indentation
    Params:
     - docstring (str) : The docstring to format
    Return:
    - CommandExtra dataclass with example and notes inside.
    """

    raw_line = [x for x in textwrap.dedent(docstring).split('\n') if not x == '']
    normal_line = []
    kwargs = {}

    for idx, line in enumerate(raw_line):
        if line.startswith('Example:') and idx == 0:
            kwargs.update({'example': line[9:]})
        else:
            normal_line.append(line)

    if normal_line:
        kwargs.update({'notes': '\n'.join(normal_line)})

    return CommandExtra(**kwargs)
