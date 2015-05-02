import math
from pprint import *
import pickle 

smoothing = 0

class classifier:
  def saveme(self,fpath):
    pickfile = open(fpath,"wb")
    pickle.dump((self.cc, self.fc),pickfile)
    pickfile.close()
    
  def loadme(self,fpath):
    pickfile = open(fpath,"rb")
    cc, fc = pickle.load(pickfile)
    self.cc = cc
    self.fc = fc
    pickfile.close()
  
  def __init__(self,getFeatures):
    self.getFeatures=getFeatures
    self.cc = {} # categories examples saw
    self.fc = {} # feature with c category

  def incfc(self, f, cat):
    self.fc.setdefault(f, {})
    self.fc[f].setdefault(cat, 0)
    self.fc[f][cat] += 1

  def incc(self, cat):
    self.cc.setdefault(cat,0)
    self.cc[cat] += 1

  def fcount(self, f, cat):
    if f in self.fc and cat in self.fc[f]:
      return float(self.fc[f][cat])
    return 0.0

  # number matches for cat
  def catcount(self, cat):
    if cat in self.cc:
      return float(self.cc[cat])
    return 0

  def totalcount(self):
    return sum(self.cc.values())

  def categories(self):
    return self.cc.keys()

  def train(self, item, label):
    features = self.getFeatures(item)
    #print(features)
    
    for pixel in features:
      self.incfc(pixel, label)
      # increment for category
    self.incc(label)

  def fprob(self, f, cat):
    if self.catcount(cat) == 0: return 0
    smoothing = 1000 
    num = self.fcount(f, cat)
    denom = self.catcount(cat)
    return (num + smoothing) / denom

  def weightedprob(self, f, cat, prf, weight = 1.0, ap = 0.5):
    basicprob = prf(f,cat)
    totals = sum( [self.fcount(f,c) for c in self.categories()] )

    bp = ((weight * ap) + (totals * basicprob)) / (weight + totals)
    return bp

class naivebayes(classifier):
    def __init__(self, getFeatures):
      classifier.__init__(self, getFeatures)
      self.thresholds = {}
      
    def prob(self, item, cat):
      features = self.getFeatures(item)

      #p = math.log(self.catcount(cat)/self.totalcount())
      p = 1
      for f in features:
        # tprob = self.weightedprob(f,cat,self.fprob)
        # if tprob == 0: continue
        # p += math.log(tprob)
        p *= self.weightedprob(f, cat, self.fprob)
      return p #* -1
    
    def setthreshold(self, cat, t):
      self.thresholds[cat] = t

    def getthreshold(self,cat):
      if cat in self.thresholds.keys():
        return self.thresholds[cat]
      return 1.0

    def classify(self, item, default = None):
      probs = {}
      maxprob = 0.0

      for cat in self.categories():
        probs[cat] = self.prob(item, cat)
        if(probs[cat] > maxprob):
          maxprob = probs[cat]
          best = cat
          
      for cat in probs:
        if cat == best: continue

        if probs[cat] * self.getthreshold(best) > probs[best]: return default
      
      return best, maxprob # return best,maxprob 
