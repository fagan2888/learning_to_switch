#!/usr/bin/python
""" This script runs linear regression, Given a training and a test file with features 
for each item in each line.
It will predict wether the rating of a given movie should be 1, 2, 3, 4 or 5 stars.
It will use the One-vs-all technic, calculating predictions for each of the 5 classes above,
finding the one with highest probability, in order do predict correctly.

Author: Arthur Barbosa Câmara (camara.arthur@{gmail.com, dcc.ufmg.br})
"""

import sys
import getopt
import os
import collections
import re

from numpy import *
from numpy import e as npe


def Usage():
  print "%s" %sys.argv[0]
  print "Options:"
  print "-t (required) train file"
  print "-e (required) test file"
  print "-a (required) parameter alpha for gradient descent"
  print "-n (required) Number of possible classes"
  sys.exit(2)

def Sigmoid(theta, x):
  return 1/(1+power(npe, ((-1) * (theta.T*x))

def GradientDescent(n, alpha, X, Y, cl):
  """
  Finds theta parameters so we can find the best thetas as parameters for the regression
  """
  partial = 0
  theta = array([])
  for i in range (1, n):
    for j in range(1, size(Y)):
      if Y[j] == cl:
        y = 1
      else
        y = 0
      partial += (Sigmoid(theta,X[j]) - y) * X[j]
    theta = theta - alpha * (1/m)*partial
  return theta


def main():
  test_file   = None
  train_file  = None
  X           = None
  Y           = array([])
  theta       = []
  i           = 0
  alpha       = None
  n           = None
  niter       = 30
  try:
    opts, args = getopt.getopt(sys.argv[1:], "t:e:a:n:")
  except getopt.GetoptError, err:
    print str(err)
    Usage()
  
  #read the train file
  test_file = open(test_file, "r")
  for line in test_file:
    linep = line.split('')
    #The last argument of a list is the actual result. So, it must be inserted at y.
    append(Y,linep.pop())
    if i == 0:
      #make the list into an numpy-formatted array
      X = array(linep)
      i = 1
    else:
      X = vstack((X, array(linep)))
      
  #train for each possible class. When testing, will select the one that fits better.
  for i in range (1, n):
    theta[i] = GradientDescent(niter, alpha, X, Y, i)

