import discord
import asyncio
import random as r

import os
from discord.ext import commands
from discord import guild, user
from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient

from easy_pil import Editor, load_image_async, Font

import functools

URI = os.environ.get("URI")

#func to connect to the database
def createData():
    uri = URI  
    mongocl = MongoClient(uri, server_api=ServerApi('1'))
    cursor = Money(mongocl.economy)
    return cursor


class NoMoney(commands.CommandError):
    pass

#class to manipulate the user/money easily
class Money:

    def __init__(self, db):
        self.db = db


    #DECORATOR   
    
    def checkMoney(self):
        def wrapper(func):
            @functools.wraps(func)
            async def wrapped(*args, **kwargs):

                money = self.getMoney(args[-1])
                ammount = int(kwargs["ammount"])

                if money < ammount or ammount <= 0: raise NoMoney

                return await func(*args, **kwargs)
            
            return wrapped
        return wrapper
    

    #GET MONEY
    
    def getMoney(self, user: discord.User):

        key = {"user": user.id}
        cur = self.db.money.find(key)
        try:
           
             cur.next()

        except Exception:
    
            self.db.money.insert_one(
                {
                "money": 0,
                "user": user,
                }
            )
        
        for i in self.db.money.find(key):
            money = i["money"]

        return int(money)

    
    #SET MONEY

    def setMoney(self, user: discord.User, ammount: int):
        
        key = {"user": user.id}
        update = {"$set": { "money": ammount }}
        self.db.money.update_one(key, update, True)


    #GET ALL USERS - LIMIT: QUANTITY TO DISPLAY
    
    def getAll(self, limit: int = 0):

        all = self.db.money.find().sort("money", -1).limit(limit)
        users = []
        for user in all:
            users.append(user)

        return users
    
    #BITESTHEDUST

    def resetAll(self):
        all = self.db.money.find()
        for user in all:
            update = {"$set": { "money": 0 }}
            self.db.money.update_one(user, update, True)

    #GETPOS - RETURN THE POSITION OF THE USER IN THE LEADERBOARD
            
        
    def getPos(self, user: discord.User)-> int:
        i = 1;

        all = self.db.money.find({}, {"user": 1}).sort("money", -1)
      
        for v in all:
            if int(v["user"]) == user.id:
                break

            i = i + 1


        return i;
    


class Economy(commands.Cog):

    def __init__(self, client, cursor):
        self.client = client
        self.cursor = cursor


    #BANK
        
    @commands.command(name = "bank", aliases=["atm", "bal", "money", "dinheiro"])
    async def _bank(self, ctx, user: discord.User = None):

        if user is None:
            user = ctx.author

        await ctx.send(f"> <@{user.id}> possui **{self.cursor.getMoney(user)}** lil coins! Posição no rank: **{self.cursor.getPos(user)}**")



    #SET MONEY

    @commands.command(name="setmoney")
    async def _setmoney(self, ctx, user: discord.User, ammount: int):

        if ctx.author.id != 409311773720576010:
            return ...
        

        self.cursor.setMoney(user, ammount)
        await ctx.send(f"**Novo valor da conta de <@{user.id}>:** {self.cursor.getMoney(user)}.")



    #DAILY


    @commands.command(name="daily")
    @commands.cooldown(1, 43200, commands.BucketType.user)
    async def _daily(self, ctx):
        
        money = self.cursor.getMoney(ctx.author)
        num = r.randint(1000, 3000)

        money = money+num
        self.cursor.setMoney(ctx.author, money)

        await ctx.send(f"**Parabéns <@{ctx.author.id}>**! Você ganhou *{num}* lil coins! Volte novamente em 12 horas para resgatar mais! _Sabia que poderia ganhar mais lil coins usando `r!vote`? Experimente!_")



    #PIX
    
    @commands.command(name="pix", aliases=["pagar", "transferir", "pay"])
    @Money.checkMoney(createData())
    async def _pix(self, ctx, paiduser: discord.User = None, *, ammount: int = None):
        
        if paiduser is None or ammount is None or paiduser.id == ctx.author.id:
            
            embed = discord.Embed(

                title = "`PIX`",
                description = "**ALIASES:** *pagar, transferir, pay*",
                color=0xa8326d,

            )
            embed.add_field(name="", value= "**Transfira suas lil coins para outro usuário!** Exemplo de comando: _r!pix <@1080924319250661456> 10000_")
            embed.set_footer(text= f"Solicitado por {ctx.author.display_name}", icon_url= ctx.author.avatar.url)
            return await ctx.send(embed=embed)
        

        embed = discord.Embed(
            title = "`PIX`",
            description = f"<@{ctx.author.id}>, você vai pagar {ammount} para <@{paiduser.id}>! **Confirme na reação para concluir a transferência!**",
            color=0xa8326d,
        )
        
        embed.set_footer(text= f"Solicitado por {ctx.author.display_name}", icon_url= ctx.author.avatar.url)
        message = await ctx.send(embed=embed)

        await message.add_reaction("✅")
        def check(r: discord.Reaction, u: discord.User):
            return u.id == ctx.author.id and r.message.channel.id == ctx.channel.id and \
                str(r.emoji) in ["\U00002705", "\U0000274c"]

        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout = 240, check=check)

        except asyncio.TimeoutError:
            return

        else:
            
            m1 = self.cursor.getMoney(ctx.author)
            m2 = self.cursor.getMoney(paiduser)

            m1 = m1 - ammount
            m2 = m2 + ammount

            self.cursor.setMoney(ctx.author, m1)
            self.cursor.setMoney(paiduser, m2)

            await ctx.send("**Transferência concluida!**")
    


    #owner- GETALL

    @commands.command(name="getall")
    async def _getall(self, ctx, limit:int = 0):

        if ctx.author.id != 409311773720576010:
            return ...
        
        i = self.cursor.getAll(limit)
        j = []
        for val in i:
            out = "<@{}>: {}\n".format(val["user"], val["money"])
            j.append(out)

        await ctx.send(f"".join(j))



    #RANK
    
    @commands.command(name="top", aliases=["rank"])
    async def _rank(self, ctx, embedst:bool = True):
        if embedst:

            all = self.cursor.getAll(5)
            st = []
            for val in all:
                out = "> **<@{}>**: {}\n".format(val["user"], val["money"])
                st.append(out)


            description = "".join(st)
            embed = discord.Embed(
                title="`RANK`",
                description=description,
                color=0xa8326d,
            )

            return await ctx.send(embed=embed)

        await ctx.send("**Em breve com imagem!**")



    #VOTE
        
    @commands.command(name="vote", aliases=["votar"])
    async def _vote(self, ctx):
        await ctx.author.send("link")
    ##                   cassino                     ##
        






    ##                    events                     ##
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, exc):
        if isinstance(exc, NoMoney):
            await ctx.reply("**Quantia inválida para a transferência! Verifique se foi digitado um número válido ou talvez você esteja meio... Pobre? 😅**")


async def setup(client):
    await client.add_cog(Economy(client, createData()))
