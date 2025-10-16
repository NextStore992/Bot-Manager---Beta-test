# ========================================
# Nexus Manager - Checks
# Desenvolvido por @079byfael • Frost Applications • UDO
# github.com/NextStore992/Bot-Manager---Beta-test
# ========================================

from discord.ext import commands

def admin_only():
    async def predicate(ctx):
        if ctx.guild is None:
            return False
        admin_role_id = ctx.bot.cfg.get("admin_role")
        if admin_role_id is None:
            return ctx.author.guild_permissions.administrator
        role = ctx.guild.get_role(admin_role_id)
        return role in ctx.author.roles
    return commands.check(predicate)