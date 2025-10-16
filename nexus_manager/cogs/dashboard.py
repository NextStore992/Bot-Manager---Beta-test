# ========================================
# Nexus Manager - Dashboard Cog
# Desenvolvido por @079byfael • Frost Applications • UDO Owner
# github.com/NextStore992/Bot-Manager---Beta-test
# ========================================

import discord
from discord import app_commands
from discord.ext import commands
from utils.ui_components import DashboardView
from core.config_manager import ConfigManager
from core.engine import DiscloudEngine
from core.discloud import DiscloudAPI
from utils.embeds import status_embed

class DashboardCog(commands.Cog):
    """Cog do painel interativo Nexus Manager (UDO)"""
    def __init__(self, bot):
        self.bot = bot
        self.cfg = ConfigManager()
        self.discloud = DiscloudEngine(DiscloudAPI(token=self.bot.config.get("DISCLOUD_TOKEN", "")))

    @app_commands.command(name="dashboard", description="Abrir painel visual de gerenciamento")
    async def dashboard(self, interaction: discord.Interaction):
        await self.cfg.init_db()
        apps = await self.discloud.list_apps()
        embed = status_embed("📊 Nexus Manager", "Selecione um bot abaixo para gerenciar:")
        view = DashboardView(self.discloud, apps, author=interaction.user)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.data and interaction.data.get("component_type") == 2:
            for view in interaction.message.components:
                if isinstance(view, DashboardView):
                    await view.interaction_handler(interaction)
                    break

async def setup(bot):
    await bot.add_cog(DashboardCog(bot))