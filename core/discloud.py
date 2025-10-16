# ============================================
# Nexus Manager - Discloud API Core
# Desenvolvido por @079byfael • Frost Applications • UDO
# github.com/NextStore992/Bot-Manager---Beta-test
# ============================================

import aiohttp

class DiscloudAPI:
    """
    API Wrapper para Discloud
    Desenvolvido por @079byfael • Frost Applications • UDO Owner
    """
    def __init__(self, token):
        self.token = token
        self.base_url = "https://api.discloud.app/v2"

    async def request(self, method, endpoint, **kwargs):
        headers = {
            "Authorization": self.token,
            "Content-Type": "application/json"
        }
        url = f"{self.base_url}{endpoint}"
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, headers=headers, **kwargs) as resp:
                data = await resp.json()
                return data

    async def list_apps(self):
        return await self.request("GET", "/app")

    async def app_action(self, app_id, action):
        return await self.request("POST", f"/app/{app_id}/{action}")

    async def get_logs(self, app_id):
        return await self.request("GET", f"/app/{app_id}/logs")