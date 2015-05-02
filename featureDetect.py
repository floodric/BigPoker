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
  handstraights = []
  #print('possible straight for {}'.format(hand))
  handorderedranks = sorted(list(map(lambda x: x[0], cards)))
  last = 0 # will never have a one
  counter = 0
  lowcard = ""
  highcard = ""
  for s in straights:
    allin= True
    for cr in s:
      if not cr in handorderedranks:
        allin= False
        break
    if allin:
      if lowcard == "":
      
        lowcard = s[0] # keep 'longer' straights
      highcard = s[4]

  if lowcard != "":
    handstraights = ["straight{},{}".format(lowcard, highcard)]
  else:
    handstraights = []
  return pairarr + flusharr + handstraights


# GENERAL IMAGE FEATUES ****
