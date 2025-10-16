# =======================================
# Nexus Manager - Main Entrypoint
# Desenvolvido por @079byfael • Frost Applications • UDO Owner
# github.com/NextStore992/Bot-Manager---Beta-test
# =======================================

import os
import discord
from discord.ext import commands

# Para suporte a .env e ao Replit (secrets)
if os.path.exists(".env"):
    from dotenv import load_dotenv
    load_dotenv(".env")

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCLOUD_TOKEN = os.getenv("DISCLOUD_TOKEN")

if not DISCORD_TOKEN or not DISCLOUD_TOKEN:
    raise RuntimeError("Tokens não encontrados! Defina DISCORD_TOKEN e DISCLOUD_TOKEN em Secrets do Replit ou no .env.")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)
bot.config = {
    "DISCORD_TOKEN": DISCORD_TOKEN,
    "DISCLOUD_TOKEN": DISCLOUD_TOKEN
}

COGS = [
    "cogs.dashboard",
    "cogs.config",
    "cogs.monitor",
    "cogs.audit",
]

async def load_cogs():
    for cog in COGS:
        await bot.load_extension(cog)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

async def main():
    await load_cogs()
    await bot.start(DISCORD_TOKEN)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())