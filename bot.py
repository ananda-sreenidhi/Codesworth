# bot.py
import os

import discord
from dotenv import load_dotenv

from discord.ext import commands

from weather import codesworth_weather
from lenny import codesworth_lenny
from wiki import codesworth_wikipedia
from currency import codesworth_currency

import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

command_list = [".currency", ".cc", ".wiki", ".wikipedia", ".weather", ".we", ".choose", ".ch", ".tell", ".t", ".lenny", ".le"]


@client.event
async def on_ready():
    guild = discord.utils.find(lambda x: x.name == GUILD, client.guilds)        
    print(f"{client.user} has connected to {guild.name}! The guild ID is {guild.id}")
    members = [(member.name, member.id) for member in guild.members]

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Hi {member.name}, welcome to the test server! Please make sure to check out #rules and come say hi when you\'re done!')
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content[0] == '.' and message.content.split()[0] not in command_list:
        await message.channel.send("An error has occured!")
        raise 

    if message.content.split()[0].lower() in [".we", ".weather"]:
        (a, x, y, z, w) = codesworth_weather(message.content.split()[1])
        embed = discord.Embed(title="Weather information for {}".format(a), color=0xffbf00)
        embed.add_field(name="Temperature", value=str(x)+"°C", inline=True)
        embed.add_field(name="Pressure", value=str(y)+" hPa", inline=True)
        embed.add_field(name="Humidity", value=str(z)+"%", inline=True)
        embed.add_field(name="Description", value=str(w).capitalize(), inline=True)
        await message.channel.send(embed=embed)

    if message.content.split()[0].lower() in [".wiki", ".wikipedia"]:
        response = codesworth_wikipedia(' '.join(message.content.split()[1:]))
        if response[0] == 0:
            (a, b, c, d) = response[1:] 
            embed = discord.Embed(title = "Wikipedia article for \"{}\"".format(' '.join(message.content.split()[1:])), url = c, color = 0xffbf00)
            embed.add_field(name = "{}".format(a), value = b, inline = False)
            embed.set_image(url=d)
            embed.set_footer(text = "Click the title to read more.")
            
        else:
            (p, q) = response[1:]
            embed = discord.Embed(color = 0xffbf00)
            embed.add_field(name = "Disambiguation error!", value = p, inline = False)
            embed.set_footer(text = q)
            
        await message.channel.send(embed=embed)

    if message.content.split()[0].lower() in [".lenny", ".le"]:
        if len(message.content.split()) >1:
            arg = message.content.split()[1].lower()
        else:
            arg = "regular"
        response = codesworth_lenny(arg)
        await message.channel.send(response)

    if message.content.split()[0].lower() in [".choose", ".ch"]:
        rlist = [i for i in ' '.join(message.content.split()[1:]).split(',') if len(i)>=0]
        response = random.choice(rlist)
        await message.channel.send(response)

    if message.content.split()[0].lower() in [".tell", ".t"]:
       msg = ' '.join(message.content.split()[2:])
       guild = discord.utils.find(lambda x: x.name == GUILD, client.guilds)        
       members = [(member.name, member.id) for member in guild.members]
       msg = str(message.author.name)+" said: "+msg
       if message.content.split()[1].lower() in [i[0].lower() for i in members]:
           u_id = [i[1] for i in members if message.content.split()[1].lower() == i[0].lower()][0]
           user = client.get_user(u_id)
           if user is not None:
               await user.send(msg)
               await message.channel.send("Message sent to {}!".format(message.content.split()[1]))

    if message.content.split()[0].lower() in [".currency", ".cc"]:
        a = eval(message.content.split()[1])
        f = message.content.split()[2]
        t = message.content.split()[3]
        response = codesworth_currency(a, f, t)
        await message.channel.send(response)
    
@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == "on_message":
            f.write(f'Unhandled message: {args[0]}\n')
            await client.send_message(message.channel, "An error has occured!")
        else:
            raise 
        
client.run(TOKEN)


