import discord
from discord.ext import commands
import cogs.getdata as getdata
import cogs.func as func
import cogs.gameloop as gameloop

class waiverButton(discord.ui.View):

    @discord.ui.button(label="Sign waiver", style=discord.ButtonStyle.grey, emoji="📝")
    async def sign_waiver(self, button, ctx):
        
        self.users = getdata.users.read_info()
        self.games = getdata.Fetch('./cogs/data/games.json').read_info()
        #if self.games[self.users[str(ctx.user.id)]['game']]['players'][0] == ctx.user.id:
        #    await ctx.response.send_message("You are the one who started this game, you can't sign the waiver.", ephemeral=True)
        #    return

        if self.games[self.users[str(ctx.user.id)]['game']]['started'] == True:
            return
        
        await ctx.response.send_message(f"<@{ctx.user.id}> signed the waiver. Good luck.")
        self.games[self.users[str(ctx.user.id)]['game']]['started'] = True

        getdata.users.update_info(self.users)
        getdata.Fetch('./cogs/data/games.json').update_info(self.games)

        await gameloop.gameloop.turn(ctx)

    @discord.ui.button(label="Decline", style=discord.ButtonStyle.red)
    async def decline_waiver(self, button, ctx):

        self.users = getdata.users.read_info()
        self.games = getdata.Fetch('./cogs/data/games.json').read_info()

        if self.games[self.users[str(ctx.user.id)]['game']]['started'] == True:
            return
        
        gameid = self.users[str(ctx.user.id)]['game']

        await ctx.response.send_message(f"<@{ctx.user.id}> declined the waiver.")
        for a in self.games[self.users[str(ctx.user.id)]['game']]['players']:
            self.users[str(a)]['game'] = "0"

        del self.games[gameid]


        getdata.users.update_info(self.users)
        getdata.Fetch('./cogs/data/games.json').update_info(self.games)

class start(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.users = getdata.users.read_info()
        self.games = getdata.Fetch('./cogs/data/games.json').read_info()

    @commands.slash_command(description="Start a game")
    async def start(self, ctx, opponent):

        isping = func.isping(opponent)

        if not(isping):
            await ctx.respond("You must ping the user in the `opponent section`", ephemeral=True)
            return
        oppid = opponent[2:len(opponent)-1]

        self.games = getdata.Fetch('./cogs/data/games.json').read_info()
        self.users = getdata.users.read_info()
    
        gameid = len(self.games)+1

        gameid = str(gameid)

        self.games = func.initgame(self.games, gameid, [ctx.user.id, int(oppid)])

        try:
            if self.users[str(ctx.user.id)]['game'] != "0":
                await ctx.respond('You are already in a game', ephemeral=True)
                return
            if self.users[oppid]['game'] != "0":
                await ctx.respond('Your opponent is already in a game', ephemeral=True)
                return
        except KeyError:
            pass

        try:
            self.users[str(ctx.user.id)]['game'] = gameid
        except:
            self.users = func.inituser(self.users, str(ctx.user.id))
            self.users[str(ctx.user.id)]['game'] = gameid

        try:
            self.users[oppid]['game'] = gameid
        except:
            self.users = func.inituser(self.users, oppid)
            self.users[oppid]['game'] = gameid

        embed = discord.Embed(
            title='Buckshot Roulette begins...',
            description=f'<@{ctx.user.id}> has challenged {opponent} to a game of Buckshot Roulette. \n\nBefore the fun gets started, this game is deadly, so {opponent} must sign a waiver.',
            color=discord.Colour.from_rgb(54, 36, 15)
        )
        #embed.set_footer(text='React to this message to sign the waiver and start the game!')
        await ctx.respond(embed=embed, view=waiverButton())

        getdata.Fetch('./cogs/data/games.json').update_info(self.games)
        getdata.Fetch('./cogs/data/users.json').update_info(self.users)


def setup(client):
    client.add_cog(start(client))    
