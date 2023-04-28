import discord
from discord.ext import commands
from discord import app_commands
import random as r
import platform
import os
import sys

from lib import minecraftclass

class Minecraft(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    '''
    @app_commands.command(name="json", description="See configuration file")
    async def json(ctx : discord.Integration, file: str = None, key : str = None):
        if key != None:
            await ctx.response.send_message(globals()[file.value].data[key], ephemeral=True)
        else :
            await ctx.response.send_message(globals()[file.value].data, ephemeral=True)
    '''

    @app_commands.command(name="hello", description="Say hello")
    async def hello(self ,ctx : discord.Integration):
        await ctx.response.send_message("Hello !", ephemeral=True)


'''

##########################################################################
# Serveur Minecraft
##########################################################################


@bot.tree.command(name="mcinfo", description="See minecraft server info")
async def mcinfo(ctx):
    embed = discord.Embed(title="Les infos sur les serveurs minecraft", description="IP : play.hypoxel.tk", color=0x3EFF00)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/808996714551181342/963103630209212466/Illustration_sans_titre.png")

    for id in range(1,len(minecraft.data["servers"])) :
        print(id)
        embed.add_field(name="Serveur : " + str(id), value=
        minecraft.data["servers"][id]["name"]+'\n'+
        minecraft.data["servers"][id]["description"]+'\n'+
        str(minecraft.data["servers"][id]["running"]),
        inline=True)

    embed.set_footer(text="Poku est un produit déposé par Poku®")
    await ctx.response.send_message(embed=embed)

@bot.tree.command(name="mc", description="Manage minecraft server")
@app_commands.choices(func=[
    app_commands.Choice(name="start", value="1"),
    app_commands.Choice(name="stop", value="2"),
    app_commands.Choice(name="restart", value="3"),
    ])
@app_commands.choices(server=[
    app_commands.Choice(name="Vanilla", value="1"),
    app_commands.Choice(name="Modé", value="2"),
    ])
async def mc(ctx, server : app_commands.Choice["str"], func : app_commands.Choice["str"]):
    if ctx.user.id in liste_op_minecraft :
        if server.value == "1": # If the user selected vanilla server
            if func.value == "1": # If the user selected start
                temp = serveur_vanilla.start() # Start the server
                if temp == 1: # If the server is not already started
                    await ctx.response.send_message("Server started", ephemeral=True) # Send a message to the user
                else: # If the server is already started
                    await ctx.response.send_message("Server already started", ephemeral=True) # Send a message to the user
            elif func.value == "2": # If the user selected stop
                serveur_vanilla.stop() # Stop the server
                await ctx.response.send_message("Server stopped", ephemeral=True) # Send a message to the user
            elif func.value == "3": # If the user selected restart
                serveur_vanilla.restart() # Restart the server
                await ctx.response.send_message("Server restarting, wait at least 2 minutes", ephemeral=True) # Send a message to the user
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=config.data["activity"]))
            return 1
        elif server.value == "2": # If the user selected mode server
            if func.value == "1": # If the user selected start
                temp = serveur_mode.start() # Start the server
                if temp == 1: # If the server is not already started
                    await ctx.response.send_message("Server started", ephemeral=True) # Send a message to the user
                else: # If the server is already started
                    await ctx.response.send_message("Server already started", ephemeral=True) # Send a message to the user
            elif func.value == "2": # If the user selected stop
                serveur_mode.stop() # Stop the server
                await ctx.response.send_message("Server stopped", ephemeral=True) # Send a message to the user
            elif func.value == "3": # If the user selected restart
                serveur_vanilla.restart() # Restart the server
                await ctx.response.send_message("Server restarting, wait at least 2 minutes", ephemeral=True) # Send a message to the user
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=config.data["activity"]))
            return 2
                
            
    


@bot.command(name="mcexec")
async def mcexec(ctx,*,commande):
    if ctx.message.author.id in liste_op_minecraft :
        commande='"'+str(commande)+'"'
        os.system('bash mcexec.sh '+str(commande))
        await ctx.channel.send("J'ai éxécuté la commande : "+commande+" dans la console du serveur")
    else:
        reponse="Toi fidèle ?"
        await ctx.reply(reponse)


"""
@bot.command(name="mcstart")
async def mcstart(ctx,*,arg):
    print(type(arg))
    print(arg)
    if ctx.message.author.id in liste_op_minecraft :
        if arg == "1":
            os.system('bash mcstart.sh')
            print("start 1")
        elif arg == "2":
            os.system('bash mcstart2.sh')
            print("mcstart 2")
        else:
            await ctx.channel.send("Y'a pas de serv : "+arg)
        await ctx.channel.send("Le serveur démarre :thumbsup:")
        data = {"activity": str("Serveur open")}
        config.write_config(data,1)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=config.data["activity"]))
    else:
        reponse="Toi fidèle ?"
        await ctx.reply(reponse)

@bot.command(name="mcstop")
async def mcstop(ctx):
    if ctx.message.author.id in liste_op_minecraft :
        os.system('bash mcstop.sh')
        data = {"activity": str("Serveur fermé")}
        config.write_config(data,1)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=config.data["activity"]))
    else:
        reponse="Toi fidèle ?"
        await ctx.reply(reponse)
"""
@bot.command(name="mcrestart")
async def mcrestart(ctx):
    if ctx.message.author.id in liste_op_minecraft :
        os.system('bash mcrestart.sh')
        await ctx.channel.send("Le serveur redémarre :gear:")
    else:
        reponse="Toi fidèle ?"
        await ctx.reply(reponse)


bot.run(token)

'''

async def setup(bot):
    await bot.add_cog(Minecraft(bot))