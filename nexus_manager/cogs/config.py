# ========================================
# Nexus Manager - Config Cog
# Desenvolvido por @079byfael • Frost Applications • UDO Owner
# github.com/NextStore992/Bot-Manager---Beta-test
# ========================================

import discord
from discord import app_commands
from discord.ext import commands
from core.config_manager import ConfigManager
from utils.embeds import status_embed

class ConfigCog(commands.Cog):
    """Cog de configuração do Nexus Manager (UDO)"""
    def __init__(self, bot):
        self.bot = bot
        self.cfg = ConfigManager()

    @app_commands.command(name="config-system", description="Configura engine, canal de logs e permissões")
    @app_commands.describe(engine="Nome da engine", log_channel="Canal de logs", admin_role="Cargo administrador")
    async def config_system(self, interaction: discord.Interaction, engine: str, log_channel: discord.TextChannel, admin_role: discord.Role):
        await self.cfg.init_db()
        await self.cfg.set_guild_config(interaction.guild.id, engine, log_channel.id, admin_role.id)
        embed = status_embed("⚙️ Sistema configurado", f"Engine: {engine}\nLog Channel: {log_channel.mention}\nAdmin Role: {admin_role.mention}")
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(ConfigCog(bot))