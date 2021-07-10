#!/home/linuxbrew/.linuxbrew/bin/python3


#Happy Bot v1

#TODO add a webscraper for gif or query discord api for gifs


#import depenedancies
import datetime
import discord
from config import DISCORD_TOKEN
from config import DISCORD_GUILD
from table_data import read_table, write_csv

#Create intents object to hand to the client instance
intents = discord.Intents.all()

#Create the Client instance imported from the discord library with the intents arguement provided
client = discord.Client(intents=intents)

#Using the on_ready() event handler
@client.event
async def on_ready():
    print(f"{client.user} is running")

#printing to the console the guild and guildmembers
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == DISCORD_GUILD:
            break
    print(f"{client.user} is connected to the following guild:\n{guild.name}(id: {guild.id})")
    print("\nMembers in the Server:")
    for member in guild.members:
        print(member)
    print("\nChannels in server:")
    #for channel in 


#sending direct message to new members
@client.event
async def on_member_join(member):
    #the await keyword suspends the execution of the surrounding coroutine until the execution of the each coroutine has finished
    await member.create_dm()
    await member.dm_channel.send(f"HappyBot happily welcomes you {member.name} to {DISCORD_GUILD}")


happy_counter = 0
snake_counter = 0

#Responding to messages
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    elif "i love you" in message.content.lower():
        await message.channel.send(f"{str(client.user).split('#')[0]} feels love too {str(message.author).split('#')[0]}")
        
    elif "happybot" in message.content.lower():
        global happy_counter
        happy_counter += 1
        with open("message.txt","a") as msg_file:
            msg_file.write(f"\n{message.content}\n{datetime.datetime.now()}\n")
        if happy_counter == 5:
            await message.channel.send(f"{str(client.user).split('#')[0]} feels popular")
            return
        await message.channel.send(f"{str(client.user).split('#')[0]} is listening")
    

    #snake logic
    elif "snake" in message.content.lower() or "serpent" in message.content.lower() or "eel" in message.content.lower():
        df = read_table()
        df.loc[0] += 1
        mentioned = df.loc[0].item()
        write_csv(df)
        global snake_counter
        snake_counter += 1
        if snake_counter >= 10:
            await message.channel.send(f"snakes mentioned {mentioned} times!")
            snake_counter = 0


        


client.run(DISCORD_TOKEN)
