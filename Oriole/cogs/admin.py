from discord.ext import commands


class Admin(commands.Cog):
    """Commands only available for bot administrators"""

    def __init__(self, bot):
        self.bot = bot
        self.emoji = "🐝"
        self.description = "Commands only available for bot administrators"

    @commands.is_owner()
    @commands.command(name="load")
    async def _load(self, ctx, *, extension) -> None:
        """Load an unloaded cog."""
        try:
            self.bot.load_extension(f"cogs.{extension}")
        except Exception as e:
            await ctx.send(f"There was an exeption while trying to load {extension}.")
        else:
            await ctx.send(f"{extension} loaded correctly.", delete_after=3)

    @commands.is_owner()
    @commands.command(name="unload")
    async def _unload(self, ctx, *, extension) -> None:
        """Unload an loaded cog."""
        try:
            self.bot.unload_extension(f"cogs.{extension}")
        except Exception as e:
            await ctx.send(f"There was an exeption while trying to load {extension}.")
        else:
            await ctx.send(f"{extension} unloaded correctly.", delete_after=3)

    @commands.is_owner()
    @commands.command(name="reload")
    async def _reload(self, ctx, *, extension) -> None:
        """Reload a cog."""
        try:
            self.bot.reload_extension(f"cogs.{extension}")
        except Exception as e:
            await ctx.send(f"There was an exeption while trying to load {extension}.")
        else:
            await ctx.send(f"{extension} reloaded correctly.", delete_after=3)


def setup(bot):
    bot.add_cog(Admin(bot))
