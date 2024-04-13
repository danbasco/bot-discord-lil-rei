import discord
from discord.ext import commands
from discord import app_commands

class Help(commands.Cog):

    def __init__(self, client) ->  None:
        self.client = client

    @commands.command(name="help")
    async def _help(self, ctx):

        embed1 = discord.Embed(
                title="Lil Rei",
                description= f"Oi, eu sou a Lil Rei! Um bot divertido de **economia, administração e outros comandos que virão em breve!**\nEstarei sempre crescendo e progredindo, então se tiver algum erro ou dúvida, não tenha medo de compartilhar e ajudar, assim eu posso ser uma versão melhor de mim mesma! Espero que se divirta, pois fui criada com muito amor e carinho <3\n\nGostaria de dar uma olhada meu código! É open source, 100% feito em **Python!** Basta clicar [aqui!](https://github.com/danbasco/rei)\n\nServidores oficiais da Lil Rei:\n -  [Saturn](https://discord.gg/saturnday)\n-  [Lil Rei's Kingdom (Suporte)](https://discord.gg/BhrEWubvdz)",
                color=0xa8326d,
            )
            #embed.add_field(name="Help", value="Digite /help ADMIN para ver os comandos de utilidade/administração.\n\nDigite /help ECONOMY para os comandos de economia.")
        embed1.set_image(url="https://cdn.discordapp.com/avatars/1080924319250661456/d824459f3f40dacac1357c1d4c00ceb3.png?size=2048")
        embed1.set_footer(text= "Lil Rei • © Todos os direitos reservados.")

        embed2 = discord.Embed(
                title="ADMIN",
                description= f" ",
                color=0xa8326d,
            )
        embed2.add_field(name="Geral", value="-  r!invite: _Link padrão para adicionar a Lil Rei no servidor!_ **Aliases:** r!convite\n\n-  r!avatar `user`: _Pega a foto de perfil do usuário! Se não passar nenhum usuário como parâmetro, pega do usuário que executou o comando!_")
        embed2.add_field(name="Chat", value="-  r!purge `quantidade`: _Apaga uma quantidade de mensagens entre 1 e 1000 do chat_.\n\n-  r!nuke: _Apaga completamente todas as mensagens de um chat._")
        embed2.add_field(name="User", value="-  r!mute `user`: _Adiciona um cargo de Silenciado para um usuário_. (antigo) **Aliases:** r!mutar, r!silenciar\n\n-  r!kick `user`: _Expulsa o usuário do servidor!_ **Aliases:** r!expulsar\n\n-  r!ban `user`: _Bane aquele cara chato do seu servidor!_")
        embed2.set_footer(text= "Lil Rei • © Todos os direitos reservados.")

        embed3 = discord.Embed(
                title="ECONOMIA",
                description= f"Todos os comandos relacionados as rei coins estão aqui! **Trabalhando assiduamente no bot, em breve terão muitos novos comandos!**",
                color=0xa8326d,
            )
        embed3.add_field(name="Money", value="-  r!bank `user`: _Mostra a conta bancária do usuário! Se nenhum for mencionado, mostra a própria conta!_\n\n-  r!daily: _Pega uma quantia diária de rei coins! Pode ser resgatado a cada 12 horas._\n\n-  r!rank: _Mostra os 5 usuários mais ricos do mundo em rei coins!_\n\n-  r!vote: _Consiga uma quantidade extra de rei coins por ajudar a divulgar o bot._")
        embed3.add_field(name="Apostas", value="r!pix `user` `quantia`: _Transfere determinada quantia de dinheiro para o usuário!_\n\n-  r!coinflip `user` `quantia`: _Está com sorte? Então aposte suas rei coins contra seu amigo! Apenas ele precisa confirmar na reação._")
        embed3.set_footer(text= "Lil Rei • © Todos os direitos reservados.")
        

        await ctx.author.send(embed=embed1)
        await ctx.author.send(embed=embed2)
        await ctx.author.send(embed=embed3)

        await ctx.author.send("__**Experimente usar também o slash /help!**__")


        await ctx.reply("_Comando enviado! Verifique suas DMs._")


    @app_commands.command(name="help", description="Ajuda da Lil Rei! Estarei sempre disposta por você...")
    @app_commands.choices(options=[
        discord.app_commands.Choice(name="Geral", value = 1),
        discord.app_commands.Choice(name="Admin", value = 2),
        discord.app_commands.Choice(name="Economy", value = 3),
    ])
    async def _helpslash(self, interaction: discord.Interaction, options: discord.app_commands.Choice[int]):
        
        if options.value == 1:

            embed = discord.Embed(
                title="Lil Rei",
                description= f"Oi, eu sou a Lil Rei! Um bot divertido de **economia, administração e outros comandos que virão em breve!**\nEstarei sempre crescendo e progredindo, então se tiver algum erro ou dúvida, não tenha medo de compartilhar e ajudar, assim eu posso ser uma versão melhor de mim mesma! Espero que se divirta, pois fui criada com muito amor e carinho <3\n\nGostaria de dar uma olhada meu código! É open source, 100% feito em **Python!** Basta clicar [aqui!](https://github.com/danbasco/rei)\n\nServidores oficiais da Lil Rei:\n -  [Saturn](https://discord.gg/saturnday)\n-  [Lil Rei's Kingdom (Suporte)](https://discord.gg/BhrEWubvdz)",
                color=0xa8326d,
            )
            #embed.add_field(name="Help", value="Digite /help ADMIN para ver os comandos de utilidade/administração.\n\nDigite /help ECONOMY para os comandos de economia.")
            embed.set_image(url="https://cdn.discordapp.com/avatars/1080924319250661456/d824459f3f40dacac1357c1d4c00ceb3.png?size=2048")
            embed.set_footer(text= "Lil Rei • © Todos os direitos reservados.")
        
        if options.value == 2:
            
            embed = discord.Embed(
                title="ADMIN",
                description= f" ",
                color=0xa8326d,
            )
            embed.add_field(name="Geral", value="-  r!invite: _Link padrão para adicionar a Lil Rei no servidor!_ **Aliases:** r!convite\n\n-  r!avatar `user`: _Pega a foto de perfil do usuário! Se não passar nenhum usuário como parâmetro, pega do usuário que executou o comando!_")
            embed.add_field(name="Chat", value="-  r!purge `quantidade`: _Apaga uma quantidade de mensagens entre 1 e 1000 do chat_.\n\n-  r!nuke: _Apaga completamente todas as mensagens de um chat._")
            embed.add_field(name="User", value="-  r!mute `user`: _Adiciona um cargo de Silenciado para um usuário_. (antigo) **Aliases:** r!mutar, r!silenciar\n\n-  r!kick `user`: _Expulsa o usuário do servidor!_ **Aliases:** r!expulsar\n\n-  r!ban `user`: _Bane aquele cara chato do seu servidor!_")
            embed.set_footer(text= "Lil Rei • © Todos os direitos reservados.")

        if options.value == 3:
            embed = discord.Embed(
                title="ECONOMIA",
                description= f"Todos os comandos relacionados as rei coins estão aqui! **Trabalhando assiduamente no bot, em breve terão muitos novos comandos!**",
                color=0xa8326d,
            )
            embed.add_field(name="Money", value="-  r!bank `user`: _Mostra a conta bancária do usuário! Se nenhum for mencionado, mostra a própria conta!_\n\n-  r!daily: _Pega uma quantia diária de rei coins! Pode ser resgatado a cada 12 horas._\n\n-  r!rank: _Mostra os 5 usuários mais ricos do mundo em rei coins!_\n\n-  r!vote: _Consiga uma quantidade extra de rei coins por ajudar a divulgar o bot._")
            embed.add_field(name="Apostas", value="r!pix `user` `quantia`: _Transfere determinada quantia de dinheiro para o usuário!_\n\n-  r!coinflip `user` `quantia`: _Está com sorte? Então aposte suas rei coins contra seu amigo! Apenas ele precisa confirmar na reação._")
            embed.set_footer(text= "Lil Rei • © Todos os direitos reservados.")

        await interaction.response.send_message(embed=embed, ephemeral=True)




async def setup(client):
    await client.add_cog(Help(client))