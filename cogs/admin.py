import discord
##This cog was made for organizing special commands for the bot, usually admin commands or other useful stuff that i dont include as AI commands or Music commands

from datetime import datetime
from inspect import Arguments
from os import name
from discord import guild, user
from discord.ext.commands import has_permissions
from discord.ext import commands
from discord.ext.commands.errors import CommandError

import asyncio


class NotInRole(commands.CommandError):
    pass

class AlreadyInRole(commands.CommandError):
    pass

class ChannelAlreadyLocked(commands.CommandError):
    pass

class ChannelAlreadyUnlocked(commands.CommandError):
    pass

class MemberNotFound(commands.CommandError):
    pass

class SelfMentioned(commands.CommandError):
    pass

class OnTop(commands.CommandError):
    pass

class NoPerm(commands.CommandError):
    pass




class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client


#COMMANDS

    #PURGE

    @commands.command(name="purge")
    @has_permissions(administrator= True)
    async def _purge(self, ctx, amount=None):
        
        
        if amount is None:
           return await ctx.send("Especifique uma quantidade para limpar!")
        
        try:
            int(amount)
        except:
            await ctx.send("O valor inserído é inválido!")
        else:
            if int(amount) > 1000:
                await ctx.send("O valor inserido tem que estar entre 1 e 1000!")
            else:
                await ctx.channel.purge(limit=int(amount))
                await ctx.send(f"{amount} mensagens foram deletadas!")
  
    
    
    #NUKE


    @commands.command(name="nuke")
    @has_permissions(administrator= True)
    async def _nuke(self, ctx):

        await ctx.reply("**__Digite confirmar para deletar o canal!__**")

        channel = ctx.channel
                
        def check(message):
            return message.author == ctx.author and message.content == 'confirmar' and message.channel == channel
                
        try: 
            message = await self.client.wait_for("message", timeout=10, check=check)
    
        except asyncio.TimeoutError:
            await ctx.send("Tempo esgotado!")
        else:
            await channel.clone(reason= "Nuke Channel")
            await channel.delete()


    #INVITE


    @commands.command(name="invite", aliases=["convite"])
    async def _invite(self, ctx):

        embed = discord.Embed(
                title="`Invite`",
                description=f"",
                color=0xa8326d,
            )
        embed.add_field(name="", value= "Gostaria de adicionar a **Lil Rei** no seu servidor?\nIsso ficou fácil, basta clicar [aqui!](https://discord.com/api/oauth2/authorize?client_id=1080924319250661456&permissions=8&scope=applications.commands%20bot)")
        embed.set_image(url="https://cdn.discordapp.com/avatars/1080924319250661456/d824459f3f40dacac1357c1d4c00ceb3.png?size=2048")
        embed.set_footer(text= "Lil Rei • © Todos os direitos reservados.")
        await ctx.send(embed=embed)
    


    #BAN 

    @commands.command(name="ban")
    @has_permissions(ban_members=True)
    async def _ban(self, ctx, pingued: discord.Member = None, *, reason = None):
        
        if pingued is None:
            raise MemberNotFound

        if pingued is ctx.message.author:
            raise SelfMentioned

        if ctx.author.top_role <= pingued.top_role:
            raise OnTop
        


        message = await ctx.reply(f"**Deseja mesmo banir o usuário <@{pingued.id}>? Reaja na mensagem para banir o usuário.**")
        await message.add_reaction("✅")


        channel = ctx.channel
                
        def check(r: discord.Reaction, u: discord.User):
            return u.id == ctx.author.id and r.message.channel.id == ctx.channel.id and \
               str(r.emoji) in ["\U00002705", "\U0000274c"]
                
        try: 
            reaction, user = await self.client.wait_for('reaction_add', timeout=10, check=check)
    
        except asyncio.TimeoutError:
            await ctx.send("Tempo esgotado!")
            return
        
        else:
            embed = discord.Embed(
                title = "Ban",
                description= f"**__{pingued}__** foi banido do servidor",
                color=0xa8326d,
                )

            embed.set_footer(text= f"Solicitado por **{ctx.author.display_name}**", icon_url= ctx.author.avatar.url)
            embed.set_image(url=pingued.avatar.url)

            await ctx.send(embed=embed)
            await pingued.ban(reason=reason)
            await ctx.delete()
        
          



    #AVATAR
    

    @commands.command(name="avatar")
    async def _avatar(self, ctx, *, user: discord.Member = None):

        
        if user is None:
            user = ctx.message.author
        
        
        embed = discord.Embed(
            title= f"{user.display_name}",
            description= f"Clique [aqui]({user.avatar.url}) para baixar a imagem",
            color=0xa8326d,
        )
            
        embed.set_footer(text= f"Solicitado por {ctx.author.display_name}", icon_url= ctx.author.avatar.url)
        embed.set_image(url=user.avatar.url)
        

        await ctx.send(embed=embed)
        

    #MUTE
    
    @commands.command(name="mute", aliases=["mutar", "silenciar"])
    @has_permissions(kick_members= True)
    async def _mute(self, ctx, user: discord.User = None):

        if user is None:
            raise MemberNotFound

        if user is ctx.message.author:
            raise SelfMentioned

        if ctx.author.top_role < user.top_role:
            raise OnTop
        


        guild = ctx.guild
        role = discord.utils.get(guild.roles, name="Silenciado")

        if role in user.roles:
            raise AlreadyInRole
        
        if role not in guild.roles:
            
            await guild.create_role(name= "Silenciado")

            for channel in guild.channels:
                role = discord.utils.get(guild.roles, name="Silenciado")
                await channel.set_permissions(role, send_messages=False)
         
        else:
            ...

        await user.add_roles(role)
        embed = discord.Embed(
            title="Silenciado",
            description=f"**O usuário {user} foi silenciado por {ctx.message.author}**",
            colour=0xa8326d,
        )
        embed.set_footer(text= f"Solicitado por {ctx.author.display_name}", icon_url= ctx.author.avatar.url)

        await ctx.send(embed=embed)      



    #KICK


    
    @commands.command(name = "kick", aliases= ["expulsar"])
    @has_permissions(kick_members=True)
    async def _kick(self, ctx, member: discord.Member, *, reason=None):
        
        if member is ctx.message.author:
            raise SelfMentioned

        if ctx.author.top_role < member.top_role:
            raise OnTop
        
        await member.kick(reason=reason)

        embed = discord.Embed(
            title="Kick",
            description=f"O usuário {member} foi expulso do servidor!",
            colour=0xa8326d,

        )
        embed.set_footer(text= f"Solicitado por **{ctx.author.display_name}**", icon_url= ctx.author.avatar.url)
        embed.set_image(url=user.avatar.url)

        if reason is not None:
            embed.add_field(name= "Motivo:", value= reason)
            return await ctx.send(embed=embed)

        await ctx.send(embed=embed)

    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, exc):

        if isinstance(exc, commands.MissingPermissions):
            await ctx.reply("**Você não tem permissão para executar esse comando!**")
            
        if isinstance(exc, commands.CommandNotFound):
            await ctx.reply(f"O comando não foi encontrado!")

        if isinstance(exc, AlreadyInRole):
            await ctx.reply("O usuário já está mutado!")

        if isinstance(exc, NotInRole):
            await ctx.reply("O usuário não está mutado!")

        if isinstance(exc, ChannelAlreadyLocked):
            await ctx.reply("O canal já está bloqueado! **Utilize `rei!unlock` para desbloquear!**")

        if isinstance(exc, ChannelAlreadyUnlocked):
            await ctx.reply("O canal já está desbloqueado!")

        if isinstance(exc, MemberNotFound):
            await ctx.reply("Não foi possível encontrar o usuário! Verifique se foi digitado corretamente")

        if isinstance(exc, SelfMentioned):
            await ctx.reply("Você não pode mencionar a si mesmo!")    
        
        if isinstance(exc, OnTop):
            await ctx.reply("Você não tem permissão para executar esse comando!") 

        if isinstance(exc, commands.CommandOnCooldown):
            await ctx.reply("**O tempo para usar o daily ainda não passou!** Você pode usar o comando a cada 12 horas, fique atento!")
        else:
            print(exc)


async def setup(client):
    await client.add_cog(Admin(client))











'''
class button_view(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
    
    

    @discord.ui.button(label="⚫", style=discord.ButtonStyle.grey, custom_id="black")
    async def black(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        role = 1210351283395887185

        if role in [y.id for y in interaction.user.roles]:
            await interaction.user.remove_roles(interaction.user.guild.get_role(role))
            await interaction.response.send_message(f"Removido o cargo <@&{role}>!", ephemeral=True)
        else:
            await interaction.user.add_roles(interaction.user.guild.get_role(role))
            await interaction.response.send_message(f"Adicionado o cargo <@&{role}>!", ephemeral=True)


    @commands.command(name="color")
    async def _color(self, ctx):
        embed = discord.Embed(
                title="─────────────────   ‧     ‹  🎨 Cores 🎨  ›     ‧    ─────────────────",
                description=f"",
                color=0xa8326d,
            )
        embed.add_field(name="", value= "Escolha uma cor de sua preferência para usar em seu nickname, ele servirá para deixar seu perfil mais bonito no chat! E, além disso, receba um ícone que fica ao lado de seu nickname, correspondente a cor adquirida!")

        embed.set_footer(text= "Lil Rei • © Todos os direitos reservados.")


        await ctx.send(embed=embed, view=button_view())

    
'''