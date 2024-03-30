import asyncio
import datetime
import os

import discord
#import pomice
from discord.ext import commands
from dotenv import load_dotenv

from keep_alive import keep_alive

#.env files

load_dotenv()
    
TOKEN = os.environ.get("DISCORD_TOKEN")
OPENAI_T = os.environ.get("OPENAI")
OWNER_ID = os.environ.get("OWNER_ID")
APP_ID = os.environ.get("APP_ID")

keep_alive()


class LilRei(commands.Bot):
    def __init__(self):
        
        super().__init__(
            command_prefix='r!', #bot prefix
            help_command=None, 
            case_insensitive=True, 
            intents=discord.Intents.all(), 
            owner_ids=[409311773720576010, 1009848625108619355],
            application_id =APP_ID)

    async def on_ready(self):
        
        await self.wait_until_ready()
       # await self.cogs["Music"].start_nodes()
                      
#status

        status = f"Em {str(len(client.guilds))} servidores! Digite /help!" #Set this as your discord bot status

        activity = discord.Game(name= status, type= 3)
        await client.change_presence(status=discord.Status.online, activity=activity)

        syc = await self.tree.sync()
        print(f"Foram sincronizados {len(syc)} comandos.")

        print("Bot está pronto")


client = LilRei() #the bot client

##EVENTS


@client.event
async def on_connect():
    print(f" Connected to Discord (latency: {client.latency*1000:,.0f} ms).")


@client.event
async def on_resumed():
    print("Bot resumed.")


@client.event
async def on_disconnect():
    print("Bot disconnected.")



@client.event

# Respond if someone pings the bot!

async def on_message(message):
    
    if message.author.bot:
        return

    if isinstance(message.channel, discord.DMChannel):
        
        return ...

    if client.user.mentioned_in(message):
        if "@" not in message.content.lower():
            return ...

        elif ("everyone" or "here" ) in message.content.lower():
            return ...

        else:
            await message.channel.send(f"O meu prefixo padrão é `r!`") #Change the ! for the bot prefix
    else:
        await client.process_commands(message)


@client.event
async def on_guild_join(guild):
    
    servers = str(len(client.guilds))

    activity = discord.Game(name= f"Em {servers} servidores! Digite /help!", type= 3)
    await client.change_presence(status=discord.Status.online, activity=activity)



@client.event
async def on_guild_remove(guild):
    
    servers = str(len(client.guilds))

    activity = discord.Game(name= f"Em {servers} servidores! Digite /help!", type= 3)
    await client.change_presence(status=discord.Status.online, activity=activity)

    print("Status alterado com sucesso")





if __name__ == "__main__":

    #load the cogs method

    async def load_extensions():
        for files in os.listdir("./cogs"):
            if files.endswith(".py"):
                await client.load_extension(f"cogs.{files[:-3]}")
                print(f"Cog {files} carregada!")



    #main func to load the bot


    async def main():


        await load_extensions()
        await client.start(TOKEN, reconnect=True)


    asyncio.run(main())