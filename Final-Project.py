import random
import featureDetect
import parsedata
import classifier

def assoc(x, seq):
    for lst in seq:
      if x == lst[0]:
        return lst
    else:
      return -1

def index(seq, x):
    try:
      return seq.index( x )
    except( ValueError ):
      return -1

def build_deck():
    rank=['2','3','4','5','6','7','8','9','T',"J","Q","K","A"]
    suit=["s", "c", "h", "d"]
    deck=[]
    for i in range (len(rank)):
        for j in range(len(suit)):
            deck.append(rank[i]+suit[j])
    return deck

def generate_hand(handSize):
    deck=build_deck()
    hand=[]
    for i in range(len(handSize)):
        print("Please Enter Card %s (e.g. 4s, Th, Ad):" % (i+1))
        card=input()
        while card not in deck:
            print ("Invalid Card, Please Try Again (e.g. 4s, Th, Ad):")
            card=input()
        hand.append(card)
        deck.remove(card)
    return hand,deck
        
#def deal_hands(n): #n=number of players
#    deck=build_deck()    
#    p1=set(random.sample(deck,2))
#    p2=set(random.sample(deck,2))
#    return (deck,p1,p2)

#def play_game(numPlayer=2):
#    (hand,deck)=generate_hand()
#    communitycards=[]
#    communitycards+=random.sampe(deck,3) #flop
#    communitycards+=random.sampe(deck,1) #turn
#    communitycards+=random.sampe(deck,3) #river
#    p1.add(communitycards)
#    p2.add(communitycards)
#    s1=determine_score(p1)
#    s2=determine_score(p2)
#    return s1, s2
      
def generate_all_strategies(handSize=7):
    result=[bin(i)[2:] for i in range(2**handSize)]
    for i in range(len(result)):
        while len(result[i])!=len(bin(2**handSize-1))-2:
            result[i]='0'+result[i]
    return result
    
def xprintsolution(sol,strategies):
    for i in range(len(sol)):
        strat_result=''
        for ele in strategies[i]:
            for chr in ele:
                if chr=='0': strat_result+= 'Throw'
                else: strat_result+='d'
        sol_result=''
        if sol[i]==0: sol_result='c'
        else: sol_result='d' 
        print('if %s: %s' % (strat_result,sol_result ))
#############################################################
################## MAIN FUNCTION ############################
def demo(handSize=7, scorefun):
    # first element of the list of preferences are the people
    hand,deck=generate_hand(handSize)
    domain = [(0,1) for i in range(0,len(hand))]
    print("\n* Genetic Optimization:")
    s= geneticoptimize( domain,hand,deck, scorefun)
    print( "- Solution representation:", s )
    print( "- Solution:")
    print_sol(s)

#############################################################
#############################################################
def print_sol(s):
    
#Takes all random throw combinations created (see line 144),
#player's hand, remaining deck
def calculate_scores(pop,hand,deck,iterations=20, scorefun): 
    scores=[[0,pop[i]] for i in range(len(pop))]#score=(score,candidate sols.)
    for strategy in range(len(pop)):
        score=0
        for i in range(iterations):
            score+=iteration_score(pop[strategy], deck, hand, scorefun) 
            score=score/iterations
        scores[strategy][0]=score
    return scores    
#returns list of throw combinations with associated average scores
    
#Takes a solution strategy, remaining deck, and current hand
def iteration_score(strategy, deck, hand, scorefun):
    for i in range(len(hand)):
        if strategy[i]==1:
            hand[i]=random.sample(deck,1)
            score = scorefun(hand)
        pass#ADD BAYESIAN HERE ON NEW HAND
#Returns a 1-probability of winning given the new hand
    
    
def geneticoptimize(domain,hand,deck,popsize=50,step=1,
                    mutprob=0.5,elite=0.5,maxiter=100, scorefun): #raja
  def sorter(scores):
    if scores == []: 
        return []
    else:
        pivot = scores[0]
        lesser = sorter([x for x in scores[1:] if x < pivot])
        greater = sorter([x for x in scores[1:] if x >= pivot])
        return lesser + [pivot] + greater
        
  def extract_vector(scores):
    return [elements[1] for elements in scores]   
     
  # Mutation Operation
  def mutate(vec):
    i=random.randint(0,len(domain)-1)
    if random.random()<mutprob and vec[i]>domain[i][0]: #raja
      return vec[0:i]+[vec[i]-step]+vec[i+1:] 
    elif vec[i]<domain[i][1]:
      return vec[0:i]+[vec[i]+step]+vec[i+1:]
    else:  #raja
      return vec
  
  # Crossover Operation
  # at a random index i segments of the two vectors r1 and r2 are swapped
  # e.g., r1 = [0,2,4,6,8,10,12,14]
  #       r2 = [1,3,5,7,9,11,13,15]
  # crossover could return
  #           [0,2,4,6,8,11,13,15]
  def crossover(r1,r2):
    i=random.randint(1,len(domain)-2)
    return r1[0:i]+r2[i:]

  # Build the initial population
  pop=[]
  for i in range(popsize):
    vec=[random.randint(domain[i][0],domain[i][1]) 
         for i in range(len(domain))]
    pop.append(vec)
  
  # How many winners from each generation?
  topelite=int(elite*popsize)
  
  # Main loop 
  for i in range(maxiter):
    scores=calculate_scores(pop,hand,deck, scorefun)
    # Start with the pure winners
    scores=sorter(scores)
    ranked=extract_vector(scores)
    pop=ranked[0:topelite]
    
    # Add mutated and crossovered forms of the winners
    while len(pop)<popsize:
      if random.random()<mutprob:
        # Mutation
        c=random.randint(0,topelite)
        pop.append(mutate(ranked[c]))
      else:
        # Crossover
        c1=random.randint(0,topelite)
        c2=random.randint(0,topelite)
        pop.append(crossover(ranked[c1],ranked[c2]))
    
    # Print current best score
    cost, vec = scores[0]
    if(i%10==0): print()
    print( "%6d" % cost,end='',flush=True )
  print()
  return( vec )
  
