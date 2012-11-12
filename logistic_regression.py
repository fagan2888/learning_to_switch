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
  print "-a (required) parameter alpha for gradient descent"
  print "-n (required) Number of possible classes"
  print "-s (optional) Data separator for test and train files. default as space"
  sys.exit(2)

def IsClass(x, cl):
  if x == cl:
    x = 1
  else:
    x = 0
  return x

def Sigmoid(x):
  return 1/(1+power(npe,((-1)*x)))

def map_feature(x1, x2):
  x1.shape = (x1.size,1)
  x2.shape = (x2.size, 1)
  degree = 6
  out = ones(shape=(x1[:,0].size, 1))
  m,n=out.shape
  for i in range(1, degree+1):
    for j in range(i+1):
      r = (x1 ** (i-j)) * (x2 **j)
      out - append(out, r, axis = 1)
  return out

def Cost(theta, X, Y):
   
  h = sigmoid(X.dot(theta))
  thetaR = theta[1:, 0]
  
  J = (1.0 /m) * ((-Y.T.dot(log(h))) - ((1-Y.T).dot(log(1.0-h)))) \
       + (1/(2.0 *m)) * (thetaR.T.dot(thetaR))
  delta = h-y
  sumdelta = delta.T.dot(X[:,1])
  gradl = (1.0/m) * sumdelta

  XR = X[: 1:x.shape[1]]
  sumdelta = delta.T.dot(XR)
  grad = (1.0/m) * (sumdelta + 1 *thetaR)
  
  out = zeros(shape=(grad.shape[0], grad.shape[1] + 1))
  out[:, 0] = gradl
  out[:, 1:] = grad

  return J.flatten(), out.T.flatten()


def GradientDescent(n, alpha, X, Y, cl):
  """
  Finds theta parameters so we can find the best thetas as parameters for the regression
  """
  m = size(Y)
  partial = 0
  
  theta = zeros(size(X[1]+1), 'float')

  for i in range (0, n):
    for j in range(0, size(Y)):
      if Y[j] == cl:
        y = 1
      else:
        y = 0
      partial += (Sigmoid(dot (theta,X[j])) - y) * X[j]
    theta = theta - alpha * (1/m)*partial
  return theta


def main():
  test_file   = None
  train_file  = None
  X           = None
  Y           = []
  theta       = []
  i           = 0
  separator   = " "
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
  if not test_file or not train_file or not alpha or not n:
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
  #feature mapping
  m,n = X.shape
  Y.shape=(m,1)
  it = map_feature(X[:,0], X[:,1])
  initial_theta = zeros(shape = (it.shape[1],1))

  cost, grad = Cost(initial_theta, it, y)
  
  def decorated_cost(theta):
    return Cost(theta, it, y)
  
  #train for each possible class. When testing, will select the one that fits better.
  for i in range(0, n):
    y = map(IsClass, Y, i)
    theta.append(fmin_bfgs(decorated_cost, initial_theta, maxfun=400))
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
