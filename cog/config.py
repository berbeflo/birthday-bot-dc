import discord
from discord.ext import commands
from config.config import config
from re import match

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
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
    async def get_prefix(self, ctx, *, arguments = None):
        if self.__is_global_call(arguments):
            if self.__has_global_permissions(ctx.message.author):
                await ctx.send('The current global prefix for this bot is `{0}`'.format(config.base.get_prefix(None)))
                return 

        await ctx.send('The current prefix for this guild is `{0}`'.format(config.base.get_prefix(ctx.message.guild.id)))

    @set.command(name='prefix')
    async def set_prefix(self, ctx, prefix, *, arguments = None):
        set_global = False
        if self.__is_global_call(arguments):
            if self.__has_global_permissions(ctx.message.author):
                set_global = True
            else:
                await ctx.send('Invalid command call')
                return
            
        prefix = prefix.strip('"`\'')
        print(prefix)
        if match(r"^([a-z]{0,3}[-.~!?]{0,2}|[a-z]{1,3} ?)$", prefix):
            if set_global:
                config.base.set_prefix(None, prefix)
                await ctx.send('Set prefix for this bot to `{0}`'.format(prefix))
            else:
                config.base.set_prefix(ctx.message.guild.id, prefix)
                await ctx.send('Set prefix for this guild to `{0}`'.format(prefix))
        else:
            await ctx.send('Invalid prefix provided. Prefix must match the pattern `^([a-z]{0,3}[-.~!?]{0,2}|[a-z]{1,3} ?)$`.')

    def __is_global_call(self, arguments):
        if arguments == None:
            return False
        arg_list = arguments.split(" ")
        if "--global" in arg_list:
            return True
        return False

    def __has_global_permissions(self, author):
        return self.bot.extensions["ext.botinfo"].info.is_owner(author.id)

def setup(bot):
    bot.add_cog(Config(bot))