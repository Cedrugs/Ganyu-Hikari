from lightbulb.ext import tasks as ts
from utils.genshin_impact import Hoyolab

import logging
import lightbulb
import pytz

tasks = lightbulb.Plugin("Tasks")
logger = logging.getLogger(__name__)

utc = pytz.utc


class Tasks:

    @staticmethod
    @ts.task(m=75, wait_before_execution=5)
    async def daily_check():
        cookies = await tasks.bot.genshin_cookies.get_all()

        for cookie in cookies:
            account = Hoyolab(cookie['ltuid'], cookie['ltoken'])
            user = await tasks.bot.rest.fetch_user(cookie['_id'])

            if not account.valid_cookie:
                return await user.send(
                    'Your cookie for Hoyolab check-in claimer is has expired. Please update by using `/daily setup`'
                )

            hoyo_check = await account.client.get_reward_info()

            if not hoyo_check.signed_in:
                reward = await account.check_in()

                await user.send(
                    f"Check-in for ID: {cookie['ltuid']} succeed! Your reward for today is {reward.amount}x {reward.name}"
                )


def load(bot):
    bot.add_plugin(tasks)


def unload(bot):
    bot.remove_plugin(tasks)
