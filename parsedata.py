from pprint import pprint as pp

"""
The betting action is encoded with a single character for each action:

        -       no action; player is no longer contesting pot
        B       blind bet
        f       fold
        k       check
        b       bet
        c       call
        r       raise
        A       all-in
        Q       quits game
        K       kicked from game
"""
bet_dict = {
  '-':'no action',
  'r':'raise',
  'f':'fold',
  'c':'call',
  'b':'bet',
  'B':'Blind bet',
  'Q':'Quits game',
  'k':'check',
  'K':'Kicked',
  'A':'All in'
}

def readhdb(path):
  hands = open(path+"/hdb")
  j = 0
  match = {}
  for line in hands:
    line = line.replace('\n','')
    ourdata = line.split()
    """
      column 1        timestamp (supposed to be unique integer)
      column 2        game set # (incremented when column 3 resets)
      column 3        game # reported by dealer bot
      column 4        number of players dealt cards
      column 5        number of players who see the flop
      column 6        pot size at beginning of flop
      column 7        number of players who see the flop
      column 8        pot size at beginning of turn
      column 9        number of players who see the flop
      column 10       pot size at beginning of river
      column 11       number of players who see the flop
      column 12       pot size at showdown
      column 13+      cards on board (0, 3, 4 or 5)
    """
  
    timestamp = int(ourdata[0])
    setnum = int(ourdata[1])
    handnum = int(ourdata[2])

  #  print(line)
    numplayers = int(ourdata[3])
    flop = ourdata[4]
    turn = ourdata[5]
    river = ourdata[6]
    
    showdn = ourdata[7]

    boardlen = 5 - ((3*(flop[0] == '0')) + (turn[0] == '0') + (river[0]=='0'))
    if boardlen != 0:
      board = ourdata[(-1)*boardlen:]
    else:
      board = []
      
  #  print(numplayers,flop,turn,river,showdn,board)
    hand = {'ts':timestamp,'set':setnum, 'handnum':handnum, 'players': numplayers, 'flop':flop, 'turn': turn, 'river':river, 'showdown': showdn, 'board': board}
    match[timestamp] = hand
  return match

  
def readhroster(path):
  roster = open(path+"/hroster")
  records = {}
  for line in roster:
    line = line.replace('\n','')
    rline = line.split()
    ts = int(rline[0])
    numplayers = int(rline[1])
    players = []
    for i in range(numplayers):
      players.append(rline[2+i])
    record = {'ts':ts, 'players':numplayers, 'roster':players}
    records[ts] = record 
  return records


def readpdb(path,playerset,holdem):
  playerdata = {}
  for p in playerset:
    player = open(path+'/pdb/pdb.'+p)
    playerdata.setdefault(p,{})
    for line in player:
      data = line.split()
      name = data[0]    
      assert(name == p)
      ts = int(data[1])
      dealt = data[2] # dealt cards
      position = data[3] # position from dealer

      initial_bet = data[4]

      flop_bet = data[5]
      turn_bet = data[6]
      showdown_bet = data[7]

      total_money = data[8]
      total_bet = data[9]
      winnings = data[10]    

      folded = (flop_bet == 'f' or turn_bet == 'f' or 
                showdown_bet == 'f' or initial_bet == 'f')
      if(not folded):
        if holdem: 
          cardindex = -2
        else:
          cardindex = -7
        
        cards = data[cardindex:]
      else:
        cards = []
      
      handdata = {
        'flop':flop_bet,
        'turn':turn_bet,
        'showdown':showdown_bet,
        'init':initial_bet,
        'money':total_money,
        'bet':total_bet,
        'winnings':winnings,
        'cards':cards
      }

      playerdata[p][ts] = handdata
    player.close()

  return playerdata

def load(path,holdem=True):
  hdbtest = readhdb(path)
  hrostertest = readhroster(path)
  players = set()
  for k,v in hrostertest.items():
    for p in v['roster']:
      players.add(p)
  #pp(players)
  pdbtest = readpdb(path,players,holdem)

  # now we pivo
  
  games = {}
  for k in hdbtest.keys():
    print(k)
    games.setdefault(k,hdbtest[k])
    assert(games[k]['players'] == hrostertest[k]['players'])
    games[k].setdefault('roster',{})
    for p in hrostertest[k]['roster']:
      if k in pdbtest[p].keys():
        games[k]['roster'][p] = pdbtest[p][k]
      
  return games
