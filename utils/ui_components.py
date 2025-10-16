# ============================================
# Nexus Manager - Dashboard UI Components
# Desenvolvido por @079byfael • Frost Applications • UDO
# github.com/NextStore992/Bot-Manager---Beta-test
# ============================================

import discord
from utils.embeds import status_embed, bot_status_emoji, WATERMARK

class DashboardView(discord.ui.View):
    """View principal do Dashboard interativo Nexus Manager.
    Desenvolvedor: @079byfael • Frost Applications • UDO Owner
    """
    def __init__(self, engine, apps, author=None, page=0):
        super().__init__(timeout=300)
        self.engine = engine
        self.apps = apps
        self.page = page
        self.page_size = 5
        self.author = author
        self.current_app = None
        self.refresh_items()

    def refresh_items(self):
        self.clear_items()
        paginated = self.apps[self.page*self.page_size:(self.page+1)*self.page_size]
        for app in paginated:
            label = f"{app['name']} {bot_status_emoji(app['status'])}"
            button = discord.ui.Button(
                label=label,
                custom_id=f"select_{app['id']}",
                style=discord.ButtonStyle.blurple
            )
            # Discord ainda não suporta tooltips nativamente, mas deixamos o campo para futuro
            self.add_item(button)
        if len(self.apps) > self.page_size:
            if self.page > 0:
                self.add_item(discord.ui.Button(label="⏪ Anterior", style=discord.ButtonStyle.gray, custom_id="prev"))
            if (self.page+1)*self.page_size < len(self.apps):
                self.add_item(discord.ui.Button(label="Próxima ⏩", style=discord.ButtonStyle.gray, custom_id="next"))
        self.add_item(discord.ui.Button(label="🔄 Atualizar", style=discord.ButtonStyle.green, custom_id="refresh"))
        self.add_item(discord.ui.Button(label="❌ Encerrar", style=discord.ButtonStyle.red, custom_id="close"))
        self.add_item(discord.ui.Button(label="ℹ Sobre", style=discord.ButtonStyle.secondary, custom_id="about"))

    async def interaction_check(self, interaction):
        if self.author:
            return interaction.user.id == self.author.id
        return True

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True

    async def interaction_handler(self, interaction: discord.Interaction):
        cid = interaction.data["custom_id"]
        if cid.startswith("select_"):
            app_id = cid.split("_")[1]
            app = next((a for a in self.apps if a["id"] == app_id), None)
            self.current_app = app
            embed = status_embed(
                f"⚙ {app['name']}",
                f"Status: {bot_status_emoji(app['status'])} {app['status'].capitalize()}\nCPU: {app['cpu']} | RAM: {app['ram']}\nÚltimo Deploy: {app['last_deploy']}",
                color=discord.Color.green() if app['status']=="online" else discord.Color.red()
            )
            self.clear_items()
            self.add_item(discord.ui.Button(label="Start", style=discord.ButtonStyle.success, custom_id=f"start_{app_id}"))
            self.add_item(discord.ui.Button(label="Stop", style=discord.ButtonStyle.danger, custom_id=f"stop_{app_id}"))
            self.add_item(discord.ui.Button(label="Restart", style=discord.ButtonStyle.primary, custom_id=f"restart_{app_id}"))
            self.add_item(discord.ui.Button(label="Logs", style=discord.ButtonStyle.secondary, custom_id=f"logs_{app_id}"))
            self.add_item(discord.ui.Button(label="Configurar", style=discord.ButtonStyle.secondary, custom_id=f"config_{app_id}"))
            self.add_item(discord.ui.Button(label="🔄 Atualizar", style=discord.ButtonStyle.green, custom_id="refresh"))
            self.add_item(discord.ui.Button(label="⬅ Voltar", style=discord.ButtonStyle.gray, custom_id="back"))
            self.add_item(discord.ui.Button(label="❌ Encerrar", style=discord.ButtonStyle.red, custom_id="close"))
            await interaction.response.edit_message(embed=embed, view=self)
        elif cid == "refresh":
            self.apps = await self.engine.list_apps()
            self.refresh_items()
            embed = status_embed("🔄 Atualizado", f"{len(self.apps)} bots carregados.")
            await interaction.response.edit_message(embed=embed, view=self)
        elif cid == "back":
            self.current_app = None
            self.refresh_items()
            embed = status_embed("📊 Nexus Manager", "Selecione um bot abaixo para gerenciar:")
            await interaction.response.edit_message(embed=embed, view=self)
        elif cid == "close":
            await interaction.response.edit_message(content="❌ Painel encerrado.", embed=None, view=None)
        elif cid == "prev":
            self.page -= 1
            self.refresh_items()
            embed = status_embed("📊 Nexus Manager", "Página anterior dos bots.")
            await interaction.response.edit_message(embed=embed, view=self)
        elif cid == "next":
            self.page += 1
            self.refresh_items()
            embed = status_embed("📊 Nexus Manager", "Próxima página dos bots.")
            await interaction.response.edit_message(embed=embed, view=self)
        elif cid.startswith(("start_", "stop_", "restart_")):
            action = cid.split("_")[0]
            app_id = cid.split("_")[1]
            result = await self.engine.perform_action(app_id, action)
            embed = status_embed("✅ Ação executada", f"{action.capitalize()} executado no bot {app_id}.")
            await interaction.response.edit_message(embed=embed, view=self)
        elif cid.startswith("logs_"):
            app_id = cid.split("_")[1]
            logs = await self.engine.fetch_logs(app_id)
            embed = status_embed("📜 Logs", f"```{logs.get('logs', 'Sem logs.')[:1500]}```\n[Ver completo no painel Discloud]", color=discord.Color.yellow())
            self.clear_items()
            self.add_item(discord.ui.Button(label="⬅ Voltar", style=discord.ButtonStyle.gray, custom_id="back"))
            self.add_item(discord.ui.Button(label="❌ Encerrar", style=discord.ButtonStyle.red, custom_id="close"))
            await interaction.response.edit_message(embed=embed, view=self)
        elif cid == "about":
            embed = discord.Embed(
                title="ℹ Sobre o Nexus Manager",
                description=(
                    "Dashboard visual para gestão de bots no Discord.\n"
                    "Desenvolvido por **@079byfael**\n"
                    "Empresa: **Frost Applications**\n"
                    "Selo: **UDO - Ultimate Developer Owner**\n"
                    "Status: **BETA**\n"
                    "GitHub: https://github.com/NextStore992\n"
                    "\nPainel em desenvolvimento — feedbacks são bem-vindos!"
                ),
                color=discord.Color.blue()
            )
            embed.set_footer(text=WATERMARK)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif cid.startswith("config_"):
            await interaction.response.send_message("Configuração não implementada ainda.", ephemeral=True)