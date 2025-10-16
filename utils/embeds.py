# ==============================================
# Nexus Manager - Embeds & Watermark
# Desenvolvido por @079byfael • Frost Applications • UDO Owner
# github.com/NextStore992/Bot-Manager---Beta-test
# ==============================================

import discord

WATERMARK = "🧊 Em desenvolvimento: @079byfael • Frost Applications • UDO"

def status_embed(title, description, color=discord.Color.blurple(), beta=True):
    embed = discord.Embed(
        title=f"{title} {'[BETA]' if beta else ''}",
        description=description,
        color=color
    )
    embed.set_footer(text=WATERMARK)
    return embed

def bot_status_emoji(status):
    mapping = {
        "online": "🟢",
        "offline": "🔴",
        "restarting": "🟡",
        "errored": "⚠️"
    }
    return mapping.get(status.lower(), "⚪")