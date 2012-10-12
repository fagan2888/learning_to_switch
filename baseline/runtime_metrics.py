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
  print "-i (required) input dataset file"
  print "-o (required) output file" 
  print "Example Usage:"
  print "./runtime_metrics.py -i /mnt/hd0/marcotcr/datasets/movielens1m/ratings.dat -o out.txt"
  sys.exit(2)

def main():
  try: 
    opts, args = getopt.getopt(sys.argv[1:], "i:o:")
  except getopt.GetOptError, err:
    print str(err)
    Usage()
  """ itens_rated_by_user is defined as mapping [user]->number of itens rated by this user
      users_rated_item is defined as mapping [item]->number if user that have rated this item
  """ 
  itens_rated_by_user = dict()
  users_rated_item    = dict()
  in_file             = None
  out_file            = None
  linep               = None
  
  for option, value in opts:
    if option == "-i":
      in_file = value
    elif option == "-o":
      out_file = value
    else:
      assert False, "option %s is not avaiable" % option
  if not in_file or not out_file:
    Usage()
  
  in_file  = open(in_file,  "r")
  out_file = open(out_file, "w")
  
  for line in in_file:
    line = line.rstrip('\n')
    linep = line.split("::")
    linep = map(int, linep)
    if linep[0] in itens_rated_by_user:
      itens_rated_by_user[linep[0]] += 1
    else:
      itens_rated_by_user[linep[0]] = 1;
    if linep[1] in users_rated_item:
      users_rated_item[linep[1]] += 1
    else:
      users_rated_item[linep[1]] = 1   

if __name__ == "__main__":
  main()
