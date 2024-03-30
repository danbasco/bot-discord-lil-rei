import requests
import os
from discord.ext import commands
from discord import app_commands

class RenderAPI:

    def __init__(self) -> None:
        self.serviceid = os.environ.get("SERVICE_ID")
        self.rendertoken = os.environ.get("RENDER_T")


        self.url = f"https://api.render.com/v1/services/{self.serviceid}/deploys"

    def Trigger(self) -> str:
        
        payload = { "clearCache": "do_not_clear" }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.rendertoken}"
        }

        response = requests.post(self.url, json=payload, headers=headers)

        return response.text["commit"]
    

class Render(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client

    @commands.command(name="deploy")
    @commands.is_owner()
    async def _deploy(self, ctx):
        await ctx.reply("Reiniciando...")

        channel = ctx.bot.get_channel(890021283759276064)
        await channel.send("> **Status do bot:** _Reiniciando... 🔄️_")
        reason  = RenderAPI.Trigger()

        print(reason)


async def setup(client):
    await client.add_cog(Render(client))