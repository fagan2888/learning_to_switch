#!/usr/bin/python
import sys
import getopt
import collections
import os
import re

"""This is a script that runs MyMediaLite algorithms, relying on a train 
and a test sets.
It expects to receive a list of algorithms to use (by default, all avaiable).
for algorithms that use user-based predictions or item-based predictions,
these must be provided as well.

author: Arthur Barbosa C^amara (camara.arthur@{gmail.com, dcc.ufmg.br})
""" 

def Usage():
  print "%s" % sys.argv[0]
  print "Options:"
  print "-a (optional) Algorithms, comma separated. Default: all"
  print "-t (required) train and test file name. Will be used as <value>_train and <value>_test"
  print "-o (required) output folder"
  print "-i (optional) item_attributes_file (required if using item-based prediction algorithms)"
  print "-u (optional) user_attributes_file (required if using user-based prediction algorithms)"
  print "Example usage:"
  print "./level1_predictors.py/ -t /mnt/hd0/marcotcr/datasets/movielens1M/out -o ./ -i /mnt/hd0/marcotcr/datasets/movies.dat -u /mnt/hd0/marcotcr/datasets/users.dat"
  sys.exit(2)

def main():
  try:
     opts, args = getopt.getopt(sys.argv[1:], "i:o:p:")
  except getopt.GetOptError, err:
    print str(err)
    Usage()
  algorithms      = None
  train_file      = None
  test_file       = None
  output_file     = None
  item_attributes = None
  user_attributes = None
  algorithms      = ['BiPolarSlopeOne', 'FactorWiseMatrixFactorization',
  'GlobalAverage', 'ItemAttributeKNN', 'ItemAverage', 'ItemKNN',
  'MatrixFactorization', 'SlopeOne', 'UserAttributeKNN', 'UserAverage',
  'UserItemBaseline', 'UserKNN', 'TimeAwareBaseline',
  'TimeAwareBaselineWithFrequencies', 'CoClustering',
  'LatentFeatureLogLinearModel', 'BiasedMatrixFactorization', 'SVDPlusPlus',
  'SigmoidSVDPlusPlus', 'SigmoidItemAsymmetricFactorModel',
  'SigmoidUserAsymmetricFactorModel', 'SigmoidCombinedAsymmetricFactorModel']

  for option, value in opts:
    if options == "-h":
      Usage()
    elif options == "-a":
      algorithms = value.split(',')
    elif options == "-t":
      train_file = value+"_train"
      test_file  = value+"_test"
    elif options == "-o":
      output_file = value
    elif options == "-i":
      item_attributes = value
    elif options == "-u":
      user_attributes = value
    else:
      assert False, "Option %s not avaiable" % option
  if not train_file or not output_folder:
    Usage()
  for algorithm in algorithms:
    
    if algorithm == "ItemAttributeKNN" or algorithm == "NaiveBayes":
      cmd = ('rating-prediction --training_file=%s --test_file=%s --recommender=%s --prediction_file=%s item-attributes=%s --file-fomat=movielens_1m' % 
(train_file, test_file, algorithm, output_file, item_attributes))
    elif algoritm == "UserAttributeKNN":
       cmd = ('rating-prediction --training_file=%s --test_file=%s --recommender=%s --prediction_file=%s user-attributes=%s --file-fomat=movielens_1m' % 
(train_file, test_file, algorithm, output_file, user_attributes))
    else:
       cmd = ('rating-prediction --training_file=%s --test_file=%s --recommender=%s --prediction_file=%s --file-fomat=movielens_1m' % 
(train_file, test_file, algorithm, output_file))
    os.system(cmd)


if __name__ == '__main__':
  main()
