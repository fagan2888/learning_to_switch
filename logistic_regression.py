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

def Cost(tehta, X, Y, l, cl):

  y = map(IsClass, Y, cl)
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

def addx0feat(X):
  rows = shape(X)[0]
  x0 = ones((rows,1), 'float')
  return concatenate((x0,X),1)

def GD(X,Y):
  i = 1
  derror = sys.maxint
  error = 0
  
  featnum = shape(X)[1]
  w = zeros((featnum+1,1), 'float')

  X_ext = addx0feat(X)
  step = 0.0001
  dthresh = 0.1
  
  while derror>dthresh:
    diff = Y-dot(X_ext, w)

    for j in range(0, shape(X_ext)[1]):
      w[j] = w[j] + step * sum(diff*X_ext[:,j:j+1])
    perror = sum(diff**2)/shape(X)[0]
    derror = abs(error-perror)
    error = perror

  return w


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

def Normalize(X, mean, std):
  for i in range (0, shape(X)[1]):
    X[:,i] = (X[:,i]-mean[i])/std[i]
  return X

def main():
  test_file   = None
  train_file  = None
  X           = None
  Y           = []
  theta       = []
  i           = 0
  alpha       = None
  n           = None
  niter       = 30
  separator   = " "
  try:
    opts, args = getopt.getopt(sys.argv[1:], "t:e:a:n:s:")
  except getopt.GetoptError, err:
    print str(err)
    Usage()
  
  for option, value in opts:
    if option == "-t":
      train_file = value
    elif option == '-e':
      test_file = value
    elif option == '-a':
      alpha = float(value)
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

  #get mean and standart deviation for each vector
  mean_X = X.mean(0)
  std_X = X.std(0)
  X = Normalize(X, mean_X, std_X)
  
  #train for each possible class. When testing, will select the one that fits better.
  for i in range(0, n):
    theta.append(GD(X,Y))
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
