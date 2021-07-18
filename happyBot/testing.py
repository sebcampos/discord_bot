#testing 
#import depenedancies
import discord
from discord.ext import tasks
from config import DISCORD_TOKEN
from happybotlib import *


#Create intents object to hand to the client instance
intents = discord.Intents.all()

#Create the Client instance imported from the discord library with the intents arguement provided
client = discord.Client(intents=intents)
GUILD_NAME = "PTCB Study Group 💊💉"

#Using the on_ready() event handler to begin tasks
@client.event
async def on_ready():
    for guild in client.guilds:
        print(f"\n{guild}:")
        for member in guild.members:
            print(f"{member} - {member.id}")


client.run(DISCORD_TOKEN)