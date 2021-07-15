#!/home/linuxbrew/.linuxbrew/bin/python3
#happybot v2

#import depenedancies
import datetime
import discord
from discord.ext import tasks
import asyncio
from config import DISCORD_TOKEN
from table_data import read_table, write_csv


#Create intents object to hand to the client instance
intents = discord.Intents.all()

#Create the Client instance imported from the discord library with the intents arguement provided
client = discord.Client(intents=intents)
GUILD_NAME = "PTCB Study Group 💊💉"



#Using the on_ready() event handler
@client.event
async def on_ready():
    guild = None
    for guild_ in client.guilds: 
        if guild_.name == GUILD_NAME:
            guild = guild_
            break
    
    general_channel_id = None
    for channel in guild.channels:
        if channel.name == "general":
            general_channel_id = channel.id
            break

    await client.get_channel(general_channel_id).send("HappyBot Conneted")
    goodmorning.start(general_channel_id)

@tasks.loop(hours=1)  
async def goodmorning(channel_id):
    channel = client.get_channel(channel_id)
    hour = datetime.datetime.now().time().hour
    minute = datetime.datetime.now().time().minute
    print(hour, minute)
    if hour == 8 and minute in range(1,59):
        await channel.send(f"Goodmorning!")
        





client.run(DISCORD_TOKEN)
