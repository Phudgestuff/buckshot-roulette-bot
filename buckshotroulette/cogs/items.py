import discord
from discord.ext import commands
from main import client as bot
import cogs.getdata as getdata
import random
import cogs.gameloop as gameloop

use = bot.create_group('use', 'Use Items')

class items(commands.Cog):
    def __init__(self, client):
        self.client = client

    @use.command(description="Restore lives by one")
    async def cigarette(ctx):
        users = getdata.Fetch('./cogs/data/users.json').read_info()
        games = getdata.Fetch('./cogs/data/games.json').read_info()

        if games[users[str(ctx.user.id)]['game']]['players'].index(ctx.user.id) != games[users[str(ctx.user.id)]['game']]['turn']:
            await ctx.respond("It's not your turn", ephemeral=True)
            return

        if 1 not in users[str(ctx.user.id)]['items']:
            await ctx.respond('You do not have this item.', ephemeral=True)
            return

        users[str(ctx.user.id)]['lives'] += 1
        if users[str(ctx.user.id)]['lives'] > 6:
            users[str(ctx.user.id)]['lives'] = 6
        await ctx.respond(f'You smoke a cigarette and restore 1 life. You have {users[str(ctx.user.id)]["lives"]} lives now.')

        for a in range(0, len(users[str(ctx.user.id)]['items'])):
            if users[str(ctx.user.id)]['items'][a] == 1:
                users[str(ctx.user.id)]['items'].pop(a)
                break

        getdata.Fetch('./cogs/data/users.json').update_info(users)

    @use.command(description="Saw off the end of the shotgun. Do double damage.")
    async def saw(ctx):
        users = getdata.Fetch('./cogs/data/users.json').read_info()
        games = getdata.Fetch('./cogs/data/games.json').read_info()
        game = games[users[str(ctx.user.id)]['game']]

        if games[users[str(ctx.user.id)]['game']]['players'].index(ctx.user.id) != games[users[str(ctx.user.id)]['game']]['turn']:
            await ctx.respond("It's not your turn", ephemeral=True)
            return

        if 3 not in users[str(ctx.user.id)]['items']:
            await ctx.respond('You do not have this item.', ephemeral=True)
            return

        game['sawedoff'] = True
        await ctx.respond(f'You saw off the end of the shotgun, it will now do 2 damage to the opponent.')

        for a in range(0, len(users[str(ctx.user.id)]['items'])):
            if users[str(ctx.user.id)]['items'][a] == 3:
                users[str(ctx.user.id)]['items'].pop(a)
                break
            
        games[users[str(ctx.user.id)]['game']] = game
        getdata.Fetch('./cogs/data/users.json').update_info(users)
        getdata.Fetch('./cogs/data/games.json').update_info(games)

    @use.command(description='See the shell in the gun')
    async def lens(ctx):
        users = getdata.Fetch('./cogs/data/users.json').read_info()
        games = getdata.Fetch('./cogs/data/games.json').read_info()
        game = games[users[str(ctx.user.id)]['game']]

        if games[users[str(ctx.user.id)]['game']]['players'].index(ctx.user.id) != games[users[str(ctx.user.id)]['game']]['turn']:
            await ctx.respond("It's not your turn", ephemeral=True)
            return

        if 0 not in users[str(ctx.user.id)]['items']:
            await ctx.respond('You do not have this item.', ephemeral=True)
            return

        await ctx.respond(f"The shell is {game['current']}", ephemeral=True)
        await ctx.respond('You crack the magnifying glass over the table and take a look at the shell.')

        for a in range(0, len(users[str(ctx.user.id)]['items'])):
            if users[str(ctx.user.id)]['items'][a] == 0:
                users[str(ctx.user.id)]['items'].pop(a)
                break

        games[users[str(ctx.user.id)]['game']] = game
        getdata.Fetch('./cogs/data/users.json').update_info(users)
        getdata.Fetch('./cogs/data/games.json').update_info(games)        

    @use.command(description='Chug to waste a shell')
    async def beer(ctx):
        users = getdata.Fetch('./cogs/data/users.json').read_info()
        games = getdata.Fetch('./cogs/data/games.json').read_info()
        game = games[users[str(ctx.user.id)]['game']]

        if games[users[str(ctx.user.id)]['game']]['players'].index(ctx.user.id) != games[users[str(ctx.user.id)]['game']]['turn']:
            await ctx.respond("It's not your turn", ephemeral=True)
            return

        if 2 not in users[str(ctx.user.id)]['items']:
            await ctx.respond('You do not have this item.', ephemeral=True)
            return

        if game['current'] == 'blank': # decreasing the current shell by one
            game['blanks'] -= 1
        else: # if it is live
            game['live'] -= 1


        if game['blanks'] <= 0 and game['live'] <= 0: # if it was the last bullet in the gun
            await ctx.respond(f"You chug a can of beer and eject a {game['current']} shell from the shotgun. It's the last bullet, so the shells are reloaded in a new turn.")
            
            for a in range(0, len(users[str(ctx.user.id)]['items'])):
                if users[str(ctx.user.id)]['items'][a] == 2:
                    users[str(ctx.user.id)]['items'].pop(a)
                    break

            games[users[str(ctx.user.id)]['game']] = game
            getdata.Fetch('./cogs/data/users.json').update_info(users)
            getdata.Fetch('./cogs/data/games.json').update_info(games)  
            await gameloop.gameloop(ctx) # new turn starts
            return


        await ctx.respond(f'You chug a can of beer and eject a {game["current"]} shell from the shotgun.')

        val = False
        while val == False:
            rInt = random.randint(1,2) # random round, re-randomises if shell type is at 0
            if rInt == 1 and game['blanks'] != 0:
                game['current'] = 'blank'
                val = True
            if rInt == 2 and game['live'] != 0:
                game['current'] = 'live'
                val = True

        for a in range(0, len(users[str(ctx.user.id)]['items'])):
            if users[str(ctx.user.id)]['items'][a] == 2:
                users[str(ctx.user.id)]['items'].pop(a)
                break

        games[users[str(ctx.user.id)]['game']] = game
        getdata.Fetch('./cogs/data/users.json').update_info(users)
        getdata.Fetch('./cogs/data/games.json').update_info(games)   

    @use.command(description='Make the opponent skip a turn')
    async def handcuffs(ctx):
        users = getdata.Fetch('./cogs/data/users.json').read_info()
        games = getdata.Fetch('./cogs/data/games.json').read_info()
        game = games[users[str(ctx.user.id)]['game']]

        if games[users[str(ctx.user.id)]['game']]['players'].index(ctx.user.id) != games[users[str(ctx.user.id)]['game']]['turn']:
            await ctx.respond("It's not your turn", ephemeral=True)
            return

        if 4 not in users[str(ctx.user.id)]['items']:
            await ctx.respond('You do not have this item.', ephemeral=True)
            return

        if game['players'].index(ctx.user.id) == 0:
            oppid = str(game['players'][1])
        else:
            oppid = str(game['players'][0])

        users[oppid]['cuffed'] = 1
        await ctx.respond(f"You place handcuffs around <@{oppid}>. Their next turn is skipped.")

        for a in range(0, len(users[str(ctx.user.id)]['items'])):
            if users[str(ctx.user.id)]['items'][a] == 4:
                users[str(ctx.user.id)]['items'].pop(a)
                break
        
        games[users[str(ctx.user.id)]['game']] = game
        getdata.Fetch('./cogs/data/users.json').update_info(users)
        getdata.Fetch('./cogs/data/games.json').update_info(games)  

def setup(client):
    client.add_cog(items(client))    