__all__ = ('strfdelta', 'format_uptime', 'get_syntax')


import datetime
import lightbulb
import typing as t


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


def get_syntax(command: t.Union[lightbulb.Command, lightbulb.CommandLike]) -> str:
    """
    A function to get syntax from CommandLike object
    Params:
     - cmd (Command, CommandLike) : Command object to retrieve property
    Return:
    - Command syntax in str
    """

    params = []

    for key, value in command.options:
        if key not in ('self', 'ctx', 'return'):
            params.append(f"[{key}]" if "NoneType" in str(value) else f"<{key}>")

    param = " ".join(params)

    return f"{command.name}{param}"
