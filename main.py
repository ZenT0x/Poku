import discord
from discord.ext import commands, tasks
from discord import app_commands

import logging

from asyncio import run as asyncio_run, sleep as asyncio_sleep
from os import path as os_path, name as os_name
from json import load as json_load 
from random import choice as random_choice
from time import sleep as time_sleep
from threading import Thread
from requests import get as requests_get
from platform import system as platform_system, python_version as platform_python_version, release as platform_release

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=".",intents=intents,help_command=None)
uptimeKumaUrl = "http://192.168.1.14:3001/api/push/k9Hj9htAyt?status=up&msg=OK&ping="   
        
cogs : list = ["cogs.Admin.admin","cogs.Minecraft.function"]


class LoggingFormatter(logging.Formatter):
    # Colors
    black = "\x1b[30m"
    red = "\x1b[31m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    blue = "\x1b[34m"
    gray = "\x1b[38m"
    # Styles
    reset = "\x1b[0m"
    bold = "\x1b[1m"

    COLORS = {
        logging.DEBUG: gray + bold,
        logging.INFO: blue + bold,
        logging.WARNING: yellow + bold,
        logging.ERROR: red,
        logging.CRITICAL: red + bold
    }

    def format(self, record):
        log_color = self.COLORS[record.levelno]
        format = "(black){asctime}(reset) (levelcolor){levelname:<8}(reset) (green){name}(reset) {message}"
        format = format.replace("(black)", self.black + self.bold)
        format = format.replace("(reset)", self.reset)
        format = format.replace("(levelcolor)", log_color)
        format = format.replace("(green)", self.green + self.bold)
        formatter = logging.Formatter(format, "%Y-%m-%d %H:%M:%S", style="{")
        return formatter.format(record)


logger = logging.getLogger("Poku : ")
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(LoggingFormatter())
# File handler
file_handler = logging.FileHandler(
    filename="discord.log", encoding="utf-8", mode="a")
file_handler_formatter = logging.Formatter(
    "[{asctime}] [{levelname:<8}] {name}: {message}", "%Y-%m-%d %H:%M:%S", style="{")
file_handler.setFormatter(file_handler_formatter)

# Add the handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)
bot.logger = logger



if not os_path.isfile(f"{os_path.realpath(os_path.dirname(__file__))}/config.json"):
    bot.logger.info("'config.json' not found! Please add it and try again.")
else:
    with open(f"{os_path.realpath(os_path.dirname(__file__))}/config.json") as file:
        config = json_load(file)
        bot.logger.info("-------------------")
        bot.logger.info("=== STARTING BOT ===")
        bot.logger.info("json loaded")



@tasks.loop(minutes=1.0)
async def status_task() -> None:
    """
    Setup the game status task of the bot.
    """
    requests_get(uptimeKumaUrl)
    statuses = config["statues"]
    if config["wake_up_time_finished"]:
        await bot.change_presence(activity=discord.Game(random_choice(statuses)))



@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="J'me lève la"))
    bot.logger.info("-------------------")
    bot.logger.info(f"Logged in as {bot.user.name}")
    bot.logger.info(f"discord.py API version: {discord.__version__}")
    bot.logger.info(f"Python version: {platform_python_version()}")
    bot.logger.info(
        f"Running on: {platform_system()} {platform_release()} ({os_name})")
    bot.logger.info("-------------------")
    status_task.start()
    if config["sync_commands_globally"]:
        try : 
            bot.logger.info("Syncing commands globally...")
            synced = await bot.tree.sync()
            for command in synced:
                bot.logger.info(f"Synced command {command.name}")
            bot.logger.info("Synced commands globally.")
            bot.logger.info("-------------------")
        except Exception as e:
            print(f"Failed to sync commands: {e}")
    bot.logger.info("Bot ready.")
    
    config["wake_up_time_finished"] = False
    await asyncio_sleep(30)
    config["wake_up_time_finished"] = True
    


            
async def load_cogs() -> None:
    bot.logger.info(f"-------------------")
    bot.logger.info(f"Loading cogs...")
    for cog in cogs:
        try:
            await bot.load_extension(cog)
            bot.logger.info(f"Loaded cog {cog}")
        except Exception as e:
            exc = "{}: {}".format(type(e).__name__, e)
            bot.logger.info("Failed to load cog {}\n{}".format(cog, exc))
    bot.logger.info(f"All cogs loaded.")
    bot.logger.info("-------------------")
    

asyncio_run(load_cogs())
bot.run(config["token"])