#
# feature detection functions
#

import pickle
import numpy
from pprint import *

ranks=['2','3','4','5','6','7','8','9','T',"J","Q","K","A"]
straights = [ranks[0+i:5+i] for i in range(len(ranks) - 4)]
suits=["s", "c", "h", "d"]

testfile = "./testdata.pick"
f = open(testfile,"rb")
out = pickle.load(f)
f.close()

def handFeatures(hand):
  if str(type(hand)) != "<class 'list'>":
    cards = hand.split(',')
  else:
    cards = hand

  handranks = set([card[0] for card in cards])
  numpairs = 0
  pairstr = ""
  pairarr = []

  if len(handranks) < len(cards):
    pairs = {}
    for pairrank in handranks:
      pairs.setdefault(pairrank,[])

    for card in cards:
      pairs[card[0]].append(card)

    for k,v in pairs.items():
      if len(v) >= 2:
        pairarr.append(str(k)+str(len(v)))

  highcard = ""
  flushs = {}
  for card in cards:
    try:
      cardrank = card[0]
      for rank in ranks[::-1]: # iterate through ranks backwards (highest first)
        if cardrank == rank:
          highcard = card
          break
      flushs.setdefault(card[1],[])
      flushs[card[1]].append(card)
    except IndexError:
      print("wut,",card,rank,cards)
      raise IndexError

  flusharr = []
  for k,v in flushs.items():
    if len(v) > 4:
      flusharr.append("{}{}".format(k,len(v)))

  handsuits = set(map(lambda x: x[1], cards))
  straights = []
  if len(handsuits) < 4: # we can only have a straight if we dont have a suit (or more, also may not)
    handorderedranks = sorted(list(map(lambda x: x[0], cards)))
    straight1 = handorderedranks[0:5]
    straight2 = handorderedranks[1:6]
    straight3 = handorderedranks[2:7]

    # always pick the highest straight
    if straight1 in straights:
      straights.append("s{}{}".format(straight1[0],straight1[4]))
    if straight2 in straights:
      straights.append("s{}{}".format(straight2[0],straight2[4]))
    if straight3 in straights:
      straights.append("s{}{}".format(straight3[0],straight3[4]))

  return pairarr + [highcard] + flusharr + straights


# GENERAL IMAGE FEATUES ****
