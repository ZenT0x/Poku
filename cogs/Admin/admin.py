import os
import discord
from typing import Union
from discord.ext import commands
from discord import app_commands
import datetime, time

class Admin(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        global startTime
        startTime = time.time()
        
    def admin_check(self, interaction):
        print(f"{interaction.user.id}")
        return interaction.user.id == id
    
    @app_commands.command(name="uptime", description="Mon uptime")
    async def uptime(self, interaction : discord.Integration):
        await interaction.response.send_message(f"J'chui up depuis {datetime.timedelta(seconds=int(round(time.time() - startTime)))}")
    

    @app_commands.command(name="dormir", description="Au dodo !")
    async def dormir(self, interaction : discord.Integration):
        if self.admin_check(interaction):
            await interaction.response.send_message("Ok, j'vais me coucher")
            self.bot.logger.info(f"{interaction.user.id} : {interaction.user.name} : Le bot s'est arrêté")
            self.bot.logger.info("=== ENDING BOT ===")
            self.bot.logger.info("-------------------")
            await self.bot.close()
        else:
            await interaction.response.send_message("Pas admin")

    @app_commands.command(name="reload", description="Reload le bot")
    async def reload(self, interaction : discord.Integration):
        if self.admin_check(interaction):
            await interaction.response.send_message("J'reviens, j'recharge")
            self.bot.logger.info(f"{interaction.user.id} : {interaction.user.name} : Le bot se recharge")
            self.bot.logger.info("=== ENDING BOT ===")
            self.bot.logger.info("-------------------")
            os.system('bash scripts/reboot.sh')
            await self.bot.close()
        else:
            await interaction.response.send_message("Pas admin")
            
    @app_commands.command(name="reload_cogs",description="Reload all cogs")
    async def reload_cogs(self, interaction):
        if interaction.user.id == id:
            embed = discord.Embed(title="Reload cogs",description="Reload all cogs",color=0x00ff00)
            cogs : list = ["cogs.Admin.admin","cogs.Minecraft.function"]
            self.bot.logger.info(f"Reloading all cogs...")
            for cog in cogs:
                try:
                    await self.bot.reload_extension(cog)
                    self.bot.logger.info(f"Reloaded cog {cog}")
                    embed.add_field(name=f"Reloaded cog {cog}",value="✅",inline=False)
                except Exception as e:
                    exc = "{}: {}".format(type(e).__name__, e)
                    self.bot.logger.info("Failed to reload cog {}\n{}".format(cog, exc))
                    embed.add_field(name=f"Failed to reload cog {cog}",value="❌",inline=False)
            self.bot.logger.info(f"All cogs reloaded.")
            self.bot.logger.info("-------------------")
            embed.add_field(name=f"Finished",value="✅",inline=False)
            await interaction.response.send_message(embed=embed,ephemeral=True)       
    
    @app_commands.command(name="discord", description="Donne des infos sur le serveur discord")
    async def discord(self, interaction : discord.Integration):
        embed = discord.Embed(title="Serveur Discord", description="Voici quelques infos sur le serveur discord", color=0x3EFF00)
        embed.add_field(name="Nom", value=interaction.guild.name, inline=True)
        embed.add_field(name="Créateur", value=interaction.guild.owner, inline=True)
        embed.add_field(name="Nombre de membres", value=interaction.guild.member_count, inline=True)
        embed.add_field(name="Nombre de salons", value=len(interaction.guild.channels), inline=True)
        embed.add_field(name="Nombre de rôles", value=len(interaction.guild.roles), inline=True)
        embed.set_footer(text="Poku")
        embed.set_image(url=interaction.guild.icon.url)        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Admin(bot))