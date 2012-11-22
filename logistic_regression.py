#!/usr/bin/python
""" This script runs linear regression, Given a training and a test file with features 
for each item in each line.
It will predict wether the rating of a given movie should be 1, 2, 3, 4 or 5 stars.
It will use the One-vs-all technic, calculating predictions for each of the 5 classes above,
finding the one with highest probability, in order do predict correctly.

Author: Arthur Barbosa Camara (camara.arthur@{gmail.com, dcc.ufmg.br})
"""

import sys
import getopt
import os
import collections
import re

from numpy import *
from numpy import e as npe
from scipy.optimize import fmin_bfgs

def Usage():
  print "%s" %sys.argv[0]
  print "Options:"
  print "-t (required) train file"
  print "-e (required) test file"
  print "-n (required) Number of possible classes"
  print "-s (optional) Data separator for test and train files. default as space"
  sys.exit(2)

def Sigmoid(x):
  return 1/(1+power(npe,((-1)*x)))


def IsClass(Y, n):
  """Look the vector for a given class, in order to discretize it. If Y[i] == n Y[i] = 1.
  """
  for i in range (size(Y)):
    if Y[i] == n:
      Y[i] = 1
    else:
      Y[i] = 0
  return Y

def Cost2(theta, X, Y):
  m,n = X.shape
  h = Sigmoid(X.dot(theta))
  thetaR = theta
  return (1.0/m) * ((-Y.T.dot(log(h))) - ((1 - Y.T).dot(log(1.0-h)))) \
        + (1/(2.0*m)) * (thetaR.T.dot(thetaR))

def Cost(theta, X, Y):
  print "COST"
  print "******************************************"
  h = Sigmoid(X.dot(theta))
  thetaR = theta[1:, 0]
  m, n = X.shape

  J = (1.0 /m) * ((-Y.T.dot(log(h))) - ((1-Y.T).dot(log(1.0-h)))) \
       + (1/(2.0 *m)) * (thetaR.T.dot(thetaR))
  print J
  delta = h-Y
  sumdelta = delta.T.dot(X[:,1])
  grad1 = (1.0/m) * sumdelta
  XR = X[: 1:X.shape[1]]
  sumdelta = delta.T.dot(XR)
  
  grad = (1.0/m) * (sumdelta + thetaR)
  
  out = zeros(shape=(grad.shape[0], grad.shape[1] + 1))
  out[:, 0] = grad1
  out[:, 1:] = grad

  return J.flatten(), out.T.flatten()


def decorated_cost(theta, y, X):
  return Cost2(theta, X, y)


def main():
  test_file   = None
  train_file  = None
  X           = None
  Y           = []
  theta       = []
  i           = 0
  
  try:
    opts, args = getopt.getopt(sys.argv[1:], "t:e:n:s:")
  except getopt.GetoptError, err:
    print str(err)
    Usage()
  
  for option, value in opts:
    if option == "-t":
      train_file = value
    elif option == '-e':
      test_file = value
    elif option == '-n':
      n = int(value)
    elif option == '-s':
      separator = value
    else:
      assert False, "Option %s not avaiable" %option
  if not test_file or not train_file or not n:
    Usage()
  #read the train file
  train_file = open(train_file, "r")
  for line in train_file:
    linep = line.split(separator)
    #The last argument of a list is the actual result. So, it must be inserted at y.
    Y.append(int(linep.pop().strip('\n')))
    linep = map(float, linep)
    if i == 0:
      #make the list into an numpy-formatted array
      X = array(linep)
      i = 1
    else:
      X = vstack((X, array(linep)))
  Y = array(Y)
  m,n = X.shape
  Y.shape=(m,1)
  initial_theta = zeros(shape = (X.shape[1],1))
    
  #def decorated_cost(theta, y):
   # return Cost2(theta, X, y)

  #train for each possible class. When testing, will select the one that fits better.
  for i in range(0, n):
    y = IsClass(Y, i)
    theta.append(fmin_bfgs(decorated_cost, initial_theta, args=(y, X)))
  for i in range(0,n):
    print theta[i]
  #Test for every entrance on test file -  get the probability for each trainned model
  test_file = open(test_file, "r")
  for line in test_file:
    for i in range(0, n):
      linep = line.split(separator)
      result = int(linep.pop())
      linep = map(float,linep)
      



if __name__ == '__main__':
  main()
