# ==============================================
# Nexus Manager - Engine Core
# Desenvolvido por @079byfael • Frost Applications • UDO
# github.com/NextStore992/Bot-Manager---Beta-test
# ==============================================

from core.discloud import DiscloudAPI

class DiscloudEngine:
    """Engine principal para Discloud - UDO"""
    def __init__(self, api: DiscloudAPI):
        self.api = api

    async def list_apps(self):
        data = await self.api.list_apps()
        if "apps" in data:
            return [
                {
                    "id": app["id"],
                    "name": app["name"],
                    "status": app["status"],
                    "cpu": app.get("cpu", "N/A"),
                    "ram": app.get("ram", "N/A"),
                    "last_deploy": app.get("lastDeploy", "N/A")
                }
                for app in data["apps"]
            ]
        return []

    async def perform_action(self, app_id, action):
        return await self.api.app_action(app_id, action)

    async def fetch_logs(self, app_id):
        return await self.api.get_logs(app_id)