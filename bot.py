from os import getenv as e
from discord.errors import LoginFailure
from discord.ext.commands.errors import ExtensionFailed

bot = commands.Bot(command_prefix='?', description='Multi-purpose Discord Bot', case_insensitive=True)

try:
    token = e('token')
except KeyError:
    error("Token not found")


@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user.display_name}")
    bot.load_extension("cogs.feed")


if __name__ == '__main__':
    try:
        bot.run(token)
    except LoginFailure:
        error("Token is Invalid")
