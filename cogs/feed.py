from os import getenv as e
from discord.ext import commands, tasks
import praw
from discord import Embed
from discord import Webhook, AsyncWebhookAdapter
from aiohttp import ClientSession

reddit = praw.Reddit(client_id=e('client_id'), client_secret=e('client_secret'),
                      password=e('password'), user_agent=e('user_agent'),
                      username=e('username'))


class Remind(commands.Cog):
    """Error handling.
    """

    def __init__(self, bot):
        self.bot = bot
        self.feed.start()

    def cog_unload(self):
        self.feed.cancel()

    @tasks.loop(hours=1.0)
    async def feed(self):
        post = Embed(color=0xFF5700)
        for submission in reddit.subreddit("kerala").new(limit=1):
            post.title = submission.title
            post.url = f"https://www.reddit.com/{submission.permalink}"
            post.set_footer(text=f"Score: {submission.score}")
            post.description = f"Comments: {submission.num_comments}"
            post.set_author(icon_url="https://i.ibb.co/4FLWrf5/community-Icon-sb8lb3clguv01.png",
                            name="r/Kerala", url="https://www.reddit.com/r/Kerala/")
            break
        async with ClientSession() as session:
            webhook = Webhook.from_url(e('webhook'), adapter=AsyncWebhookAdapter(session))
            await webhook.send(embed=post, username='r/Kerala Feed')

    @feed.before_loop
    async def before_printer(self):
        print('waiting...')
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Remind(bot))
