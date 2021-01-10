import discord
from discord.ext import commands
from config.config import config

description = "Birthday Bot"
intents = discord.Intents.default()

bot = commands.Bot(command_prefix=lambda bot, message : config.base.get_prefix(message.guild.id), description=description, case_insensitive=True, intents=intents)

startup_extensions = [
    "cog.config",
    "ext.botinfo",
]

@bot.event
async def on_ready():
    print("bot booted")
    for extension in startup_extensions:
        bot.load_extension(extension)
        print("extension " + extension + " loaded")

    await bot.extensions["ext.botinfo"].info.setup()
    await bot.change_presence(activity=discord.Game(name="Yet Another Birthday Bot"))

    print("bot ready")

bot.run(config.base.get_token())