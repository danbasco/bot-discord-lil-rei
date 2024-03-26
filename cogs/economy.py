import discord
import asyncio
import random as r

import os
from discord.ext import commands
from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient


URI = os.environ.get("URI")

# Func to connect to the database
def createData():
    uri = URI  
    mongocl = MongoClient(uri, server_api=ServerApi('1'))
    cursor = Money(mongocl.economy)
    return cursor


class NoMoney(commands.CommandError):
    pass

class NoMoneyUS(commands.CommandError):
    pass


# Class to manipulate the money/user easily

import discord
import functools
from discord.ext import commands

class Money:

    def __init__(self, db):
        self.db = db


    # Decorator 
    
    def checkMoney(self, checku: bool = False):
        def wrapper(func):
            @functools.wraps(func)
            async def wrapped(*args, **kwargs):

                if args[1] is None or args[-1] is None:
                    pass
                
                else:
                    money = self.getMoney(args[1].author)
                    ammount = int(kwargs["ammount"])

                    print(kwargs)
                    print(args)

                    
                    if checku is True:
                        money2 = self.getMoney(args[-1])
                        if money2 < ammount: raise NoMoneyUS
                    
                    if money < ammount or ammount <= 0: raise NoMoney

                return await func(*args, **kwargs)
            
            return wrapped
        return wrapper
    

    # Get Money
    
    def getMoney(self, user: discord.User) ->int:

        key = {"user": user.id}
        cur = self.db.money.find(key)
        try:
           
            cur.next()

        except Exception:
    
            self.db.money.insert_one(
                {
                "money": 0,
                "user": user.id,
                }
            )
        
        for i in self.db.money.find(key):
            money = i["money"]

        return int(money)

    
    # Set Money

    def setMoney(self, user: discord.User, ammount: int):
        
        key = {"user": user.id}
        update = {"$set": { "money": ammount }}
        self.db.money.update_one(key, update, True)


    # Get All, Limit- Number of users to search
    
    def getAll(self, limit: int = 0):

        all = self.db.money.find().sort("money", -1).limit(limit)
        users = []
        for user in all:
            users.append(user)

        return users
    
    #Reset All

    def resetAll(self):
        all = self.db.money.find()
        for user in all:
            update = {"$set": { "money": 0 }}
            self.db.money.update_one(user, update, True)


    # GetPos - Position in the leaderboard
            
        
    def getPos(self, user: discord.User)-> int:
        i = 1;

        all = self.db.money.find({}, {"user": 1}).sort("money", -1)
      
        for v in all:
            if int(v["user"]) == user.id:
                break

            i = i + 1


        return i;
    

    # ChangeValues
    
    
    async def changeValues(self, user: discord.User, paiduser: discord.User, ammount: int):
        
        m1 = self.getMoney(user)
        m2 = self.getMoney(paiduser)

        m1 = m1 - ammount
        m2 = m2 + ammount

        if m1 < 0:
            m1 = 0
            self.setMoney(paiduser, self.getMoney(user))
        else:
            self.setMoney(paiduser, m2)
            self.setMoney(user, m1)
            
        

class NoMoney(commands.CommandError):
    pass

class NoMoneyUS(commands.CommandError):
    pass

class Economy(commands.Cog):

    def __init__(self, client, cursor):
        self.client = client
        self.cursor = cursor


    # Bank
        
    @commands.command(name = "bank", aliases=["atm", "bal", "money", "dinheiro"])
    async def _bank(self, ctx, user: discord.User = None):

        if user is None:
            user = ctx.author

        await ctx.send(f"> <@{user.id}> possui **{self.cursor.getMoney(user)}** rei coins! Posição no rank: **{self.cursor.getPos(user)}**")



    # Setmoney

    @commands.command(name="setmoney")
    async def _setmoney(self, ctx, user: discord.User, ammount: int):

        if ctx.author.id != 409311773720576010 and ctx.author.id != 1009848625108619355:
            return ...
        

        self.cursor.setMoney(user, ammount)
        await ctx.send(f"**Novo valor da conta de <@{user.id}>:** {self.cursor.getMoney(user)}.")



    # Daily


    @commands.command(name="daily")
    @commands.cooldown(1, 43200, commands.BucketType.user)
    async def _daily(self, ctx):
        
        money = self.cursor.getMoney(ctx.author)
        num = r.randint(1000, 3000)

        money = money+num
        self.cursor.setMoney(ctx.author, money)

        await ctx.send(f"**Parabéns <@{ctx.author.id}>**! Você ganhou *{num}* rei coins! Volte novamente em 12 horas para resgatar mais! _Sabia que poderia ganhar mais rei coins usando `r!vote`? Experimente!_")



    # Pix
    
    @commands.command(name="pix", aliases=["pagar", "transferir", "pay"])
    @Money.checkMoney(createData())
    async def _pix(self, ctx, paiduser: discord.User = None, *, ammount: int = None):
        
        if paiduser is None or ammount is None or paiduser.id == ctx.author.id:
            
            embed = discord.Embed(

                title = "`PIX`",
                description = "**ALIASES:** *pagar, transferir, pay*",
                color=0xa8326d,

            )
            embed.add_field(name="", value= "**Transfira suas rei coins para outro usuário!** Exemplo de comando: _r!pix <@1080924319250661456> 10000_")
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
            
            self.cursor.changeValues(ctx.author, paiduser, ammount)
            await ctx.send("**Transferência concluida!**")
    


    # Getall

    @commands.command(name="getall")
    async def _getall(self, ctx, limit:int = 0):

        if ctx.author.id != 409311773720576010 or ctx.author.id != 1009848625108619355:
            return ...
        
        i = self.cursor.getAll(limit)
        j = []
        for val in i:
            out = "<@{}>: {}\n".format(val["user"], val["money"])
            j.append(out)

        await ctx.send(f"".join(j))



    # Rank
    
    @commands.command(name="top", aliases=["rank"])
    async def _rank(self, ctx, embedst:bool = True):
        if embedst:

            all = self.cursor.getAll(5)
            st = []
            i = 1
            for val in all:
                out = "> **`#{}`: <@{}>** // _{} rei coins!_\n".format(i, val["user"], val["money"])
                st.append(out)
                i += 1


            description = "".join(st)
            embed = discord.Embed(
                title="`RANK`",
                description=description,
                color=0xa8326d,
            )

            return await ctx.send(embed=embed)

        await ctx.send("**Em breve com imagem!**")



    # Vote
    
    '''
    @commands.command(name="vote", aliases=["votar"])
    async def _vote(self, ctx):
        await ctx.author.send("link")
    '''

    # MadeinHeaven

    @commands.command(name="madeinheaven")
    async def _madeinheaven(self, ctx):

        if ctx.author.id != 409311773720576010 or ctx.author.id != 1009848625108619355:
            return await ctx.send("https://media1.tenor.com/m/2gyEEp_NdYAAAAAd/made-in-heaven-jojo.gif")
        
        else:
            
            def check(message):
                return message.author == ctx.author and message.content == 'confirmar'
                
            try: 
                message = await self.client.wait_for("message", timeout=10, check=check)
    
            except asyncio.TimeoutError:
                await ctx.send("Tempo esgotado!")
            else:
            
                self.cursor.resetAll()
                await ctx.send("https://media1.tenor.com/m/2gyEEp_NdYAAAAAd/made-in-heaven-jojo.gif")
            


    ##                   cassino                     ##
        


    # CoinFlip
    @commands.command(name="coinflip", aliases=["caraoucoroa", "50/50"])
    @Money.checkMoney(createData(), True)
    async def _coinflip(self, ctx, paiduser: discord.User = None, *, ammount: int = None):
        
        if paiduser is None or ammount is None or paiduser.id == ctx.author.id:
            
            embed = discord.Embed(

                title = "`COINFLIP`",
                description = "**ALIASES:** *caraoucoroa*",
                color=0xa8326d,

            )
            embed.add_field(name="", value= "**Acha que estás com sorte? **Por que não apostar então?** Marque seu amigo e coloque as rei coins em jogo! O jogador que chama a aposta será sempre a cara, e o que aceita, coroa! \n\n**Exemplo de comando:** _r!coinflip <@1080924319250661456> 10000_\n\n**")
            embed.set_footer(text= f"Solicitado por {ctx.author.display_name}", icon_url= ctx.author.avatar.url)
            return await ctx.send(embed=embed)

        embed = discord.Embed(
            title = "`COINFLIP`",
            description = f"**> 🪙 | <@{ctx.author.id}> Está fazendo uma aposta contra <@{paiduser.id}> no valor de {ammount} rei coins!** \nCada usuário tem 50% de chances de ganhar!\n\nPara fazer a aposta, **<@{paiduser.id}> precisa confirmar na reação!**",
            color=0xa8326d,
        )
        embed.set_footer(text= f"Solicitado por {ctx.author.display_name}", icon_url= ctx.author.avatar.url)
        message = await ctx.send(embed=embed)


        await message.add_reaction("✅")
        def check(r: discord.Reaction, u1: discord.User):
            return u1.id == paiduser.id and r.message.channel.id == ctx.channel.id and \
                str(r.emoji) in ["\U00002705", "\U0000274c"]


        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout = 100, check=check)

        except asyncio.TimeoutError:
            return

        else:
            
            rand = r.randint(0, 1) # O 0 é cara, 1 é coroa

            if rand == 0:
                await ctx.send(f"> **🪙 | Cara!** <@{ctx.author.id}> venceu!")

                self.cursor.changeValues(ctx.author, paiduser, ammount)

            if rand == 1:
                await ctx.send(f"> **🪙 | Coroa!** <@{paiduser.id}> venceu!")

                self.cursor.changeValues(paiduser, ctx.author, ammount)




    ##                    global                     ##
                











    ##                    events                     ##
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, exc):
        if isinstance(exc, NoMoney):
            await ctx.reply("**Quantia inválida para a transferência! Verifique se foi digitado um número válido ou talvez você esteja meio... Pobre? 😅**")
        
        if isinstance(exc, NoMoneyUS):
            await ctx.reply("**O usuário mencionado não tem dinheiro o suficiente para esse comando!!**")

async def setup(client):
    await client.add_cog(Economy(client, createData()))
