#!/usr/bin/python
"""Given an dataset in movielens1M/10M format and a percentage X, generates a training and a test file
  for using on MyMediaLite Algorithms, with X percent of the size from the input being used as training
Authors: Arthur Barbosa Camara (camara.arthur@{gmail,dcc.ufmg}.com) 
         Marco Tulio Correia Ribeiro (marcotcr@gmail.com)
"""

# Makes float division the default (instead of integer division)
from __future__ import division

import sys
import getopt
import math
import random
import os

def Usage():
  print "%s" % sys.argv[0]
  print "Options: "
  print "-i (required) ratings file - using MovieLens1M format"
  print "-o (required) output file prefix. Final output is option_train and option_test"
  print "-p (optional) Percentage of the file to be used as training."
  print 'Default is 0.8. This must be a number between 0 and 1'
  print "Example Usage:"
  print "./generate_input.py -i /mnt/hd0/marcotcr/datasets/movielens1M/ratings.dat -o out -p .80"
  sys.exit(2)
def FileSize(fname):
  """
  Counts how many lines there are in a file.
  Returns an integer.
  """
  return int(os.popen('wc -l %s' % fname).read().split()[0])

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
      train_file = value + '_train'
      test_file  = value + '_test'
    elif option == "-p":
      percentage = float(value)
    else:
      assert False, "Option %s is not avaiable" % option
  if not in_file or not train_file or not test_file:
    print "Something is missing"
    Usage()

  #Get the input size
  in_size = FileSize(in_file)
  test_size = in_size * (1 - percentage)

  train_file = open(train_file, "w")
  test_file  = open(test_file,  "w")

  # Reads the data from the infile
  data = open(in_file, 'r').readlines()

  #Shuffle lines of a file
  random.shuffle(data)
  
  #write the shuffled lines on the output files
  for i , line in enumerate(data):
    if i <= test_size:
      test_file.write(line)
    elif i > test_size:
      train_file.write(line)

if __name__ == "__main__":
  main()
