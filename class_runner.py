#!/usr/bin/python
import featureDetect
import classifier
import parsedata
import geneticOptimize as ga
import sys
from pprint import pprint

c = classifier.naivebayes(featureDetect.handFeatures)
exclusions =[199602, 199806, 200102, 199507, 200008, 199803, 199905, 199707] 
#exclusions = exclusions [:2]
def train(classifier=c):
  print("training classifier, please wait\n")

  trainingData = parsedata.readAllGames(False,exclusions)

  counter = 0
  # lazy iterator since trainingdata can be HUUUUUUUUUGE 
  for k in iter(trainingData):
    counter += 1
    #print(k)
    if len(k.split(',')) != 7:
      continue
    for score in trainingData[k]:
      classifier.train(k,score > 0)
    if counter % 5000 == 0:
      print('.',end='',flush=True)

  print("\n")


con = [[0 for guess in range(10)] for correct in range(10)]
def testClassifier(classifier):
  print("testing classifier with test data, please wait\n")

  maxwin = 0.0
  maxlose = 0.0
  bestwin=""
  bestlose=""

  total = 0
  right = 0
  trainData = parsedata.readAllGames(True,exclusions)
  counter = 0
  for k in iter(trainData):
    guess,prob = classifier.classify(k)
    correct = trainData[k]
    counter += 1
    for game in correct:
      if guess == (game > 0):
        right+=1
        if prob > maxwin:
          maxwin = prob
          bestwin = k
      else:
        if prob > maxlose:
          bestlose = k
          maxlose = prob
      total += 1
      con[guess][game>0] += 1
      con[game>0][guess] += 1

    if counter % 500 == 0: print('.',end="",flush=True)


  #printConfusion(con)
  #pprint(con)
  # printing the prototypical images

  print(right / total, 'accuracy')

def printConfusion(confusion):
  for r in range(len(confusion)):
    rowsum = sum(confusion[r]) # take the sum before we override it  with strings
    for c in range(len(confusion[r])):
      confusion[r][c] = "{0:.2f}".format( confusion[r][c] / rowsum )

  for row in confusion:
    for col in row:
      print(col,end=" | ")
    print(" ")
    for i in range(10): print("----",end=" | ")
    print (" ")

print("load from memory y/n")
toload = input()
if toload == 'y':
  c.loadme('./class.pick')
else:
  train()
testClassifier(c)
if toload != 'y':
  print('save?')
  tosave = input()
  if tosave == 'y':
    c.saveme('./class.pick')
ga.demo(c.classify,7)
