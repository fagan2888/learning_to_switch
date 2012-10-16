#!/usr/bin/python
import sys
import getopt

"""This script generetes the runtime metrics used for the STREAM system on recommender systems.
It calculates the first two metrics propoed by Bao, Bergman and Thompson:
  -Number of itens that u has rated
  -Number of users that have rated i
It must receive the file with the whole dataset in order to create a file with these informations

Author: Arthur Barbosa C^amara (camara.arthur@{gmail.com, dcc.ufmg.br})
"""
def Usage():
  print "%s" %sys.argv[0]
  print "Options:"
  print "-a (optional) List of algorithms to be used as level1-predictors. Default all"
  print "-i (required) input file format. Wil be used as <algorithm>_<input_format>"
  print "-u (optional) user attributes file"
  print "-t (optional) item attributes file"
  print "-f (required) training file"
  print "-e (required) test file"
  print "-o (required) output file" 
  print "Example Usage:"
  print "./runtime_metrics.py -i /mnt/hd0/marcotcr/datasets/movielens1m/ratings.dat -o out.txt"
  sys.exit(2)

global i = dict()
global u = dict()


def  GenerateRM1(filename):
""" Generates a dictionary with the first RunTimeMetric, giving how many itens has been rated by a given user. map[user]->#
"""
  i = dict()
  in_file = open(filename, "r")
  for line in in_file:
    line = line.rstrip("\n")
    linep = line.split("::")
    linep = map(int, linep)
    if linep[0] in i:
      i[linep[0]] += 1
    else:
      i[linep[0]] = 1
  return i
    
    
def GenerateRM2(filename):
"""Generates a dictionary with the second RunTimeMetric, giving how many times a given item has been rated map[item]->#
"""
  u = dict()
  in_file = open(filename, "r")
  for line in in_file:
    line = line.rstrip("\n")
    linep = line.rstrip("\n")
    linep = map(int, linep)
    if linep[1] in u:
      u[linep[1]] += 1
    else:
      u[linep[1]] = 1
  return i

def ListToString(l):
  l = str(l)
  l = l.strip("[")
  l = l.strip("]")
  l = l.replace("', '", ",")
  l = l.strip("'")

  return l

def  GenerateRatings(file_format, algorithms):
  """Generates a dictionary, with tuples as keys that maps[(user_id,movie_id, algorithm)]->rating
    Receives an algorithm list and the file format used for the inputs
  """
  ratings = {}
  for algorithm in algorithms:
    in_file = open(algorithm+ '_' + file_format, 'r')
    for line in in_file:
      linep = line.split(" ")
      ratings[(int(linep[0]), int(linep[1]), algorithm)] = float(linep[2])

def PrintWeka(out_file, algorithms, )




def main():
  try: 
    opts, args = getopt.getopt(sys.argv[1:], "i:a:u:t:f:e:o:")
  except getopt.GetoptError, err:
    print str(err)
    Usage()
  
  itens_rated_by_user = dict()
  users_rated_item    = dict()
  ratings             = {}
  percentage          = '0.80'
  in_file_format      = None
  in_file             = None
  out_file            = None
  out_folder          = None
  test_file           = None 
  train_file          = None
  user_attributes     = None
  item_attributes     = None

  algorithms  = ['BiPolarSlopeOne', 'FactorWiseMatrixFactorization',
  'GlobalAverage', 'ItemAttributeKNN', 'ItemAverage', 'ItemKNN',
  'MatrixFactorization', 'SlopeOne', 'UserAttributeKNN', 'UserAverage',
  'UserItemBaseline', 'UserKNN', 'TimeAwareBaseline',
  'TimeAwareBaselineWithFrequencies', 'CoClustering',
  'LatentFeatureLogLinearModel', 'BiasedMatrixFactorization', 'SVDPlusPlus',
  'SigmoidSVDPlusPlus', 'SigmoidItemAsymmetricFactorModel',
  'SigmoidUserAsymmetricFactorModel', 'SigmoidCombinedAsymmetricFactorModel']

  for option, value in opts:
    if option == "-i":
      in_file_format = value
    elif option == "-a":
      algorithms = value.split(",")
    elif option == "-u":
      user_attributes = value
    elif option =="-t":
      item_attributes = value
    elif option == "-f":
      train_file = value
    elif option == "-e":
      test_file = value
    elif option == "-o":
      out_file = value
    else:
      assert False, "option %s is not avaiable" % option
  if not in_file or not out_file:
    Usage()

  #Defines the Runtime metrics to be used, as dictionaries
  itens_rated_by_user = GenerateRM1(train_file)
  users_rated_item    = GenerateRM2(train_file)

  #generates a tuple-indexed dictionary ratings[(user_id, movie_id, algorithm')] -> rating
  ratings = GenerateRatings(in_file_format, algorithms)

  #generates Weka formatted output file
  

if __name__ == "__main__":
  main()
