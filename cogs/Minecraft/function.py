import os
import discord
from time import sleep
from discord.ext import commands
from discord.ui import Button, View
from discord import app_commands
from random import randint
from datetime import datetime

from lib.minecraftdb import db as db
from lib.minecraftcstatus import get_minecraft_status 
        
        
    
class Minecraft(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.minecraftServerIpAdress = "ip"
        self.minecraftBootFiles = os.listdir('scripts/minecraft_boot')
        self.minecraftLaunchScripts = self.minecraftBootFiles
        self.minecraftBootFiles = [file.replace(".sh", "") for file in self.minecraftBootFiles]    
    
    @app_commands.command(name="minecraft",description="Choisis un serveur minecraft à gérer") 
    async def minecraftserver(self, interaction : discord.Integration):
        self.bot.logger.info("Minecraft command called by "+interaction.user.name)
        servers = db.get_all_servers()
        for server in servers:
            if server[3] == 1:
                serverRunning = server
                break
            else :
                serverRunning = None
                
        if get_minecraft_status(self.minecraftServerIpAdress)[0] == -1:
            serverRunning = None
            db.set_all_servers_running(0)
        
        
        if serverRunning == None:
            embed = discord.Embed(title="Serveur Minecraft", description="Aucun serveur n'est actuellement lancé", color=0x3EFF00)
            for server in db.get_all_servers():
                embed.add_field(name=server[1], value=server[2], inline=True)
                
            view = View()
            LaunchButtonDict = {}
            
            for i in range(len(db.get_all_servers())):
                server = db.get_all_servers()[i]
                LaunchButtonDict[server[1]] = Button(label="Lancer "+server[1], style=discord.ButtonStyle.green,emoji="▶️")
                view.add_item(LaunchButtonDict[server[1]])

                 
                async def launchServerCallback(interaction : discord.Interaction, server):
                    timeOut = 150
                    attempts = 0

                    os.system('bash scripts/minecraft_boot/'+server[4])
                    db.set_server_running(server[0], 1)
                    
                    await interaction.response.defer()
                    for button in LaunchButtonDict.values():
                        button.disabled = True
                    new_embed = discord.Embed(title="Serveur Minecraft", description="Le serveur "+server[1]+" est en cours de lancement", color=0x3EFF00)
                    self.bot.logger.info("The server "+server[1]+" is being launched by "+interaction.user.name)
                    progress_bar = ["⬜"] * 16
                    new_embed.add_field(name="Statut", value="".join(progress_bar), inline=True)
                    message = await interaction.original_response()
                    await message.edit(embed=new_embed, view=view)
                        
                    progress_bar[0] = "🟩"
                    progress_bar[1] = "🟩"
                    while get_minecraft_status(self.minecraftServerIpAdress)[0] == -1 and attempts < timeOut:
                        index = attempts % 16
                        progress_bar[index-1] = "⬜"
                        progress_bar[(index+2)%16] = "🟩"
                        new_embed.set_field_at(0, name="Statut", value="".join(progress_bar), inline=True)
                        await message.edit(embed=new_embed)
                        attempts += 1
                        sleep(1)
                        
                    if attempts == timeOut:
                        for i in range(len(progress_bar)):
                            progress_bar[i] = "🟥"
                        new_embed.set_field_at(0, name="Statut", value="".join(progress_bar), inline=True)
                        new_embed.title = "Le serveur "+server[1]+" n'a pas pu être lancé"
                        new_embed.description = "Ptit problème technique"
                        new_embed.color = 0xFF0000
                        self.bot.logger.error("The server "+server[1]+" could not be launched by "+interaction.user.name)
                        await message.edit(embed=new_embed)
                        db.set_server_running(server[0], 0)
                        return
                    
                    await self.manageServer(interaction, server, message)
                
                LaunchButtonDict[server[1]].callback = lambda x, s=server: launchServerCallback(x, s)            
            
            await interaction.response.send_message(embed=embed, view=view)
        else:
            await self.manageServer(interaction, serverRunning)
            message = await interaction.original_response()
        if serverRunning != None:
            await self.manageServer(interaction, serverRunning)
            
    async def manageServer(self, interaction : discord.Integration, server, message = None):
        if message == None:
            embed = discord.Embed(title="Chargement de l'interface", description="Veuillez patienter", color=0x3EFF00)
            await interaction.response.send_message(embed=embed)
            message = await interaction.original_response()
        
        serverinformation = get_minecraft_status(self.minecraftServerIpAdress)
        try: 
            number_of_players = serverinformation[0]
            list_of_players = serverinformation[1]
            ping = serverinformation[2]
        except:
            number_of_players = list_of_players = ping = -1
            
        view = View()
        stopButton = Button(label="Arrêter "+server[1], style=discord.ButtonStyle.red,emoji="⬜")
        refreshButton = Button(label="Rafraîchir", style=discord.ButtonStyle.blurple,emoji="🔄")
        
        view.add_item(stopButton)
        view.add_item(refreshButton)
        
        #Edit message to change title and add nubmber of players, list of player, ping, ...
        embedStatus = discord.Embed(title="Serveur : "+server[1], description="Le serveur est actuellement lancé", color=0x7289DA)
        embedStatus.add_field(name="Nombre de joueurs", value=number_of_players, inline=True)
        embedStatus.add_field(name="Liste des joueurs", value=list_of_players, inline=True)
        embedStatus.add_field(name="Ping", value=ping, inline=True)
        embedStatus.set_footer(text="Actualisé à "+datetime.now().strftime("%H:%M le %d/%m/%Y "))
        await message.edit(embed=embedStatus, view=view)
        
        async def stopServerCallback(interaction : discord.Interaction, server):
            os.system('bash scripts/minecraft_tools/stop.sh')
            await interaction.response.defer()
            db.set_server_running(server[0], 0)
            embed_stop = discord.Embed(title="Serveur Minecraft", description="Le serveur "+server[1]+" a été arrêté", color=0xFF0000)
            embed_stop.set_footer(text="Actualisé à "+datetime.now().strftime("%H:%M le %d/%m/%Y "))
            self.bot.logger.info("The server "+server[1]+" has been stopped")
            for button in view.children:
                button.disabled = True
            await message.edit(embed=embed_stop, view=view)
            
            
            
        async def refreshServerCallback(interaction : discord.Interaction, server):
            serverinformation = get_minecraft_status(self.minecraftServerIpAdress)
            self.bot.logger.info("The server "+server[1]+" has been refreshed by "+interaction.user.name)
            try: 
                number_of_players = serverinformation[0]
                list_of_players = serverinformation[1]
                ping = serverinformation[2]
            except:
                number_of_players = list_of_players = ping = -1
            embedStatus = discord.Embed(title="Serveur : "+server[1], description="Le serveur est actuellement lancé", color=0x7289DA)
            embedStatus.add_field(name="Nombre de joueurs", value=number_of_players, inline=True)
            embedStatus.add_field(name="Liste des joueurs", value=list_of_players, inline=True)
            embedStatus.add_field(name="Ping", value=ping, inline=True)
            embedStatus.set_footer(text="Actualisé à "+datetime.now().strftime("%H:%M le %d/%m/%Y "))
            await message.edit(embed=embedStatus, view=view)
            await interaction.response.defer()
            
        stopButton.callback = lambda x, s=server: stopServerCallback(x, s)
        refreshButton.callback = lambda x, s=server: refreshServerCallback(x, s)

async def setup(bot):
    await bot.add_cog(Minecraft(bot))