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
    guild = {"ptcb":GUILD_NAME, "robguild": ""}
    for guild_ in client.guilds: 
        if guild_.name == GUILD_NAME:
            guild["ptcb"] = guild_
        else:
            guild["robuild"] = guild_
    
    general_channel_id = {"ptcb":"", "robguild": ""}
    for channel in guild["ptcb"].channels:
        if channel.name == "general":
            general_channel_id["ptcb"] = channel.id
            break

    for channel in guild["robguild"].channels:
        if channel.name == "general":
            general_channel_id["robguild"] = channel.id
            break
    # new_happy_bot_guild_users(guild, GUILD_NAME)
    # user_of_the_week_new_table()
    #await client.get_channel(general_channel_id).send(f"HappyBot Conneted to {GUILD_NAME}")
    goodmorning.start(general_channel_id["ptcb"])
    goodmorning.start(general_channel_id["robguild"])


@client.event
async def on_message(message):
    #DM to HappyBot
    if isinstance(message.channel, discord.channel.DMChannel) and message.author != client.user:
        await message.channel.send(f'Hello {message.author}')




@tasks.loop(hours=1)  
async def goodmorning(channel_id):
    channel = client.get_channel(channel_id)
    hour = datetime.datetime.now().time().hour
    minute = datetime.datetime.now().time().minute
    ws = WebScraper()
    gif = ws.goodmorning()
    ws.quit()
    if hour == 8 and minute in range(1,59):
        await channel.send(f"Goodmorning!\n{gif}")
        





client.run(DISCORD_TOKEN)
