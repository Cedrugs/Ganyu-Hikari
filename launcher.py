from ganyu import bot


import logging
import contextlib


@contextlib.contextmanager
def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    try:
        dt_fmt = '%Y/%m/%d %H:%M:%S'
        fmt = logging.Formatter('{asctime} {levelname:<7} {name}: {message}', dt_fmt, style='{')
        logging.getLogger("hikari.ratelimits").setLevel(logging.ERROR)

        file_hdlr = logging.FileHandler(
            filename='data/log/log.txt',
            encoding="utf-8",
            mode='w'
        )
        file_hdlr.setFormatter(fmt)
        logger.addHandler(file_hdlr)

        yield
    finally:
        handlers = logger.handlers[:]
        for hdlr in handlers:
            hdlr.close()
            logger.removeHandler(hdlr)


if __name__ == '__main__':
    with setup_logging():
        bot.build()
