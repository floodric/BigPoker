# BigPoker
67-362 final project

data comes in the following formats:

HDB format
==========
1        timestamp (supposed to be unique integer)
2        game set # (incremented when column 3 resets)
3        game # reported by dealer bot
4        number of players dealt cards
5        number of players who see the flop
6        pot size at beginning of flop
7        number of players who see the flop
8        pot size at beginning of turn
9        number of players who see the flop
10       pot size at beginning of river
11       number of players who see the flop
12       pot size at showdown
13+      cards on board (0, 3, 4 or 5)

HROSTER format
==============
1        timestamp
2        number of player dealt cards
3+       player nicknames


in file `pdb/pdb.[playername]`
PDB format
==========
1        player nickname
2        timestamp of this hand (see HDB)
3        number of player dealt cards
4        position of player (starting at 1, in order of cards received)
5        betting action preflop (see below)
6        betting action on flop (see below)
7        betting action on turn (see below)
8        betting action on river (see below)
9        player's bankroll at start of hand
10       total action of player during hand
11       amount of pot won by player
12+      pocket cards of player (if revealed at showdown)
