
import discord
from discord import app_commands
from discord.ext import commands


## ## Get discord TOKEN ## ##
with open('asset/apiKey/TOKEN', 'r') as file:
    Token=file.read()
    file.close()
## ####################### ##

dodoBot = discord.Client(intents=discord.Intents.default())
tree = app_commands.CommandTree(dodoBot)

import game

@dodoBot.event
async def on_ready():
    await tree.sync()
    print("dodoBot is alive")


@tree.command(name="say") 
@app_commands.describe(arg = "what should i say ?")
async def say(interaction: discord.Integration, arg: str):
    await interaction.response.send_message(f'{arg}')

dodoBot.run(Token)