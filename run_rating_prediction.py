#!/usr/bin/python
import sys
import getopt
import collections
import os
import re

"""This is a script that runs mymedialite algorithms in 5-fold cross validation
folds.
The input folder is supposed to have the files:
file_name1.train
file_name2.train
file_name3.train
file_name4.train
file_name5.train
and
file_name[1-5].test.
The output uses the following naming conventions:
algorithm_fold1.output
algorithm_fold2.output
algorithm_fold3.output
algorithm_fold4.output
algorithm_fold5.output
"""

#TODO(arthur): adicionar parametros para o user_attributes_file e o
# item_attributes_file

def Usage():
  print '%s' % sys.argv[0]
  print 'Options:'
  print '-a (optional): Algorithms, separated by commas. Default: all.'
  print '-i (required): input folder.'
  print '-f (required): file name'
  print '-o (required): output_folder'
  print 'Example usage:'
  print '%s ' % sys.argv[0]
  quit()

def main():
  try:
    opts, args = getopt.getopt(sys.argv[1:], "a:i:f:o:")
  except getopt.GetoptError, err:
    print str(err)
    Usage()
  algorithms = None
  input_dir = None
  test_dir = None
  file_name = None
  output_dir = None
  algorithms = ['BiPolarSlopeOne', 'FactorWiseMatrixFactorization',
  'GlobalAverage', 'ItemAttributeKNN', 'ItemAverage', 'ItemKNN',
  'MatrixFactorization', 'SlopeOne', 'UserAttributeKNN', 'UserAverage',
  'UserItemBaseline', 'UserKNN', 'TimeAwareBaseline',
  'TimeAwareBaselineWithFrequencies', 'CoClustering',
  'LatentFeatureLogLinearModel', 'BiasedMatrixFactorization', 'SVDPlusPlus',
  'SigmoidSVDPlusPlus', 'SigmoidItemAsymmetricFactorModel',
  'SigmoidUserAsymmetricFactorModel', 'SigmoidCombinedAsymmetricFactorModel']
  for option, value in opts:
    if option == "-h":
      Usage()
    elif option == '-a':
      algorithms = value.split(',')
    elif option == '-i':
      input_dir = value
    elif option == '-f':
      file_name = value
    elif option == '-o':
      output_dir = value
    else:
      assert False, "Option %s not available" % option
  if not input_dir or not file_name or not output_dir:
    Usage()

  for algorithm in algorithms:
    print 'Running for %s' % algorithm
    for i in range(1,6):
      train_file = '%s/%s%d.train' % (input_dir, file_name, i)
      test_file = '%s/%s%d.test' % (input_dir, file_name, i)
      output_file = '%s/%s_fold%d.output' % (output_dir, algorithm, i)
      cmd = ('rating_prediction --training-file=%s --test-file=%s\
 --recommender=%s --prediction-file=%s' %
             (train_file, test_file, algorithm, output_file))
      # TODO(arthur): trocar print pro os.system(cmd) e ver se funciona
      print cmd



if __name__ == '__main__':
  main()
