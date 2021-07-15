#!/home/linuxbrew/.linuxbrew/bin/python3
#happybot v2

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



#Using the on_ready() event handler
@client.event
async def on_ready():
    guild_PTCB = None
    guild_ROB = None
    for guild_ in client.guilds: 
        if guild_.name == GUILD_NAME:
            guild_PTCB = guild_
        else:
            guild_ROB= guild_
    
    general_channel_id = {"ptcb": 0, "robguild": 0}
    for channel in guild_PTCB.channels:
        if channel.name == "general":
            general_channel_id["ptcb"] += channel.id
            break

    for channel in guild_ROB.channels:
        if channel.name == "general":
            general_channel_id["robguild"] += channel.id
            break
    new_happy_bot_guild_users(guild, GUILD_NAME)
    user_of_the_week_new_table()
    #await client.get_channel(general_channel_id).send(f"HappyBot Conneted to {GUILD_NAME}")
    goodmorning.start(general_channel_id)


@client.event
async def on_message(message):
    #DM to HappyBot
    if isinstance(message.channel, discord.channel.DMChannel) and message.author != client.user:
        await message.channel.send(f'Hello {message.author.split("#")[0]}')




@tasks.loop(hours=1)  
async def goodmorning(channel_id):
    channel_ptcb = client.get_channel(channel_id["ptcb"])
    channel_rob = client.get_channel(channel_id["robguild"])
    hour = datetime.datetime.now().time().hour
    minute = datetime.datetime.now().time().minute
    ws = WebScraper()
    gif = ws.goodmorning()
    ws.quit()
    print("waiting")
    if hour == 8 and minute in range(1,59):
        await channel_ptcb.send(f"Goodmorning!\n{gif}")
        await channel_rob.send(f"Goodmorning!\n{gif}")
        





client.run(DISCORD_TOKEN)
