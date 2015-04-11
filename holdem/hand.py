
hands = open(path+"/hdb")

for line in hands:
  ourdata = line.split("\t")
  timestamp = ourdata[0]
  dealer = ourdata[1]
  handnum = ourdata[2]
  playnum = ourdata[3]
  numplayers = ourdata[4]
    

