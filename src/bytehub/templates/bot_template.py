import os
from discord.ext import commands

def create_bot(token_env_var="DISCORD_BOT_TOKEN"):
    token = os.getenv(token_env_var)
    if not token:
        raise RuntimeError("token not set")
    import discord
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)
    @bot.event
    async def on_ready():
        print(f"ready {bot.user} {bot.user.id}")
    @bot.command(name="ping")
    async def ping(ctx):
        await ctx.send("pong")
    return bot, token

if __name__ == "__main__":
    bot, token = create_bot()
    bot.run(token)
