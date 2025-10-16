# ========================================
# Nexus Manager - Monitor Cog
# Desenvolvido por @079byfael • Frost Applications • UDO Owner
# github.com/NextStore992/Bot-Manager---Beta-test
# ========================================

import discord
from discord import app_commands
from discord.ext import commands
from core.engine import DiscloudEngine
from core.discloud import DiscloudAPI
from utils.embeds import status_embed

class MonitorCog(commands.Cog):
    """Cog de monitoramento do Nexus Manager (UDO)"""
    def __init__(self, bot):
        self.bot = bot
        self.engine = DiscloudEngine(DiscloudAPI(token=self.bot.config.get("DISCLOUD_TOKEN", "")))

    @app_commands.command(name="monitor", description="Ver estatísticas globais e saúde das engines")
    async def monitor(self, interaction: discord.Interaction):
        apps = await self.engine.list_apps()
        status_summary = "\n".join([f"{app['name']}: {app['status']} (CPU: {app['cpu']} | RAM: {app['ram']})" for app in apps])
        embed = status_embed("📈 Estatísticas Globais", status_summary)
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(MonitorCog(bot))