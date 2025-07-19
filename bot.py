import discord
from discord import app_commands
import os

class MyClient(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        @self.tree.command(
            name="message",
            description="Send a customized embed message"
        )
        @app_commands.describe(
            title="The title of the embed",
            description="The main content of the message",
            color="Hex color code (e.g., #FF0000)",
            image="Image URL",
            thumbnail="Thumbnail URL"
        )
        async def message_command(interaction: discord.Interaction,
                                  title: str,
                                  description: str,
                                  color: str = "#0099ff",
                                  image: str = None,
                                  thumbnail: str = None):
            try:
                color_int = int(color.lstrip("#"), 16)
            except ValueError:
                await interaction.response.send_message("❌ Invalid hex color!", ephemeral=True)
                return

            embed = discord.Embed(title=title, description=description, color=color_int)
            if image:
                embed.set_image(url=image)
            if thumbnail:
                embed.set_thumbnail(url=thumbnail)
            await interaction.response.send_message(embed=embed)

        await self.tree.sync()
        print("✅ Slash command registered")

    async def on_ready(self):
        print(f"✅ Logged in as {self.user} (ID: {self.user.id})")

client = MyClient()
token = os.environ.get("DISCORD_TOKEN")
if not token:
    raise RuntimeError("DISCORD_TOKEN environment variable is required")
client.run(token)