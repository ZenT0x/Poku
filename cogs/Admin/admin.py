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
        return interaction.user.id == 306848454032883714
    
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
            await interaction.response.send_message("Ratio ?")

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
            await interaction.response.send_message("Ratio ?")
            
    @app_commands.command(name="compter", description="Compte très vite")
    async def compter(self, interaction : discord.Integration):
        if self.admin_check(interaction):
            await interaction.response.send_message("1")
            message = await interaction.original_response()
            for i in range(2, 100):
                await message.edit(content=str(i))
    
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