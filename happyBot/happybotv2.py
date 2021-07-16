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
    guild_dict_gc = collect_general_chat_all_guilds(client)
    scrape_web.start()
    goodmorning.start(guild_dict_gc)
    new_user_of_the_week.start()


@client.event
async def on_message(message):
    #DM to HappyBot
    if isinstance(message.channel, discord.channel.DMChannel) and message.author != client.user:
        await message.channel.send(f'Hello {message.author.split("#")[0]}')




@tasks.loop(hours=168)
async def new_user_of_the_week():
    tup = pick_user_of_the_week("PTCB","PTCB_users")
    tup2 = pick_user_of_the_week("ROB","ROB_users")
    print(tup, tup2)


@tasks.loop(hours=72)
async def scrape_web():
    ws = WebScraper()
    gif = ws.goodmorning_gif()
    ws.quit()



@tasks.loop(hour=24)  
async def goodmorning(guild_dict_gc):
    hour = datetime.datetime.now().time().hour
    minute = datetime.datetime.now().time().minute
    print("morning loop")
    if hour == 8 and minute in range(1,60):
        for guild,gc_channel in guild_dict_gc.items():
            await guild.get_channel(gc_channel).send(f"Goodmorning!")
            await guid.get_channel(gc_channel).send(file=discord.File(pick_random_goodmorning_gif()))

    





client.run(DISCORD_TOKEN)
