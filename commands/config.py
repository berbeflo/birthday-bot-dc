import discord
from discord.ext import commands
from config.config import config
from re import match

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True, invoke_without_command=False)
    async def config(self, ctx):
        pass
    
    @config.group(pass_context=True, invoke_without_command=False)
    async def get(self, ctx):
        pass

    @config.group(pass_context=True, invoke_without_command=False)
    async def set(self, ctx):
        pass
    
    @get.command(name='prefix')
    async def get_prefix(self, ctx):
        await ctx.send('The current prefix for this guild ist `{0}`'.format(config.base.get_prefix(ctx.message.guild.id)))

    @set.command(name='prefix')
    async def set_prefix(self, ctx, *, prefix):
        prefix = prefix.strip('"`\'')
        if match(r"^[a-z]{0,3}[.-~!?]{0,2} ?$", prefix) and prefix != ' ' and prefix != '':
            config.base.set_prefix(ctx.message.guild.id, prefix)
            await ctx.send('Set prefix for this guild to `{0}`'.format(prefix))
        else:
            await ctx.send('Invalid prefix provided. Prefix must match the pattern `^[a-z]{0,3}[.-~!?]{0,2} ?$` and must not be a single blank or empty.')

def setup(bot):
    bot.add_cog(Config(bot))