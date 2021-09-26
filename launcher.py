# -*- coding: utf-8
from discord.ext import commands

from config import api_token

bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
    print("on_ready")


bot.load_extension('cogs.factorio')
bot.run(api_token)
