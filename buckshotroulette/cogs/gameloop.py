import discord
from discord.ext import commands
import cogs.getdata as getdata
import cogs.func as func
import random

class gameloop(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.items = ['🔍', '🚬', '🍺', '🪚', '🔗']

    def shells_init(self, game):

        #if game['turn'] == 1:
        #    game['turn'] = 0
        #else:
        #    game['turn'] = 1


        if game['live'] < 1 and game['blanks'] < 1: # beginning of a new sub-round

            game['subround'] += 1

            if game['subround'] == 1: # how shells are layed out depending on sub-round
                game['blanks'] = 1
                game['live'] = 2
            elif game['subround'] == 2:
                game['live'] = 2
                game['blanks'] = 2
            elif game['subround'] == 3:
                game['blanks'] = 3
                game['live'] = 2
            elif game['subround'] == 4:
                game['blanks'] = 3
                game['live'] = 3
            elif game['subround'] == 5:
                game['blanks'] = 4
                game['live'] = 3
            else:
                game['blanks'] = 4
                game['live'] = 4

        return game


    @commands.command()
    async def turn(self, ctx):
        self.games = getdata.Fetch('./cogs/data/games.json').read_info()
        self.users = getdata.Fetch('./cogs/data/users.json').read_info()

        uid = str(ctx.user.id)
        gameid = self.users[uid]['game']
        uid = str(self.games[gameid]['players'][0])
        game = self.games[gameid]
        oppid = str(game['players'][1])
        first = False


        if game['fullturn'] == 2:
            for a in range(0, 4):
                self.users[uid]['items'].append(random.randint(0,len(self.items)-1))
                self.users[oppid]['items'].append(random.randint(0,len(self.items)-1))
            game['fullturn'] = 0

        if len(self.users[uid]['items']) > 8:
            self.users[uid]['items'] = self.users[uid]['items'][:8]
        if len(self.users[oppid]['items']) > 8:
            self.users[oppid]['items'] = self.users[oppid]['items'][:8]

        if game['live'] < 1 and game['blanks'] < 1:
            first = True
        else:
            shotgunstring = ''

        game = self.shells_init(self.games[gameid]) # inits player turn, what rounds are added in when live and blank reaches 0, what the current shell type is

        if first:
            shotgunstring = f'**Shells loaded**:{game["live"]} live shells and {game["blanks"]} blank shell(s) have been loaded in a random order.\n'

        val = False
        while val == False:
            rInt = random.randint(1,2) # random round, re-randomises if shell type is at 0
            if rInt == 1 and game['blanks'] != 0:
                game['current'] = 'blank'
                val = True
            if rInt == 2 and game['live'] != 0:
                game['current'] = 'live'
                val = True
        
        self.games[gameid] = game
        getdata.Fetch('./cogs/data/games.json').update_info(self.games)

        itemstringuser = ''
        itemstringopp = ''

        shotgunstring += f"The shotgun lies on the table, awaiting <@{game['players'][game['turn']]}>'s action..."

        itemstringuser = '| '
        itemstringopp = '| '

        fid = str(self.games[gameid]['players'][0])
        for x in self.users[fid]['items']:
            itemstringuser += f'{self.items[x]} | '
        for x in self.users[oppid]['items']:
            itemstringopp += f'{self.items[x]} | '

        embed = discord.Embed(
            title=f'Buckshot Roulette: Classic mode',
            description=f"""<@{fid}>
***Lives***: **{self.users[fid]['lives']}** out of **{self.users[fid]['maxlives']}**
{itemstringuser}

-
        {shotgunstring}
-
    
<@{oppid}>
***Lives***: **{self.users[oppid]['lives']}** out of **{self.users[oppid]['maxlives']}**

{itemstringopp}""",
            colour=discord.Color.from_rgb(54, 36, 15)
        )
        embed.set_footer(text="Use `/help` to figure out how to actually play.")
        embed.set_thumbnail(url="https://static.wikia.nocookie.net/villains/images/4/4e/The_Dealer_%28Buckshot_Roulette%29.png/revision/latest/scale-to-width-down/250?cb=20231230210541")
        
        try:
            await ctx.send(embed=embed)
        except AttributeError:
            await ctx.followup.send(embed=embed)

        #getdata.Fetch('./cogs/data/games.json').update_info(self.games)
        getdata.Fetch('./cogs/data/users.json').update_info(self.users)

def setup(client):
    client.add_cog(gameloop(client))   