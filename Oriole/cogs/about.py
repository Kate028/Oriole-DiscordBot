import discord
import datetime
from discord.ext import commands


class About(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="about")
    async def _about(self, ctx):
        """Displays information about the bot"""
        info_embed = discord.Embed(
            title="Oriole DiscordBot",
            color=discord.Color.gold(),
            description="An open source multipurpose discord bot.",
        )
        info_embed.add_field(
            name="Created At",
            value=self.bot.user.created_at.strftime("%B %d %Y at %H:%M:%S %p"),
        )
        info_embed.add_field(
            name="Uptime",
            value=(datetime.datetime.utcnow() - self.bot.uptime),
        )
        info_embed.add_field(
            name="Github",
            value=f"[Repository]({self.bot.repository})",
        )

        info_embed.set_thumbnail(url=self.bot.user.avatar.url)

        await ctx.send(embed=info_embed)


def setup(bot):
    bot.add_cog(About(bot))
