# -*- coding: utf-8 -*-
import random
"""
Created on Sat Apr 11 18:18:16 2015

@author: rhung
"""

def build_deck():
    rank=['2','3','4','5','6','7','8','9','T',"J","Q","K","A"]
    suit=["s", "c", "h", "d"]
    deck=[]
    for i in range (len(rank)):
        for j in range(len(suit)):
            deck.append(rank[i]+suit[j])
    return deck
    
def deal_hands(n): #n=number of players
    deck=build_deck()    
    p1=set(random.sample(deck,2))
    p2=set(random.sample(deck,2))
    return (deck,p1,p2)

def play_game(numPlayer=2):
    (deck,p1,p2)=deal_hands()
    communitycards=[]
    communitycards+=random.sampe(deck,3) #flop
    communitycards+=random.sampe(deck,1) #turn
    communitycards+=random.sampe(deck,3) #river
    p1.add(communitycards)
    p2.add(communitycards)
    s1=determine_score(p1)
    s2=determine_score(p2)
    return s1, s2
    
def determine_scores(hand):
    
    