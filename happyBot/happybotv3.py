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

#MusicPlayer
mp = MusicPlayer()

#Using the on_ready() event handler to begin tasks
@client.event
async def on_ready():
    global mp
    await mp.start_music_player_connections(client)
    for vc in mp.client_list:
        print(f"{vc} is starting")
        song = random.choice(list(mp.library.values()))
        await mp.play_song(song, vc, discord)
    #tasks
    # scrape_web.start()
    # goodmorning.start(guild_dict_gc)
    # new_user_of_the_week.start(guild_dict_gc)
    musicplayer.start()
    

#when DM'd happybot logs the suggestion
@client.event
async def on_message(message):
    #DM to HappyBot
    if isinstance(message.channel, discord.channel.DMChannel) and message.author != client.user:
        if "suggestion" in message.content.lower().split(" ")[0]:
            with open("../data/logs/happybot_feedback.txt","a") as log:
                log.write(f'\n{datetime.datetime.now()}\n{message.author.name.split("#")[0]}:\n{message.content}\n\n')
                await message.channel.send(f'Suggestion added, thank yous {message.author.name.split("#")[0]}!')
        
        elif "restart_players" in message.content.lower().split(" ")[0]:
            print("restarting all players")
            await mp.close_vc_connections(client)
            await mp.start_music_player_connections(client)
            musicplayer.restart()
        
        elif "list_songs" in message.content.lower().split(" ")[0]:
            string = "\n\n".join(os.listdir("../data/mp3s"))
            await message.channel.send(string)
        
        elif "change_song" in message.content.lower().split(" ")[0]:
            if message.content.split(" ")[1] in os.listdir("../data/mp3s"):
                await mp.close_vc_connections(client)
                await mp.start_music_player_connections(client)
                musicplayer.restart()
            else:
                await message.channel.send("song not in available list: use command list_songs to view available songs")

        elif "download_song" in message.content.lower().split(" ")[0]:
            ws = WebScraper()
            response = ws.scrape_youtube(message.content.split(" ")[1])
            ws.quit()
            await message.channel.send(response)
        
        else:
            await message.channel.send(f'Hello I am HappyBot!\n\ncommands:\n\nlist_songs -> lists available mp3s\nchange_song <song_name> -> change currently playing song to another song in library\ndownload_song <youtube_link> -> will download a youtube link and add song to library')
            
    

#on member join happybot welcomes them with a gif
@client.event
async def on_member_join(member):
    await member.send(f'Welcome {member.name.split("#")[0]}\n')
    await member.send(file=discord.File(pick_random_welcome_gif()))
    user = User(member.name, member.id, member.guild, "NaN","NaN","NaN")
    print(user)
    with open("../data/logs/new_member.log","a") as new_members:
        new_members.write(f"\n\n{user.username}, {user.user_id}, {user.guild}\n\n")




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

    

#music player
@tasks.loop(seconds=30)
async def musicplayer():
    global mp
    if mp.is_playing != True:
        return "Nothing playing"
    elif mp.is_playing != False:
        print(mp.library)



                


client.run(DISCORD_TOKEN)
