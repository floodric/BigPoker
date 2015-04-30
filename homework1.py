# Homework 1
# NOTE: sometimes it is useful for programmers to write "notes" inside their code
#       we do this so we remember things, or other people can read our code and 
#       make sense of it.  

#       To write a note, put a #.  Anything following a # will not be read by the computer

import math

# inputs: none
# outputs: none
# side-effects: print out "Hello World"
def helloWorld():
  # code here
  return 0

# inputs: number num1, number num2
# outputs: some number which is the sum of num1 and num2
# side-effects: none
def add(num1,num2):
  # code here
  return 0

# inputs: two x/y number pairs which represent a point
# outputs: a single number representing the distance between them
# side-effects: none
def distance(x1,y1,x2,y2):
  # code here
  # use abs(x) for absolute value
  # use math.sqrt(x) for the square root
  return 0  

# inputs: numbers representing distance, speed, and time
# outputs: a BOOLEAN (True/False) that says if the car can finish in the given time
# side-effects: none
def isFastEnough(distance,speed,time):
  # code here
  return False

# Here is the testing calls
print "Should print: \"Hello World"
helloWorld()

print "Should print 3"
print add(1,2)
print "Should print 3141569"
print add(3140232,1337)
print "Should print -500"
print add(-1000,500)

print "should print about 16.03"
print distance(8,8,-8,7)
print "should print about 7.28"
print distance(-1,2,-3,5)

print "should print True"
print isFastEnough(1,50,0)
print "should print False"
print isFastEnough(50,1,1)
print "should print True"
print isFastEnough(100,10,10)
print "should print False"
print isFastEnough(5000,50,99)
