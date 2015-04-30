import os
import multiprocessing

ranks = ['0','1','2','3','4','5','6','7','8','9','T','J','Q','K','A']
suits = ['c','d','h','s']

leavingHandActions = ['f','K','-','Q']

def readpdbh(path):
  try:
    pdb = open(path,"r")
  except FileNotFoundError as e:
    print("{} not found".format(path))
    return None,None
  playername = "" 
  playerdata = {}

  for line in pdb:
    try: # data set irregular, so throw out bad lines
    

      data = line.split()
      assert(len(line) >= 11)

      player = data[0]            # column 1        player nickname
      ts = int(data[1])           # column 2        timestamp of this hand (see HDB)
      numCards = int(data[2])     # column 3        number of player dealt cards
      playerPos = int(data[3])    # column 4        position of player (starting at 1, in order of cards received)

      preflop = data[4]
      flop = data[5]
      turn = data[6]
      river = data[7]

      startBank = int(data[8])    # column 10       player's bankroll at start of hand       
      totalBet = int(data[9])    # column 11       total action of player during hand
      totalWin = int(data[10])    # column 12       amount of pot won by player

      
      handActions = [preflop, flop, turn, river]
      finished = True
      if '-' in handActions:
        foundGameExit = False
        for betAction in handActions:
          for action in list(betAction): # since betAction can be cf (call then fold)
            foundGameExit = foundGameExit or action in leavingHandActions
        assert(foundGameExit)
        finished = False
    
      if(playername != ""):
        assert(playername == player)
      else:
        playername = player

      if finished:
        cards = data[11:]           # column 13+      pocket cards of player (if revealed at showdown)
        for card in cards:
          assert(card[0] in ranks)
          assert(card[1] in suits)


        handdata = {"hand": cards, "winnings": totalWin - totalBet}
        playerdata[ts] = handdata

    except AssertionError as e: # if we have an invalid row, just forget about it
      print("INVALID {}".format(line))
      continue
    
  pdb.close()
  if p7i % 100 == 0:
    print('.',end='',flush=True)
  return playername, playerdata



def readpdb7(path):

  try:
    pdb = open(path,"r")
  except FileNotFoundError as e:
    print("{} not found".format(path))
    return None,None
 
  playername = "" 
  playerdata = {}
  for line in pdb:
    try: # data set irregular, so throw out bad lines
    

      data = line.split()
      assert(len(line) >= 13)

      player = data[0]            # column 1        player nickname
      ts = int(data[1])           # column 2        timestamp of this hand (see HDB)
      numCards = int(data[2])     # column 3        number of player dealt cards
      playerPos = int(data[3])    # column 4        position of player (starting at 1, in order of cards received)

      postcard3 = data[4]         # column 5        betting action
      postcard4 = data[5]         # column 6        betting action
      postcard5 = data[6]         # column 7        betting action
      postcard6 = data[7]         # column 8        betting action
      postcard7 = data[8]         # column 9        betting action 

      startBank = int(data[9])    # column 10       player's bankroll at start of hand       
      totalBet = int(data[10])    # column 11       total action of player during hand
      totalWin = int(data[11])    # column 12       amount of pot won by player

      cards = data[12:]           # column 13+      pocket cards of player (if revealed at showdown)
      for card in cards:
        assert(card[0] in ranks)
        assert(card[1] in suits)
      
      handActions = [postcard3,postcard4,postcard5,postcard6,postcard7]
      if '-' in handActions:
        assert(len(cards) >= 1)
        foundGameExit = False
        for betAction in handActions:
          for action in list(betAction): # since betAction can be cf (call then fold)
            foundGameExit = foundGameExit or action in leavingHandActions
        assert(foundGameExit)
    
      if(playername != ""):
        assert(playername == player)
      else:
        playername = player

      
      if(len(cards) == 7): # if they made it to the end, include this
        handdata = {"hand": cards, "winnings": totalWin - totalBet}
        playerdata[ts] = handdata

    except AssertionError as e: # if we have an invalid row, just forget about it
      print("INVALID {}".format(line))
      continue
    
  pdb.close()
  print("done with player")
  return playername, playerdata

# read hroster file from ./7stud/game/hroster
# return dict of playernick->game_timestamp[]
def readhroster(game,holdem):
  if holdem:
    pathstr = "./holdem/{}/hroster"
  else:
    pathstr = "./7stud/{}/hroster"
  
  path = pathstr.format(game)
  hroster = open(path,"r")
  playerDB = {} 
  for line in hroster: 
    data = line.split() 
    ts = int(data[0])       # column 1        timestamp
    numCards = int(data[1]) # column 2        number of player dealt cards
    players = data[2:]      # column 3+       player nicknames
  
    for p in players:
      playerDB.setdefault(p,[])
      playerDB[p].append(ts)
  
  hroster.close()
  return playerDB
    

def correlateWithBoard(game,playerHandDB):
  hdb = open("./holdem/{}/hdb".format(game),"r")
  for line in hdb:
    data = line.split()
    ts = int(data[0])

    if len(data) < 8:
      continue

    board = data[8:]

    for player, games in playerHandDB.items():
      for ts2, handData in games.items():
        if ts == ts2:
          playerHandDB[player][ts]["hand"] += board

  print("done with player")
  return playerHandDB
        

def readPlayers(game,players,holdem):
  if holdem:
    pathstr = "./holdem/{}/pdb/pdb.{}"
  else:
    pathstr = "./7stud/{}/pdb/pdb.{}"

  paths = list(map(lambda x: pathstr.format(game,x), players))

  pool = multiprocessing.Pool(4)
  if holdem:
    out = pool.map(readpdbh,paths)
  else:
    out = pool.map(readpdb7,paths)
  out = dict(out)

  if holdem:
    out = correlateWithBoard(game,out)
    
  return out
    

def getData(holdem,game):
  playerDB = readhroster(game,holdem)
  playerHandDB = readPlayers(game,playerDB.keys(),holdem)

  
  try:
    del playerDB[None]
  except KeyError:
    print("we got lucky")  

  try:
    del playerHandDB[None]
  except KeyError:
    print("we got lucky")  


  """ not every player made it
  for player in playerDB.keys():
    handSet = set(playerDB[player])
    
    finishedSet = playerHandDB[player].keys()

    # each game they finished should be a game they played
    assert(finishedSet <= handSet)
  """
  
  handDB = {}
  for player, hands in playerHandDB.items():
    
    for ts, handData in hands.items():
      hand = handData["hand"]
      hand = sorted(hand)
      hand = ",".join(hand)
      handDB.setdefault(hand,[])
      handDB[hand].append(handData["winnings"])
      
  return handDB
  
def readAllGames(path):
  games = os.listdir("./7stud")
  print("Found {} games".format(len(games)))
  masterHandList = {}
  for g in games:
    print("Reading {}".format(g))
    gameDB = getData(False,g)
    for k in gameDB.keys():
      masterHandList.setdefault(k,[])
      masterHandList[k] += gameDB[k]

  games = os.listdir("./holdem")
  print("Found {} games".format(len(games)))
  for g in games:
    print("Reading {}".format(g))
    gameDB = getData(True,g)
    for k in gameDB.keys():
      masterHandList.setdefault(k,[])
      masterHandList[k] += gameDB[k]
  
  return masterHandList
