# ========================================
# Nexus Manager - Audit Cog
# Desenvolvido por @079byfael • Frost Applications • UDO Owner
# github.com/NextStore992/Bot-Manager---Beta-test
# ========================================

import discord
from discord import app_commands
from discord.ext import commands
from core.config_manager import ConfigManager
from utils.embeds import status_embed

class AuditCog(commands.Cog):
    """Cog de auditoria do Nexus Manager (UDO)"""
    def __init__(self, bot):
        self.bot = bot
        self.cfg = ConfigManager()

    @app_commands.command(name="audit", description="Mostra logs de ações (histórico)")
    async def audit(self, interaction: discord.Interaction):
        await self.cfg.init_db()
        logs = await self.cfg.fetch_audit(interaction.guild.id)
        description = "\n".join([f"{l[4]} — <@{l[2]}> [{l[3]}] ({l[5]})" for l in logs]) or "Nenhuma ação registrada."
        embed = status_embed("📜 Audit Log", description)
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(AuditCog(bot))