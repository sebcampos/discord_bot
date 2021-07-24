#testing 
#import depenedancies
import discord
from discord.ext import tasks
from config import DISCORD_TOKEN



#Create intents object to hand to the client instance
intents = discord.Intents.all()

#Create the Client instance imported from the discord library with the intents arguement provided
client = discord.Client(intents=intents)
GUILD_NAME = "PTCB Study Group 💊💉"

#Using the on_ready() event handler to begin tasks
@client.event
async def on_ready():
    for guild in client.guilds:
        for channel in guild.channels:
            if str(channel.type) == "voice" and "general" in channel.name.lower():
                print(channel)




client.run(DISCORD_TOKEN)