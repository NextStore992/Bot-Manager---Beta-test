# =======================================
# Nexus Manager - Core Config Manager
# Desenvolvido por @079byfael • Frost Applications • UDO
# github.com/NextStore992/Bot-Manager---Beta-test
# =======================================

import aiosqlite
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "../data/database.db")

class ConfigManager:
    """Gerenciador de configuração e auditoria - UDO"""
    def __init__(self):
        self.db_path = DB_PATH

    async def init_db(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS guild_config (
                    guild_id INTEGER PRIMARY KEY,
                    engine TEXT DEFAULT "discloud",
                    log_channel INTEGER,
                    admin_role INTEGER
                )
            """)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS audit_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    guild_id INTEGER,
                    user_id INTEGER,
                    action TEXT,
                    target TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            await db.commit()

    async def get_guild_config(self, guild_id):
        async with aiosqlite.connect(self.db_path) as db:
            cur = await db.execute("SELECT * FROM guild_config WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            return row

    async def set_guild_config(self, guild_id, engine=None, log_channel=None, admin_role=None):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO guild_config (guild_id, engine, log_channel, admin_role)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(guild_id) DO UPDATE SET engine=excluded.engine, log_channel=excluded.log_channel, admin_role=excluded.admin_role
            """, (guild_id, engine, log_channel, admin_role))
            await db.commit()

    async def log_audit(self, guild_id, user_id, action, target):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO audit_log (guild_id, user_id, action, target)
                VALUES (?, ?, ?, ?)
            """, (guild_id, user_id, action, target))
            await db.commit()

    async def fetch_audit(self, guild_id, limit=20):
        async with aiosqlite.connect(self.db_path) as db:
            cur = await db.execute("""
                SELECT * FROM audit_log
                WHERE guild_id = ?
                ORDER BY timestamp DESC LIMIT ?
            """, (guild_id, limit))
            rows = await cur.fetchall()
            return rows