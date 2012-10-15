#!/usr/bin/python
"""
This script runs MyMediaLite algorithms with a train and a test files
The input files are supposed to have the MovieLens1M/10M format.
One can give a list of algorithms to be executed or run all of the algorithms from MyMediaLite.
In the latter case, or in a case that some algorithms rely on movies or user data, these must be given as well.

author: Arthur Barosa C^Amara (camara.arthur@{gmail.com, dcc.ufmg.br})
"""

import sys
import getopt
import random

def Usage():
  print '%s' % sys.argv[0]
  print 'Options:'
  print '-a (optional): Algorithms, separated by commas. Default: all.'
  print '-t (required): input format. Used for <value>_train and <value>_test'
  print '-o (required): output_folder'
  print '-u (optional): user_attributes_file' 
  print '-t (optional): item_attributes_file'
  print 'Example usage:'
  print './run_level1.py '

