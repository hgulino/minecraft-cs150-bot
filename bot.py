# bot.py
import os
import random
import asyncio

import discord
from dotenv import load_dotenv
from mcstatus import MinecraftServer

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
MC_SERVER = os.getenv('MC_SERVER')

client = discord.Client()

server = MinecraftServer.lookup(MC_SERVER)

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    
    text_channel_id = '';
    for s in client.guilds:
        for channel in s.channels:
            if channel.name == 'minecraft-status':
                text_channel_id = channel.id
    if text_channel_id == '':
        print('no valid channel. Please name one minecraft-status.')
        return
    print(text_channel_id)

    channel = client.get_channel(text_channel_id)

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    minecraft_quotes = [
        'Wash your hands!',
        'Soap and water!',
        'Support local businesses!',
        'Stay home and play games!',
        'Stay safe!',
        'Stay strong!',
        'Cough or sneeze into your elbow!',
        'Don’t touch your face!',
        'Support elderly relatives and friends!',
        'Prepare, but don’t hoard!',
        'Gamers unite – separately in your own homes!',
        'Save the world – stay inside!',
        'Shop for your elders!',
        'Hang out with your friends online!'
    ]

    response = random.choice(minecraft_quotes)
    msg = await channel.send(response)
    TEN_MINUTES_IN_THIRTY_SECOND_INTERVALS = 20
    tenMinuteCounter = 0

    status = await channel.send("Pinging: " + MC_SERVER)

    while True:
        if tenMinuteCounter == TEN_MINUTES_IN_THIRTY_SECOND_INTERVALS:
            tenMinuteCounter = 0
            response = random.choice(minecraft_quotes)
            await msg.edit(content=response)
        else:
            tenMinuteCounter += 1
        
        query = server.query()
        
        if query.players.names:
            await status.edit(content="The server has the following players online: {0}".format(", ".join(query.players.names)))
        else:
            await status.edit(content="No users are currently online 😢")
        await asyncio.sleep(30)
        
client.run(TOKEN)


