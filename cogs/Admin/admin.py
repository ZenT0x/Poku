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
    
    @app_commands.command(name="uptime", description="Depuis combien de temps j'chui au carré VIP ?")
    async def uptime(self, interaction : discord.Integration):
        await interaction.response.send_message(f"J'chui au carré VIP depuis {datetime.timedelta(seconds=int(round(time.time() - startTime)))}")
    

    @app_commands.command(name="dormir", description="J'sors du casino")
    async def dormir(self, interaction : discord.Integration):
        if self.admin_check(interaction):
            await interaction.response.send_message("Ok, j'me casse")
            self.bot.logger.info(f"{interaction.user.id} : {interaction.user.name} : Le bot s'est arrêté")
            self.bot.logger.info("=== ENDING BOT ===")
            self.bot.logger.info("-------------------")
            await self.bot.close()
        else:
            await interaction.response.send_message("Ratio ?")

    @app_commands.command(name="reload", description="J'sors fumé un pétard et j'reviens")
    async def reload(self, interaction : discord.Integration):
        if self.admin_check(interaction):
            await interaction.response.send_message("J'reviens, j'vais fumé un pétard quelque secondes")
            self.bot.logger.info(f"{interaction.user.id} : {interaction.user.name} : Le bot se recharge")
            self.bot.logger.info("=== ENDING BOT ===")
            self.bot.logger.info("-------------------")
            os.system('bash scripts/reboot.sh')
            await self.bot.close()
        else:
            await interaction.response.send_message("Ratio ?")

async def setup(bot):
    await bot.add_cog(Admin(bot))