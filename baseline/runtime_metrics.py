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
  print "-a (optional) List of algorithms to be executed as level1-predictos. Default all"
  print "-p (optional) Percentage of the split from the dataset to be used as training. Default 0.80"
  print "-i (required) input dataset file"
  print "-o (required) output file" 
  print "Example Usage:"
  print "./runtime_metrics.py -i /mnt/hd0/marcotcr/datasets/movielens1m/ratings.dat -o out.txt"
  sys.exit(2)

global i = dict()
global u = dict()


def  RuntimeMetrics(filename, i, u):
"""maps i[user] -> Number of itens rated by this user
   maps u[item] -> Number of users that have rated this item 
"""
  in_file = open(filename, "r")
  for line in in_file:
    line = line.rstrip("\n")
    linep = line.split("::")
    linep = map(int, linep)
    if linep[0] in i:
      i[linep[0]] += 1
    else:
      i[linep[0]] = 1
    if linep[1] in u:
      u[linep[1]] += 1
    else:
      u[linep[1]] = 1



def main():
  try: 
    opts, args = getopt.getopt(sys.argv[1:], "i:o:a:p")
  except getopt.GetoptError, err:
    print str(err)
    Usage()
  
  itens_rated_by_user = dict()
  users_rated_item    = dict()
  percentage          = None
  algorithms          = None
  in_file             = None
  out_file            = None
  linep               = None
  
  for option, value in opts:
    if option == "-i":
      in_file = value
    elif option == "-o":
      out_file = value
    elif option == "-a":
      algorithms = value.split(",")
    elif option == "-p":
      percentage = float(value)
    else:
      assert False, "option %s is not avaiable" % option
  if not in_file or not out_file:
    Usage()
  #Defines the Runtime metrics to be used
  RuntimeMetrics (in_file, itens_rated_by_user, users_rated_item)
    

if __name__ == "__main__":
  main()
