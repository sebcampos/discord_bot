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



#Using the on_ready() event handler to begin tasks
@client.event
async def on_ready():
    vc_client_list = []
    #connect to music channel
    general_voice_channels = collect_general_voice_channels(client)
    for guild,gc_channel in general_voice_channels.items(): 
        vc = await client.get_channel(gc_channel).connect()
        vc_client_list.append(vc)
    
    for music_file in os.listdir("../data/mp3s"):
        for vc in vc_client_list:
            if vc.is_playing() != True:
                print("begining to play")
                print(f"\n\n{type(vc)}\n\n")
                vc.play(discord.FFmpegPCMAudio(f'/home/discord_admin/discord_bot/data/mp3s/{music_file}'), after=lambda x: print('done', x))
            else:
                print(f"{vc} conditional met")
                break

    # musicplayer.start(vc_client_list)
    # scrape_web.start()
    # goodmorning.start(guild_dict_gc)
    # new_user_of_the_week.start(guild_dict_gc)
    
    


#when DM'd happybot logs the suggestion
@client.event
async def on_message(message):
    #DM to HappyBot
    if isinstance(message.channel, discord.channel.DMChannel) and message.author != client.user:
        with open("../data/logs/happybot_feedback.txt","a") as log:
            log.write(f"\n{datetime.datetime.now()}\n{message.content}\n\n")
        await message.channel.send(f'Suggestion added, thank yous {message.author.name.split("#")[0]}!')

    

#on member join happybot welcomes them with a gif
@client.event
async def on_member_join(member):
    await member.send(f'Welcome {member.name.split("#")[0]}\n(message me suggestions please!)')
    await member.send(file=discord.File(pick_random_welcome_gif()))
    user = User(member.name, member.id, member.guild, "NaN","NaN","NaN")
    print(user)
    with open("../data/logs/new_member.log","a") as new_members:
        new_members.write(f"{user.username}, {user.user_id}, {user.guild}\n")




#choses a user of the week
@tasks.loop(hours=168)
async def new_user_of_the_week(guild_dict_gc):
    user_1 = pick_user_of_the_week("PTCB","PTCB_users")
    user_2 = pick_user_of_the_week("ROB","ROB_users")
    for user in [user_1, user_2]:
        for guild in client.guilds:
            for member in guild.members:
                if member.name == user:
                    channel = await member.create_dm()
                    await channel.send(f"You are User of the week for week {datetime.datetime.now().date()}!\n\nThis entitles you to bragging rights :)")
                    
    
    for unpack,user in list(zip(guild_dict_gc.items(),[user_1, user_2])):
        print(unpack)
        guild,gc_channel = unpack
        await guild.get_channel(gc_channel).send(f"{user.split('#')[0]} is user of the week!")
        await guild.get_channel(gc_channel).send(file=discord.File(pick_random_celebration_gif()))


#scrapes gifs every 3 days
@tasks.loop(hours=72)
async def scrape_web():
    ws = WebScraper()
    print("Goodmorning Scrape")
    ws.goodmorning_gif()
    print("Celebration Scrape")
    ws.celebration_gif()
    print("Welcome Scrape")
    ws.welcome_gif()
    ws.quit()


#sends a goodmorning and gif to the general channel
@tasks.loop(hours=24)  
async def goodmorning(guild_dict_gc):
    hour = datetime.datetime.now().time().hour
    minute = datetime.datetime.now().time().minute
    print("morning loop")
    for guild,gc_channel in guild_dict_gc.items():
        await guild.get_channel(gc_channel).send(f"Goodmorning!")
        await guild.get_channel(gc_channel).send(file=discord.File(pick_random_goodmorning_gif()))

    


                


client.run(DISCORD_TOKEN)
