#!/usr/bin/python
"""Given a folder and a list of algorithms to be inspected, generates a CSV file with the data
  one .csv file will be generated per fold.
  Each line will contain the user, movie and a list with every prediction given by an algorithm

Author: Arthur Barbosa Camara (camara.arthur@{gmail.com, dcc.ufmg.br})
"""

import sys
import os
import getopt
import collections
import math

def GetRMSE(algorithm, ratings, predictions):
  """Gives the estimated RMSE for a given algorithm"""
  length = 0
  MSE = 0
  for user in predictions:
    for movie in predictions[user]:
      MSE+= (float(predictions[user][movie][algorithm])-(float(ratings[user][movie])))**2
      length += 1
  return math.sqrt(MSE/length)


def CreateMapping(file_format, algorithms):
  predictions = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(lambda: 0.0)))
  for algorithm in algorithms:
    for i in range (1,6):
      if ((i == 5) and (algorithm == "TimeAwareBaseline" or algorithm == "TimeAwareBaselineWithFrequencies")):
        continue
      in_file = open(file_format + algorithm + "_fold" + str(i) + ".output", 'r')
      for line in in_file:
        linep    = line.split()
        user_id  = linep[0]
        movie_id = linep[1]
        rating   = linep[2]
        predictions[user_id][movie_id][algorithm] = rating
  return predictions


def CreateMappingPerFold(file_format, algorithms, fold):
  predictions = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(lambda: 0.0)))
  for algorithm in algorithms:
    if ((fold == 5) and (algorithm == "TimeAwareBaseline" or algorithm == "TimeAwareBaselineWithFrequencies")):
      continue
    in_file = open(file_format + algorithm + "_fold" + str(fold) + ".output", 'r')
    for line in in_file:
      linep    = line.split()
      user_id  = linep[0]
      movie_id = linep[1]
      rating   = linep[2]
      predictions[user_id][movie_id][algorithm] = rating
  return predictions

def GetRealRatings(test_file_format):
  ratings = collections.defaultdict(lambda: collections.defaultdict(lambda: 0.0))
  test_file = open(test_file_format, 'r')
  for line in test_file:
    linep = line.split("::")
    ratings[linep[0]][linep[1]] = float(linep[2])
  return ratings


def GetRealRatingsPerFold(test_file):
  test_file = open(test_file, 'r')
  ratings = collections.defaultdict(lambda: collections.defaultdict(lambda: 0.0))
  for line in test_file:
    linep = line.split("::")
    ratings[linep[0]][linep[1]] = float(linep[2])
  return ratings

def main():
  try:
    opts, args = getopt.getopt(sys.argv[1:], "i:a:t:r:")
  except getopt.GetoptError, err:
    print (err)
    print "Something is missing"
    sys.exit(2)

  in_folder = None
  train_folder = None
  algorithms  = ['BiPolarSlopeOne', 'FactorWiseMatrixFactorization',
                'GlobalAverage', 'ItemAttributeKNN', 'ItemAverage', 'ItemKNN',
                'MatrixFactorization', 'SlopeOne', 'UserAttributeKNN' , 'UserAverage', 
                'UserItemBaseline', 'UserKNN', 'TimeAwareBaseline', 'TimeAwareBaselineWithFrequencies', 
                'CoClustering', 'LatentFeatureLogLinearModel', 'BiasedMatrixFactorization', 'SVDPlusPlus',
                'SigmoidSVDPlusPlus', 'SigmoidItemAsymmetricFactorModel',
                'SigmoidUserAsymmetricFactorModel']
  for option, value in opts:
    if option == "-a":
      algorithms = value.split(',')
    elif option == "-i":
      in_folder = value
    elif option == "-t":
     train_folder = value
    elif option == "-r":
      ratings_file = value
    else:
      assert False, "option not avaiable"
  if not in_folder or not train_folder:
    print "Lacking input or test folder. Where are the predictions?"
    sys.exit(2)
   
  predictions = {}
  out_file = open("RMSE.csv", 'w')
  for algorithm in algorithms:  
     out_file.write(("%s,")%(algorithm))
  out_file.write('\n')
  for i in range(1,6):
    predictions = CreateMappingPerFold(in_folder, algorithms, i)
    ratings = GetRealRatingsPerFold(("%sr%d.test") % (train_folder, i))
    out_file.write("fold_" + str(i) + ",")
    print         ("fold_" + str(i) + ",")
    for algorithm in algorithms:
      out_file.write(str(GetRMSE(algorithm, ratings, predictions))+",")
    out_file.write('\n')
  #print RMSEs for all folds cobined
  
  predictions = CreateMapping(in_folder, algorithms)
  ratings = GetRealRatings(ratings_file)
  out_file.write("Combined,")
  print         ("Combined,")
  for algorithm in algorithms:
    out_file.write(str(GetRMSE(algorithm, ratings, predictions))+",")
  out_file.write('\n')
  out_file.write('\n')
if __name__ == "__main__":
  main()
