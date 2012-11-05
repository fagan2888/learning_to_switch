#!/usr/bin/python
"""
given a dataset in movielens format, generates a 5fold cross-validation
receives as paramenters: i -> input dataset, o-> output_format
"""

from __future__ import division

import sys
import getopt
import math
import random
import os


def FileSize(filename):
  return int(os.popen('wc -l %s' %filename).read().split()[0])

def main():
  try:
    opts, args = getopt.getopt(sys.argv[1:], "i:o:")
  except getopt.GetOptError, err:
    print str(err)
    Usage()
    sys.exit(2)
  in_file = None
  train_file = None 
  test_file  = None 
  for option, value in opts: 
    if option == "-i":
      in_file = value
    elif option == "-o":
      out_file = value
    else: 
      assert False, "Option %s is not avaiable" % option
  if not in_file or not out_file:
    print "Something is missing"
    sys.exit(2)

  in_size = FileSize(in_file)
  test_size = in_size/5
  train_test = test_size*4
  
#read input file and shuffle lines
  data = open(in_file, 'r').readlines()
  random.shuffle(data)
#split the lines in 5 parts:
  folds=[data[x:x+int(test_size)] for x in xrange(0, len(data), int(test_size))]
#for each part, creates a test with it and a train with the other parts
  for i in range(0,5):
    train_file = open("./"+out_file+str(i+1)+"_train", 'w')
    test_file  = open(out_file+str(i+1)+"_test", 'w')
    for line in folds[i]:
      test_file.write(line)
    for j in range (0,5):
      if j!=i:
        for line in folds[j]:
          train_file.write(line)


if __name__ == '__main__':
  main()
