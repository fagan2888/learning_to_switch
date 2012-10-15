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
  print "-a (optional) List of algorithms to be executed as level1-predictors. Default all"
  print "-p (optional) Percentage of the split from the dataset to be used as training. Default 0.80"
  print "-i (required) input dataset file"
  print "-o (required) output file" 
  print "Example Usage:"
  print "./runtime_metrics.py -i /mnt/hd0/marcotcr/datasets/movielens1m/ratings.dat -o out.txt"
  sys.exit(2)

global i = dict()
global u = dict()


def  GenerateRM1(filename):
""" Generates a dictionary with the first RunTimeMetric, itens rated by a given user.
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
"""Generates a dictionary with the second RunTimemetric, how many times a given item has been rated
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

def main():
  try: 
    opts, args = getopt.getopt(sys.argv[1:], "i:o:a:p:f:u:m:")
  except getopt.GetoptError, err:
    print str(err)
    Usage()
  
  itens_rated_by_user = dict()
  users_rated_item    = dict()
  percentage          = '0.80'
  in_file             = None
  out_file            = None
  out_folder          = None
  test_file           = outlvl1_test
  train_file          = outlvl1_train
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
      in_file = value
    elif option == "-o":
      out_file = value
    elif option == "-a":
      algorithms = value.split(",")
    elif option == "-p":
      percentage = value
    elif option == "-f":
      out_folder = value
    elif option == "-u":
      user_attributes = value
    elif options == "-m":
      item_attributes = value
    else:
      assert False, "option %s is not avaiable" % option
  if not in_file or not out_file:
    Usage()
  
  #Split dataset for test and train sets
  cmd = "./generate_input.py -i %s -o outlvl1 -p %s" % (in_file, percentage)
  os.system(cmd)

  #With the dataset splitted as train and test, we can run level 1 predictors and runtime metrics
  #Run level1-predictor engines
    cmd = "./level1_predictors -a %s -t outlvl1 -o %s -i %s -u %s" % (ListToString(algorithms), out_folder, item_attributes, user_attributes)

  #Defines the Runtime metrics to be used, as dictionaries
  itens_rated_by_user = GenerateRM1(in_file)
  users_rated_item    = GenerateRM2(in_file)
  
  #Next step is to generate Weka input file. First, generate each line, with the ratings from every algorithm and the runtimemetrics



if __name__ == "__main__":
  main()
