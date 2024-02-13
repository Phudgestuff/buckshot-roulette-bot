
def isping(string):
    if string[:2] != "<@":
        return False
    
    else:
        return True
    
def initgame(games, gameid, players): # games: {}, gameid:int, players: []
    games[gameid] = {
        'players': players,
        #'round': 1,
        'turn': 0,
        'blanks':0,
        'live':0,
        'sawedoff': False,
        'started': False,
        'current':'blank',
        'subround': 0,
        'fullturn':2
    }
    return games

def inituser(users, uid): # users: {}, uid:string
    users[uid] = {
        'game':"0",
        'lives':6,
        'maxlives':6,
        'wins':0,
        'losses':0,
        'items':[], # maximum of 8
        'cuffed':0
    }
    return users