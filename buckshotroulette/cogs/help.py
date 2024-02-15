import discord
from discord.ext import commands

class help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(description="Explains what commands do/how to play.")
    async def help(self, ctx):
        string = '''# Commands
**Basic commands**
`/start <opponent>`
This command will request a game against an opponent. The opponent must accept (sign the waiver) for the game to start.

`/end game`
Ends the current game.

**In-game**
The basic loop of the game involves shooting either yourself or your opponent with a shotgun that has varied probabilities to have either a live shell or a blank shell.
Items exist to manipulate the chances, increase effects or help figure out your odds.

**Shotgun commands**
`/shoot self`
To shoot oneself. If it is live, you lose a life. If it is blank, you get an extra turn.

`/shoot opponent`
To shoot the opponent. If it is live, they lose a life. If it is blank, nothing happens and the turn ends.

**Items**
You will gain 4 items per turn. The `/use` prefix is used to activate their effects.

`/use lens`
Find out what the current shell in the gun is. Your opponent can't see this.

`/use beer`
Eject whatever shell is in the gun.

`/use saw`
Double the damage that your shot will do. Only lasts for one turn and is wasted if the shot is blank.

`/use handcuffs`
Make your opponent skip their next turn. Shooting yourself with a blank will not affect this.

`/use cigarette`
Gain one extra life. You cannot over-heal.
'''
        await ctx.respond(embed=discord.Embed(
            title="Buckshot Roulette: Help",
            description=string,
            colour=discord.Colour.from_rgb(54, 36, 15)
        ))

def setup(client):
    client.add_cog(help(client))