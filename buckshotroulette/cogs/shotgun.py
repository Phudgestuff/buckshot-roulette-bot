import discord
from discord.ext import commands
from main import client as bot
import cogs.getdata as getdata
import time
import cogs.gameloop as gameloop

shoot = bot.create_group('shoot', 'Fire the shotgun')
end = bot.create_group('end', 'End the game')

class shotgun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @shoot.command(name='self')
    async def attemptedsuicide(ctx):
        try:

            users = getdata.Fetch('./cogs/data/users.json').read_info()
            games = getdata.Fetch('./cogs/data/games.json').read_info()

            uid = str(ctx.user.id)   
            game = games[users[uid]['game']]
            if game['players'].index(int(uid)) == 0:
                oppid = str(game['players'][1])
            else:
                oppid = str(game['players'][0])

            if game['players'].index(int(uid)) != game['turn']:
                await ctx.respond("It's not your turn", ephemeral=True)
                return


            await ctx.respond('You point the shotgun to your chin and...')
            time.sleep(0.7)
            if game['current'] == 'blank':
                await ctx.send("*Click*, it was a blank, you're safe for now")
                game['blanks'] -= 1
                game['sawedoff'] = False

                games[users[uid]['game']] = game
                getdata.Fetch('./cogs/data/games.json').update_info(games)
                await gameloop.gameloop.turn(ctx)

            else:
                if game['sawedoff'] == True:
                    users[uid]['lives'] -= 2
                else:
                    users[uid]['lives'] -= 1

                if users[uid]['lives'] < 1:
                    #if game['round'] == 3:
                    await ctx.send("***BANG***, you take the final shot on yourself. The defibrilator ain't bringing you back this time.")
                    await ctx.send(embed=discord.Embed(
                        title="Game Over",
                        description=f"<@{oppid}> won the game. Congrats, now get back out there and win some more for us.\nAs for <@{uid}>, you've got some work to do, starting with the state of your face.",
                        colour=discord.Color.from_rgb(54, 36, 15)
                    ))
                    
                    await shotgun.endgame(ctx)
                    return
                
                    """else:
                        await ctx.send("**BANG**, you take the shot on yourself and fall to the ground. The defibrilator uses an extra strong charge to bring you from the brink of death onto the next round.")
                        game['round'] += 1

                        game['live'] = 0
                        game['blanks'] = 0
                        
                        users[uid]['maxlives'] += 2
                        users[uid]['lives'] = users[uid]['maxlives']

                        users[oppid]['maxlives'] += 2
                        users[oppid]['lives'] = users[oppid]['maxlives']

                        game['turn'] = game['players'].index(int(oppid))
                        game['live'] -= 1

                    users[uid]['items'] = []
                    users[oppid]['items'] = []
                    games[users[uid]['game']] = game
                    getdata.Fetch('./cogs/data/users.json').update_info(users)
                    getdata.Fetch('./cogs/data/games.json').update_info(games)"""

                    await gameloop.gameloop.turn(ctx)

                else:
                    await ctx.send("**BANG**, you take a shot to your face. Luckily, the defibrilator sends a charge to keep you alive, at the cost of a life.")
                    game['turn'] = game['players'].index(int(oppid))
                    game['live'] -= 1
                    games[users[uid]['game']] = game

                    getdata.Fetch('./cogs/data/users.json').update_info(users)
                    getdata.Fetch('./cogs/data/games.json').update_info(games)

                    await gameloop.gameloop.turn(ctx)


            #getdata.Fetch('./cogs/data/users.json').update_info(users)
            #getdata.Fetch('./cogs/data/games.json').update_info(games)


        
        except KeyError:
            await ctx.respond("An error occured, maybe you aren't in a game?", ephemeral=True)
        except IndexError:
            await ctx.respond("An error occured, maybe you aren't in a game?", ephemeral=True)
    
    @shoot.command()
    async def opponent(ctx):
        try:

            users = getdata.Fetch('./cogs/data/users.json').read_info()
            games = getdata.Fetch('./cogs/data/games.json').read_info()

            uid = str(ctx.user.id)   
            game = games[users[uid]['game']]
            if game['players'].index(int(uid)) == 0:
                oppid = str(game['players'][1])
            else:
                oppid = str(game['players'][0])

            if game['players'].index(int(uid)) != game['turn']:
                await ctx.respond("It's not your turn", ephemeral=True)
                return


            await ctx.respond(f'You point the shotgun at <@{oppid}> and...')
            time.sleep(0.7)
            if game['current'] == 'blank':
                await ctx.send("*Click*, it was a blank, tough luck")
                game['blanks'] -= 1
                game['sawedoff'] = False

                games[users[uid]['game']] = game

                if users[oppid]['cuffed'] == 0:
                    game['turn'] = game['players'].index(int(oppid))
                    game['fullturn'] += 1
                elif users[oppid]['cuffed'] == 1:
                    users[oppid]['cuffed'] = 2
                    await ctx.send(f"<@{oppid}> can't move due to the handcuffs, another turn for <@{uid}>.")
                elif users[oppid]['cuffed'] == 2:
                    users[oppid]['cuffed'] = 0
                    await ctx.send(f"<@{oppid}> broke out of their handcuffs, they can play on now.")
                    game['turn'] = game['players'].index(int(oppid))
                    game['fullturn'] += 1

                getdata.Fetch('./cogs/data/games.json').update_info(games)
                await gameloop.gameloop.turn(ctx)

            else:
                if game['sawedoff'] == True:
                    users[oppid]['lives'] -= 2
                else:
                    users[oppid]['lives'] -= 1

                if users[oppid]['lives'] < 1:
                    #if game['round'] == 3:
                    await ctx.send(f"***BANG***, you take the final shot. The defibrilator ain't bringing them back this time.")
                    await ctx.send(embed=discord.Embed(
                        title="Game Over",
                        description=f"<@{uid}> won the game. Congrats, now get back out there and win some more for us.\nAs for <@{oppid}>, you've got some work to do, starting with the state of your face.",
                        colour=discord.Color.from_rgb(54, 36, 15)
                    ))
                    
                    await shotgun.endgame(ctx)

                    return
                    
                    """else:
                        await ctx.send("**BANG**, you take the shot on yourself and fall to the ground. The defibrilator uses an extra strong charge to bring you from the brink of death onto the next round.")
                        game['round'] += 1

                        game['live'] = 0
                        game['blanks'] = 0
                        
                        users[uid]['maxlives'] += 2
                        users[uid]['lives'] = users[uid]['maxlives']

                        users[oppid]['maxlives'] += 2
                        users[oppid]['lives'] = users[oppid]['maxlives']

                        game['turn'] = game['players'].index(int(oppid))
                        game['live'] -= 1

                    users[uid]['items'] = []
                    users[oppid]['items'] = []
                    games[users[uid]['game']] = game
                    getdata.Fetch('./cogs/data/users.json').update_info(users)
                    getdata.Fetch('./cogs/data/games.json').update_info(games)"""

                    #await gameloop.gameloop.turn(ctx)

                else:
                    await ctx.send(f"**BANG**, you take a shot. Unlucky for you, the defibrilator sends a charge to keep them alive, at the cost of a life.")
                    
                    if users[oppid]['cuffed'] == 0:
                        game['turn'] = game['players'].index(int(oppid))
                        game['fullturn'] += 1
                    elif users[oppid]['cuffed'] == 1:
                        users[oppid]['cuffed'] = 2
                        await ctx.send(f"<@{oppid}> can't move due to the handcuffs, another turn for <@{uid}>.")
                    elif users[oppid]['cuffed'] == 2:
                        users[oppid]['cuffed'] = 0
                        await ctx.send(f"<@{oppid}> broke out of their handcuffs, they can play on now.")
                        game['turn'] = game['players'].index(int(oppid))
                        game['fullturn'] += 1
                    
                    game['live'] -= 1
                    games[users[uid]['game']] = game

                    getdata.Fetch('./cogs/data/users.json').update_info(users)
                    getdata.Fetch('./cogs/data/games.json').update_info(games)

                    await gameloop.gameloop.turn(ctx)


            #getdata.Fetch('./cogs/data/users.json').update_info(users)
            #getdata.Fetch('./cogs/data/games.json').update_info(games)


        
        except KeyError:
            await ctx.respond("An error occured, maybe you aren't in a game?", ephemeral=True)
        except IndexError:
            await ctx.respond("An error occured, maybe you aren't in a game?", ephemeral=True)

    @end.command()
    async def game(ctx):
        await shotgun.endgame(ctx)
        await ctx.respond("Game ended, stats restored, better luck next time.")


    async def endgame(ctx):
        users = getdata.Fetch('./cogs/data/users.json').read_info()
        games = getdata.Fetch('./cogs/data/games.json').read_info()

        uid = str(ctx.user.id)   
        game = games[users[uid]['game']]

        if game['players'].index(int(uid)) == 0:
            oppid = str(game['players'][1])
        else:
            oppid = str(game['players'][0])

        del games[users[uid]['game']]

        users[uid]['lives'] = 6
        users[uid]['maxlives'] = 6
        users[oppid]['lives'] = 6
        users[oppid]['maxlives'] = 6
        users[uid]['game'] = "0"
        users[oppid]['game'] = "0"
        users[uid]['items'] = []
        users[oppid]['items'] = []

        getdata.Fetch('./cogs/data/users.json').update_info(users)
        getdata.Fetch('./cogs/data/games.json').update_info(games)


def setup(client):
    client.add_cog(shotgun(client))