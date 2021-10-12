from datetime import datetime
import discord
import os
import traceback
from discord.ext import commands


class Oriole(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(
            command_prefix=".",
            description="An open source multipurpose discord bot.",
            heartbeat_timeout=150.0,
            intents=intents,
        )
        self._load_extensions()
        self.uptime = datetime.utcnow()
        self.owner_ids = {534820059965685770}
        self.repository = "https://github.com/Batucho/Oriole-DiscordBot"

    def _load_extensions(self) -> None:
        try:
            cogs_dir = os.listdir("./Oriole/cogs")
        except FileNotFoundError as e:
            cogs_dir = os.listdir("cogs")
        for filename in cogs_dir:
            if filename.endswith(".py"):
                cog = filename[:-3]
                try:
                    self.load_extension(f"cogs.{cog}")
                except Exception as e:
                    traceback.print_exc()

    async def on_ready(self) -> None:
        print(f"Bot Online! || {self.user} (ID: {self.user.id})")
