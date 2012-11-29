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
import math

from numpy import *
from numpy import e as npe
from scipy.optimize import fmin_bfgs, fmin, minimize, leastsq

def Usage():
  print "%s" %sys.argv[0]
  print "Options:"
  print "-t (required) train file"
  print "-e (required) test file"
  print "-n (required) Number of possible classes"
  print "-s (optional) Data separator for test and train files. default as space"
  sys.exit(2)


def Sigmoid(x):
  h = 1.0/(1.0+ npe**((-1.0)*x))
  return h


def PreProcessing(X,Y,cl,delta):
  for i in range (size(Y)):
    if abs(X[cl][i]-Y[i]) <= delta:
      Y[i] = 1
    else:
      Y[i] = 0
  return (X, Y)


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
  m = Y.size
  print m
  Y = Y.flatten()
  for i in range(X.shape[0]):
    X[i]=X[i].flatten()
  
  print theta
  print X.dot(theta.T)
  h = Sigmoid(X.dot(theta.T))

  print "h="
  print h
  
  print"PARAMS----------------------------------"
  
  a = (-Y.T.dot(log(h)))
  b = ((1.0 - Y.T).dot(log(1.0-h)))
  if math.isnan(b):
    b = -999999
  print theta
  print a
  print b
  print a-b
  J =  (a-b)/m
  print J
  #J = ((-Y.T.dot(log(h))) - ((1.0 - Y.T).dot(log(1.0-h))))
  print "---------------"
  print J/m
  print "---------------"
  return J/m


def predict(theta, X):
  m, n = X.shape
  p = zeros(shape=(m,1))
  h = Sigmoid(X.dot(theta.T))
  print h
  for i in range (0, h.shape[0]):
    if h[i] >= 0.5:
      h[i] = int(1)
    else:
      h[i] = int(0)

  map(int, h)
  print h
  return h 


def main():
  test_file   = None
  train_file  = None
  X           = None
  Y           = []
  theta       = []
  result      = []
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
  
  X = array(X)
  Y = array(Y)
  m,n = X.shape
  intercept=ones(m)
  X = column_stack((intercept, X))
  print X
  Y.shape=(m,1)
  initial_theta = zeros(n+1)
  print "initial_theta:"
  initial_theta.shape = (n+1,1)
  print initial_theta
  print "Shapes:"
  print initial_theta.shape
  print X.shape
  print Y.shape
  theta = fmin_bfgs(Cost2,initial_theta.T, args = (X,Y))
  print theta
  print predict(theta, X)
  print Y.T[0]
  #train for each possible class. When testing, will select the one that fits better.
  #for i in range(0, n):
    #print "TRAINNED"
    #y = IsClass(Y, i) 
    #t1 = (fmin(decorated_cost, initial_theta, args=(y, X)))
    #print t1
    #theta.append(t1)
  #for i in range(0,n):
   # print theta[i]
  #Test for every entrance on test file -  get the probability for each trainned model
  test_file = open(test_file, "r")
  i=0
  for line in test_file:
    linep = line.split(separator)
    result.append(int(linep.pop().strip('\n')))
    linep = map(float,linep)
    if i ==0:
      Xt = array(linep)
      i = 1
    else:
      Xt = vstack((Xt, array(linep)))
  result = array(result)
  m,n = Xt.shape
  result.shape=(m,1)
  #prediction time:
  p = predict(theta.T, Xt)
  print "*************************************"
  print p
  print result.T


if __name__ == '__main__':
  main()
