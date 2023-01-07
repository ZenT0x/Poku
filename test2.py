from asyncore import write
from unicodedata import name
from discord.ext import commands
from datetime import datetime
from email import message
import random as r
import discord
import json as js
import os
import time
import sys

#-------------------- Class json

class jsonclass:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    def read_config(self):
        with open(self.file_path, 'r') as f:
            self.data = js.load(f)

    def write_config(self,data,add=0):
        if add == 1:
            self.read_config()
            self.data.update(data)
        with open(self.file_path, "w") as file:
            js.dump(self.data,file,sort_keys=True,indent=4)

    def del_value_from_key_list(self,key,value):
        self.read_config()
        self.data[key].remove(value)
        self.write_config(self.data)

    def add_value_from_key_list(self,key,value):
        self.read_config()
        self.data[key].append(value)
        self.write_config(self.data)

config = jsonclass("config.json")
config.read_config()

token = config.data["token"]
liste_op = config.data["liste_op"]
liste_op_minecraft = config.data["liste_op_minecraft"]
prefix = config.data["prefix"]
ratio = config.data["ratio"]

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=prefix,intents=intents,help_command=None)

##########################################################################
# à la connexion
##########################################################################
@bot.event
async def on_ready():
    channel = discord.utils.get(bot.get_all_channels(), name="poku")  #remplacer "général" par le nom du salon
    await bot.get_channel(channel.id).send(config.data["message"])
    print(datenow() + f"{bot.user.name} est prêt.")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=config.data["activity"]))

##########################################################################
# en cas d'erreur dans les commandes
##########################################################################
@bot.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.CommandNotFound):
        await ctx.reply("J'connais pas ça, déso bro")
    else :
        raise error
    print(log(on_command_error,ctx))

##########################################################################
# Commandes
##########################################################################
@bot.command(name="coucou")
async def bonjour(ctx):
    reponse=f"Ça va, {ctx.message.author.name} ?"
    await ctx.reply(reponse)
    print(f"Réponse à message {ctx.message.id} : {reponse}")


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
    print(log(aide,ctx))

###########################################
# Images ...
###########################################

@bot.command(name="gicle")
async def gicle(ctx):
    await ctx.message.delete()
    await ctx.send(file=discord.File('images\gicler.png'))
    print(log(gicle,ctx))

@bot.command(name="juan")
async def juan(ctx):
    await ctx.message.delete()
    await ctx.send(file=discord.File('images\juan.png'))
    print(log(juan,ctx))

@bot.command(name="bebou")
async def bebou(ctx):
    await ctx.message.delete()
    await ctx.send("https://tenor.com/view/antoine-zevent-uwu-catboi-catboy-gif-23710618")
    print(log(bebou,ctx))

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
        print(log(act,ctx) + " : " + str(texte))

@bot.command(name="prefix")
async def change_prefix(ctx,):
    await ctx.send("J'ai pas envie")
    print(log(prefix,ctx))

###########################################
# Autres
###########################################

@bot.command(name="del")
async def delete(ctx,amount=1):
    if amount > 25:
        await ctx.reply("Pas plus de 25 chef")
    else:
        await ctx.channel.purge(limit=amount+1)
    print(log(delete,ctx))

@bot.command(name="dit")
async def dit(ctx,*,texte):
        await ctx.message.delete()
        await ctx.send(texte)
        print(log(dit,ctx) + " : " + str(texte))


@bot.command(name="apprend")
async def apprend(ctx,*,texte):
        if len(texte) > 240:
            await ctx.send("Trop long")
            print(log(apprend,ctx))
        else:
            myFile = open('phrases.txt', 'a', encoding="latin-1")
            myFile.write(texte+" \n")
            myFile.close()
            await ctx.message.delete()
            await ctx.send(f"<@{ctx.message.author.id}> m'a appris : {texte}")
            print(log(apprend,ctx) + " : " + str(texte))


@bot.command(name="parle")
async def parle(ctx,*,amount=1):
    if amount > 25:
            await ctx.send(amount,"? Ca fait beaucoup")
    else:
        myFile = open('phrases.txt', 'r', encoding="latin-1")
        phrases = myFile.readlines()
        await ctx.message.delete()
        if amount !=1:
            liste = ""
            for k in range(amount):
                liste = liste +" " + phrases[r.randint(0,len(phrases))]
            await ctx.send(liste.replace("\n",""))
        else:
            await ctx.send(phrases[r.randint(0,len(phrases))])
    print(log(parle,ctx))
    myFile.close


##########################################################################
# Serveur Minecraft
##########################################################################

@bot.command(name="mcinfo")
async def mcinfo(ctx):
    embed = discord.Embed(title="Les infos sur le serveur minecraft", description="IP : play.hypoxel.tk", color=0x3EFF00)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/808996714551181342/963103630209212466/Illustration_sans_titre.png")
    embed.add_field(name="Version", value=config.data["mc_version"], inline=True)
    embed.add_field(name="______________________", value="Uniquement pour les fidèles", inline=False)
    embed.add_field(name="Démarrer le serveur", value="£mcstart", inline=True)
    embed.add_field(name="Arrêter le serveur", value="£mcstop", inline=True)
    embed.add_field(name="Redémarre", value="£mcrestart", inline=True)

    embed.set_footer(text="Poku est un produit déposé par Poku®")
    await ctx.reply(embed=embed)
    print(log(aide,ctx))

@bot.command(name="mcexec")
async def mcexec(ctx,*,commande):
    if ctx.message.author.id in liste_op_minecraft :
        commande='"'+str(commande)+'"'
        os.system('bash mcexec.sh '+str(commande))
        print(log(mcexec,ctx)+' : bash mcexec.sh '+str(commande))
        await ctx.channel.send("J'ai éxécuté la commande : "+commande+" dans la console du serveur")
    else:
        reponse="Toi fidèle ?"
        await ctx.reply(reponse)

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
        print(log(mcstart,ctx))
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
        print(log(mcstop,ctx))
        data = {"activity": str("Serveur fermé")}
        config.write_config(data,1)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=config.data["activity"]))
    else:
        reponse="Toi fidèle ?"
        await ctx.reply(reponse)

@bot.command(name="mcrestart")
async def mcrestart(ctx):
    if ctx.message.author.id in liste_op_minecraft :
        os.system('bash mcrestart.sh')
        print(log(mcrestart,ctx))
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
        print(log(exit,ctx))
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
        print(log(reboot,ctx))
    else:
        reponse="Ratio t'es pas op"
        await ctx.reply(reponse)


##########################################################################
# Divers
##########################################################################

def datenow():
    return(datetime.now().strftime("%d/%m/%Y %H:%M:%S"+" : "))

def autheur(ctx):
    return ctx.message.author.name + " (" + str(ctx.message.author.id) + ")"

def log(function,ctx):
    l = datenow() + autheur(ctx) + " -> " + str(function)
    return l


##########################################################################
# Exécution du bot
##########################################################################

bot.run(token)