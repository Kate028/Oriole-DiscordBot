import datetime
from discord.errors import DiscordException
import humanize
from typing import Dict, List

import discord
from discord.ext import commands


class HelpDropdown(discord.ui.Select):
    def __init__(
        self,
        ctx: commands.Context,
        msg: discord.Message,
        data: Dict[commands.Cog, commands.Command],
        helpcommand: commands.HelpCommand,
    ):
        self.ctx = ctx
        self.bot = ctx.bot
        self.msg = msg
        self.command_data = data
        self.helpcommand = helpcommand
        self.pages = self._generate_pages()
        super().__init__(
            placeholder="Select a category...",
            min_values=1,
            max_values=1,
            options=self._fill_menu(),
        )

    def _generate_pages(self) -> Dict[str, discord.Embed]:
        """Generates a list containing all Embeds needed in the help cmd"""
        pages = {}

        for cog in self.command_data:
            if cog != None:
                commands = self.command_data[cog]

                cog_help_page = discord.Embed(
                    title=f"{cog.__cog_name__} Help",
                    color=discord.Color.gold(),
                    description="**No commands available.**"
                    if len(commands) == 0
                    else "**Commands**",
                )

                for command in commands:
                    cog_help_page.add_field(
                        name=self.helpcommand.get_command_signature(command),
                        value=self.helpcommand.get_command_brief(command),
                        inline=False,
                    )
                cog_help_page.set_author(
                    name=self.bot.user.name,
                    icon_url=self.bot.user.avatar.url,
                )
                cog_help_page.set_footer(
                    text=f"Requested by {self.ctx.author}",
                    icon_url=self.ctx.author.avatar.url,
                )
                pages[cog.__cog_name__] = cog_help_page

        return pages

    def _fill_menu(self) -> List[discord.SelectOption]:
        """Generates all options in dropdown menu."""
        options = []

        for cog in self.bot.cogs:
            option = discord.SelectOption(
                label=self.bot.cogs[cog].__cog_name__,
                description=self.bot.cogs[cog].description,
                emoji=self.bot.cogs[cog].emoji,
            )
            options.append(option)

        return options

    async def callback(self, interaction: discord.Interaction) -> None:
        await interaction.message.edit(embed=self.pages[self.values[0]])


class HelpDropdownView(discord.ui.View):
    def __init__(
        self,
        ctx: commands.Context,
        msg: discord.Message,
        data: Dict[commands.Cog, commands.Command],
        helpcommand: commands.HelpCommand,
    ):
        self.msg = msg
        super().__init__(timeout=60)
        self.add_item(HelpDropdown(ctx, msg, data, helpcommand))

    async def on_timeout(self) -> None:
        try:
            await self.msg.edit("Menu timed out after 60 seconds.", view=None)
        except discord.errors.NotFound:
            pass


class OrioleHelp(commands.HelpCommand):
    def _about_embed(self):
        """Returns an embed displaying information about the bot"""
        info_embed = discord.Embed(
            title="Oriole DiscordBot",
            color=discord.Color.gold(),
            description="An open source multipurpose discord bot.",
        )
        info_embed.add_field(
            name="Created At",
            value=self.context.bot.user.created_at.strftime("%B %d %Y"),
        )
        info_embed.add_field(
            name="Uptime",
            value=humanize.naturaldelta(
                datetime.datetime.utcnow() - self.context.bot.uptime
            ),
        )
        info_embed.add_field(
            name="Github",
            value=f"[Repository]({self.context.bot.repository})",
        )

        info_embed.set_thumbnail(url=self.context.bot.user.avatar.url)

        return info_embed

    def get_command_signature(self, command: commands.Command):
        return "**`%s%s %s`**" % (
            ".",
            command.qualified_name,
            command.signature,
        )

    def get_command_brief(self, command: commands.Command):
        return command.short_doc or "Command has not been documented."

    async def send_error_message(self, error: DiscordException) -> None:
        embed = discord.Embed(
            title="Something broke...",
            description=error,
            color=discord.Color.red(),
        )
        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_bot_help(self, mapping) -> None:
        channel = self.get_destination()
        msg = await channel.send(embed=self._about_embed())
        view = HelpDropdownView(self.context, msg, dict(mapping), self)
        await msg.edit(view=view)

    async def send_command_help(self, command) -> None:
        command_help_embed = discord.Embed(
            title=f"{(command.name).capitalize()} Help",
            description=self.get_command_signature(command),
            color=discord.Color.gold(),
        )
        command_help_embed.add_field(
            name="Description",
            value=command.help,
        )
        command_help_embed.add_field(
            name="Aliases",
            value=", ".join(command.aliases) if len(command.aliases) != 0 else None,
        )
        command_help_embed.add_field(
            name="Cog",
            value=command.cog.__cog_name__,
        )
        command_help_embed.set_author(
            name=self.context.bot.user.name,
            icon_url=self.context.bot.user.avatar,
        )
        command_help_embed.set_footer(
            text=f"Requested by {self.context.author}",
            icon_url=self.context.author.avatar,
        )

        await self.context.send(embed=command_help_embed)


class Help(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.emoji = "ℹ️"
        self.description = "Show information on bot's usage."
        help_command = OrioleHelp()
        help_command.cog = self
        bot.help_command = help_command


def setup(bot):
    bot.add_cog(Help(bot))
