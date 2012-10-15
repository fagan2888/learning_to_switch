#!/usr/bin/python
"""Given an dataset in movielens1M/10M format and a X, generates a training and a test file
  for using on MyMediaLite Algorithms, with X percent of the size from the input being used as training
Author: Arthur Barbosa C^amara (camara.arthur@{gmail,dcc.ufmg}.com) 
"""

import sys
import getopt
import math
import random

def Usage():
  print "%s" % sys.argv[0]
  print "Options: "
  print "-i (required) ratings file - using MovieLens1M format"
  print "-o (required) output file prefix. Final output is option_train and option_test"
  print "-p (optional) Percentage of the file to be used as training. Default as 0.8"
  print "Example Usage:"
  print "./generate_input.py -i /mnt/hd0/marcotcr/datasets/movielens1M/ratings.dat -o out -p .80"
  sys.exit(2)
def File_Size(fname):
  """
  Count how many inputs there is in a file
  """
  with open(fname) as f:
    for i, l in enumerate(f):
      pass
  return i+1

def main():
  try: 
    opts, args = getopt.getopt(sys.argv[1:], "i:o:p:")
  except getopt.GetOptError, err:
    print str(err)
    Usage()
    sys.exit(2)
  in_file = None
  train_file = None
  test_file  = None
  percentage = 0.8
  for option, value in opts:
    if option == "-i":
      in_file = value
    elif option == "-o":
      train_file = value+"_train"
      test_file  = value+"_test"
    elif option == "-p":
      percentage = float(value)
    else:
      assert False, "Option %s is not avaiable" % option
  if not  in_file or not train_file or not test_file:
    print "Something is missing"
    Usage()

  #Get the input size
  in_size = File_Size(in_file)
  test_size = in_size*percentage

  train_file = open(train_file, "w")
  test_file  = open(test_file,  "w")

  #Shuffle lines of a file
  with open(in_file, 'r') as source:
    data = [ (random.random(), line) for line in source ]
    data.sort()
  
  i=0
  
  #write the shuffled lines on the output files
  for _,line in data:
    if i <= test_size:
      test_file.write(line)
    elif i > test_size:
      train_file.write(line)
    i = i+1

if __name__ == "__main__":
  main()
