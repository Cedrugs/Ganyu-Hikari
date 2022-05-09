__all__ = ('strfdelta', 'format_uptime')


from datetime import datetime


def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)


def format_uptime(startuptime) -> str:
    uptime = datetime.utcnow() - startuptime
    day, hour = strfdelta(uptime, "{days}"), strfdelta(uptime, "{hours}")
    minute, second = strfdelta(uptime, "{minutes}"), strfdelta(uptime, "{seconds}")
    days, hours, minutes, seconds = f'{day}d', f'{hour}h', f'{minute}m', f'{second}s'
    return f'{days if int(day) != 0 else ""} {hours if int(hour) != 0 else ""} {minutes if int(minute) != 0 else ""}' \
           f' {seconds if int(second) != 0 else ""}'.lstrip()