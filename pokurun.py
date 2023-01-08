import discord
from discord.ext import commands
from discord import app_commands
import random as r
import platform
import os
import sys

from pokuclass import *

"""
from asyncore import write
from unicodedata import name
from datetime import datetime
from email import message
import time"""

#-------------------- Class json



intents = discord.Intents.all()
bot = commands.Bot(command_prefix=prefix,intents=intents,help_command=None)

##########################################################################
# à la connexion
##########################################################################
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=config.data["activity"]))
    print(f"Logged in as {bot.user.name}")
    print(f"discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

##########################################################################
# en cas d'erreur dans les commandes
##########################################################################
@bot.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.CommandNotFound):
        await ctx.reply("J'connais pas ça, déso bro")
    else :
        raise error

##########################################################################
# Commandes avec un slash (/)
##########################################################################

@bot.tree.command(name="hello", description="Say hello !")
async def hello(interaction : discord.Integration):
    await interaction.response.send_message("Hello !" , ephemeral=True)

@bot.tree.command(name="say")
@app_commands.describe(thing_to_say="What should I say ?")
async def say(interaction : discord.Integration, thing_to_say : str):
    await interaction.response.send_message(thing_to_say)

@bot.tree.command(name="activity", description="Change the bot's activity")
@app_commands.describe(activity="What is my next activity ?")
async def activity(interaction : discord.Integration, activity : str):
    if interaction.user.id in liste_op :
        await interaction.response.send_message(f"Activity changed to {activity}", ephemeral=True)
        data = {"activity": str(activity)}
        config.write_config(data,1)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=config.data["activity"]))
    else :
        await interaction.response.send_message("Fin fréro, tu me donnes pas d'ordre", ephemeral=True)
        

@bot.tree.command(name="del", description="Delete X messages")
@app_commands.describe(amount="Less than 25 messages")
async def delete(ctx,amount : int = 1):
    if amount > 25:
        await ctx.response.send_message("Pas plus de 25 chef")
    else:
        await ctx.response.send_message("C'est clean :ok_hand:", ephemeral=True)
        await ctx.channel.purge(limit=amount+1)

@bot.tree.command(name="rps")
@app_commands.choices(choices=[
    app_commands.Choice(name="Rock", value="rock"),
    app_commands.Choice(name="Paper", value="paper"),
    app_commands.Choice(name="Scissors", value="scissors"),
    ])
async def rps(i: discord.Interaction, choices: app_commands.Choice[str]):
    if (choices.value == 'rock'):
        counter = 'paper'
    elif (choices.value == 'paper'):
        counter = 'scissors'
    else:
        counter = 'rock'
    # rest of your command      
        
@bot.tree.command(name="json", description="See configuration file")
@app_commands.describe(file="Which file do you want to see ?")
@app_commands.describe(key="Which key do you want to see ?")
@app_commands.choices(file=[
    app_commands.Choice(name="config", value="config"),
    app_commands.Choice(name="minecraft serveur", value="minecraft"),
    ])
async def json(ctx : discord.Integration, file: app_commands.Choice["str"], key : str = None):
    if ctx.user.id in liste_op :
        if key != None:
            await ctx.response.send_message(globals()[file.value].data[key], ephemeral=True)
        else :
            await ctx.response.send_message(globals()[file.value].data, ephemeral=True)



##########################################################################
# Commandes
##########################################################################

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author.id == 1:
        await message.reply("Ratio !")


@bot.command(name="aled")
async def aide(ctx):
    await ctx.channel.send("Check tes DM bébou :point_right: :point_left: ...")
    embed = discord.Embed(title="La page d'aide de Poku !", description="Jmet quoi", color=0xFF5733)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/808996714551181342/963103630209212466/Illustration_sans_titre.png")
    embed.add_field(name="______", value="Les bases", inline=False)
    embed.add_field(name="£aled", value="Tu l'as déjà fait, ça va ?", inline=True)
    embed.add_field(name="£dit", value="Répète ton message anonymement ...", inline=True)
    embed.add_field(name="£del 'X'", value="Nettoie les X derniers messages", inline=True)
    embed.add_field(name="______", value="Parle avec Poku", inline=False)
    embed.add_field(name="£apprend 'X'", value="Apprend une phrase X à Poku", inline=True)
    embed.add_field(name="£parle", value="Poku s'exprime avec les mots appris", inline=True)
    embed.add_field(name="______", value="Les images", inline=False)
    embed.add_field(name="£gicle", value="ça gicle ici", inline=True)
    embed.add_field(name="£juan", value="juan", inline=True)
    embed.add_field(name="£bebou", value="Antoine Daniel ?", inline=True)

    embed.set_footer(text="Poku est un produit déposé par Poku®")
    await ctx.message.author.send(embed=embed)

###########################################
# Config
###########################################

@bot.command(name="msg")
async def msg(ctx,*,texte):
    data = {"message" : str(texte)}
    config.write_config(data,1)

@bot.command(name="json")
async def json(ctx):
    if ctx.message.author.id in liste_op :
        await ctx.send(config.data)

@bot.command(name="act")
async def act(ctx,*,texte):
    if ctx.message.author.id in liste_op :
        data = {"activity": str(texte)}
        config.write_config(data,1)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=config.data["activity"]))

@bot.command(name="prefix")
async def change_prefix(ctx,):
    await ctx.send("J'ai pas envie")

###########################################
# Autres
###########################################



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


##########################################################################
# Déconnexion
##########################################################################


@bot.command(name="sleep")
async def exit(ctx):
    if ctx.message.author.id in liste_op :
        reponse="J'm'en vais ronpiche, la bise"
        await ctx.reply(reponse)
        await bot.close()
    else:
        reponse="Ratio"
        await ctx.reply(reponse)

@bot.command(name="reboot")
async def reboot(ctx):
    if ctx.message.author.id in liste_op :
        reponse="J'reviens"
        await ctx.reply(reponse)
        await bot.close()
    else:
        reponse="Ratio t'es pas op"
        await ctx.reply(reponse)


##########################################################################
# Exécution du bot
##########################################################################

bot.run(token)