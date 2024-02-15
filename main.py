import discord
from discord.ext import commands
import cogs.getdata as getdata
import json
import os
import cogs.func as func

intents = discord.Intents.default()
intents.messages = True

with open('./token.json', 'r') as file:
    token = json.load(file)['token']

client = commands.Bot(command_prefix='buckshot ', intents=intents)

exclude = ['getdata.py', 'func.py']

for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and (filename not in exclude):
        client.load_extension(f"cogs.{filename[:-3]}")
        print('imported', filename[:-3])

@client.event
async def on_ready():
    #await client.sync_commands()
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    try:
        getdata.users.read_info()[str(message.author.id)]
    except:
        users = getdata.users.read_info()
        
        users = func.inituser(users, str(message.author.id))
        getdata.users.update_info(users)

    await client.process_commands(message)


@client.slash_command(description="Simple testing command")
async def test(ctx):
    print('testing')
    await ctx.respond('Testing')

#@client.slash_command()
#async def sync_modules(ctx):
#    await ctx.respond('syncing modules')
#    await client.sync_commands()
#    await ctx.send('modules synced')
#    print('sync modules')    

client.run(token)
