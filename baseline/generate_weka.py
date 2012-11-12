#!/usr/bin/python
import os
import sys
import getopt
import collections

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
  print "-i (required) input file folder for the algorithm predictions. Wil be used as <value>/<algorithm>.output"
  print "-u (optional) user attributes file"
  print "-t (optional) item attributes file"
  print "-f (required) training file"
  print "-e (required) test file"
  print "-o (required) output file format. Will be used as <output_file><train|test>.arff" 
  print "Example Usage:"
  print "./runtime_metrics.py -i /mnt/hd0/marcotcr/datasets/movielens1m/ratings.dat -o out.txt"
  sys.exit(2)



def GenerateRM1(filename):
  """ Generates a dictionary with the first RunTimeMetric, giving how many itens has been rated by a given user. map[user]->rating
  """
  itens_rated = {}
  in_file = open(filename, "r")
  for line in in_file:
    line = line.rstrip("\n")
    linep = line.split("::")
    linep[0] = int(linep[0])
    linep[1] = int(linep[1])
    linep[2] = float(linep[2])
    if linep[0] in itens_rated:
      itens_rated[linep[0]] += 1
    else:
      itens_rated[linep[0]] = 1
  return itens_rated
    
    
def GenerateRM2(filename):
  """Generates a dictionary with the second RunTimeMetric, giving how many times a given item has been rated map[item]->#
  """
  user_rated = {}
  in_file = open(filename, "r")
  for line in in_file:
    linep = line.rstrip("\n")
    linep = linep.split("::")
    linep[0] = int(linep[0])
    linep[1] = int(linep[1])
    linep[2] = float(linep[2])
    
    if linep[1] in user_rated:
      user_rated[linep[1]] += 1
    else:
      user_rated[linep[1]] = 1
  return user_rated

def GenerateCV(cv_file_format, input_file):
  """Generates a 5-fold validation set for a file"""
  cmd = ("./generate_cv.py -i %s -o %s") % (input_file, cv_file_format)
  os.system(cmd)

def GenerateTrainingRatings(training_input, algorithms, item_attributes, user_attributes):
  """Given the training file input and the list of algorithms, creates a map[algorithm][user][movie] = rating, with the rating predicted by a algorithm
  """
  cv_file_format = "r"
  out_format = "out"
  
  print "Generating 5fold cross validation file for the trainning set and running algorithms for it"    
#generate 5fold Cross Validation. The same for every algorithm
  GenerateCV(cv_file_format, training_input)
  for algorithm in algorithms:
    for i in range(1,6):
      train_file = cv_file_format+str(i)+"_test"
      test_file  = cv_file_format+str(i)+"_train"
      out_file   = out_format+algorithm+str(i)+".output"
       
      print "Running for algorithm %s" %(algorithm)
      #run algorithms
      if algorithm == "ItemAttributeKNN" or algorithm == "NaiveBayes":
        cmd = ('rating_prediction --training-file=%s --test-file=%s --recommender=%s --prediction-file=%s --item-attributes=%s --file-format=movielens_1m' %
                            (train_file, test_file, algorithm, out_file, item_attributes))
        print cmd
      elif algorithm == "UserAttributeKNN":
        cmd = ('rating_prediction --training-file=%s --test-file=%s --recommender=%s --prediction-file=%s --user-attributes=%s --file-format=movielens_1m' %
               (train_file, test_file, algorithm, out_file, user_attributes, ))
        print cmd
      else:
        cmd = ('rating_prediction --training-file=%s --test-file=%s --recommender=%s --prediction-file=%s --file-format=movielens_1m'%
              (train_file, test_file, algorithm, out_file))
      print cmd
      os.system(cmd)
      print ("Done!")
  ratings = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(lambda:0.0)))
  #After running the algorithms, create the mapping
  for algorithm in algorithms:
    for i in range(1, 6):
      fold_file = open(out_format+algorithm+str(i)+".output", 'r')
      for line in fold_file:
        linep     = line.split()
        user_id   = linep[0]
        movie_id  = linep[1]
        rating    = linep[2]
        ratings[algorithm][int(user_id)][int(movie_id)] = float(rating)

  return ratings
  
def GenerateRatings(file_format, algorithms):
  """Generates a dictionary, such that dict[algorithm][user][movie] = rating
    Receives an algorithm list and the file format used for the inputs
  """
  ratings = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(lambda:0.0)))
  for algorithm in algorithms:
    #open algorithm prediction file
    in_file = open(file_format + algorithm + '.output', 'r')
    for line in in_file:
      linep = line.split()
      ratings[algorithm][int(linep[0])][int(linep[1])] = float(linep[2])
  return ratings

def GetRealRatingsForTraining(train_file):
  """
    Generates a map[user][movie]-> rating with the real ratings, based on the trainning file provided
  """
  ratings = {}
  in_file = open(train_file, "r")
  #Generate the map with the given trainning set
  for line in in_file:
    linep = line.split("::")
    print linep
    ratings[int(linep[0])][int(linep[1])] = float(linep[2])
  return ratings

      # TODO(arthur): Os ratings gerados aqui(e em outros lugares similares) sao strings.
      # Espero que isso nao de problema em outro lugar.
      #Eles so sao usados para impressao, entao, nao acho que teriamos problemas. De qualquer forma, passei para int


def GetRealRatings(train_file):
  """Generates a dictionary, in the format [user_id][movie_id]=rating, giving the actual ratings provided by a user for a item
  """
  ratings = collections.defaultdict(lambda: collections.defaultdict(lambda: 0.0))
  infile = open(train_file, 'r')
  for line in infile:
    # TODO(arthur): Nem todos os datasets tem esse separador. Um jeito de fazer
    # eh dar o split e ver se o length deu certo. Se tiver dado errado, tenta
    # outro separador.
    
    # Um problema que isso pode gerar eh que, no arquivo padrao do MovieLens, tem mais um campo, que eh um timestamp. 
    #Acho que seria mais util criar um script que converte algum outro formato no do MovieLens.
    linep = line.split("::")
    user_id = int(linep[0])
    movie_id = int(linep[1])
    rating = float(linep[2])
    if user_id not in ratings:
      ratings[user_id] = {}
    if movie_id not in ratings[user_id]:
      ratings[user_id][movie_id] = rating
  return ratings

def PrintWeka(out_file, algorithms, predictions, ratings, metric1, metric2):
  weka_file = open(out_file, 'w')
  weka_file.write("@relation ratingPredictionForMovies\n")
  weka_file.write("@attribute id string\n")
  weka_file.write("@attribute metric1 numeric\n")
  weka_file.write("@attribute metric2 numeric\n")
  for algorithm in algorithms:
    weka_file.write(("@attribute %s_algorithm numeric\n") % (algorithm))
  weka_file.write("@attribute class numeric\n")
  weka_file.write("@data\n\n")
  for user in ratings:
    for movie in ratings[user]:
      if user not in metric1:
        metric1[user] = 0
      if movie not in metric2:
        metric2[movie] = 0
      line = ''
      line += '%s_%s,' % (str(user), str(movie))
      line += '%s,'    %str(metric1[user])
      line += '%s,'    %str(metric2[movie])
      for algorithm in algorithms:
        line += str(predictions[algorithm][int(user)][int(movie)])+','
      line += str(ratings[user][movie]) + '\n'
      weka_file.write(line)
  weka_file.close()
  
def PrintWekaTest(out_file, algorithms, predictions, ratings, metric1, metric2):
  weka_file = open(out_file, 'w')
  weka_file.write("@relation ratingPredictionForMovies\n")
  weka_file.write("@attribute id string\n")
  weka_file.write("@attribute metric1 numeric\n")
  weka_file.write("@attribute metric2 numeric\n")
  for algorithm in algorithms:
    weka_file.write(("@attribute %s_algorithm numeric\n") % (algorithm))
  weka_file.write("@attribute class numeric\n")
  weka_file.write("@data\n\n") 
  seen = {}
  for algorithm in algorithms:
    for user in predictions[algorithm]:
      if user not in seen:
        seen[user] = {}
      for movie in predictions[algorithm][user]:
        if movie in seen[user]:
          continue
        line = ''
        line += '%s_%s,' %(user, movie)
        if user not in metric1:
          metric1[user] = 0
        if movie not in metric2:
          metric2[movie] = 0
        line += '%s,'    %str(metric1[user])
        line += '%s,'    %str(metric2[movie])
        for algorithm in algorithms:
          if movie not in predictions[algorithm][user]:
            predictions[algorithm][user] = "?"
          line += str(predictions[algorithm][user][movie])+','
        if movie not in ratings[user]:
          line += '0\n'
        else:
          if float(rating[user][movie]) > 4:
            line+="1\n"
          else:
            line+"0\n"
        weka_file.write(line)
        seen[user][movie] = 1
  weka_file.close()

def main():
  try: 
    opts, args = getopt.getopt(sys.argv[1:], "i:a:u:t:f:e:o:")
  except getopt.GetoptError, err:
    print str(err)
    Usage()
  
  itens_rated_by_user = {}
  users_rated_item    = {}
  ratings             = {}
  cv_ratings          = {}
  predictions         = {}
  in_file_folder      = None
  in_file             = None
  out_file_format     = None
  out_folder          = None
  test_file           = None 
  train_file          = None
  user_attributes     = None
  item_attributes     = None

  algorithms = ['BiPolarSlopeOne', 'FactorWiseMatrixFactorization',
  'GlobalAverage', 'ItemAttributeKNN', 'ItemAverage', 'ItemKNN',
  'MatrixFactorization', 'SlopeOne', 'UserAttributeKNN', 'UserAverage',
  'UserItemBaseline', 'UserKNN', 'TimeAwareBaseline',
  'TimeAwareBaselineWithFrequencies', 'CoClustering',
  'LatentFeatureLogLinearModel', 'BiasedMatrixFactorization', 'SVDPlusPlus',
  'SigmoidSVDPlusPlus', 'SigmoidItemAsymmetricFactorModel',
  'SigmoidUserAsymmetricFactorModel', 'SigmoidCombinedAsymmetricFactorModel']

  for option, value in opts:
    if option == "-a":
      algorithms = value.split(",")
    elif option == "-u":
      user_attributes = value
    elif option =="-t":
      item_attributes = value
    elif option =="-i":
      in_file_folder = value
    elif option == "-f":
      train_file = value
    elif option == "-e":
      test_file = value
    elif option == "-o":
      out_file = value
    else:
      assert False, "option %s is not avaiable" % option
  if not in_file_folder or not out_file or not test_file or not train_file:
    Usage()

  #Defines the Runtime metrics to be used, as dictionaries
  print "Generating the runtime metrics..."
  #itens_rated_by_user = GenerateRM1(train_file)
  #users_rated_item    = GenerateRM2(train_file)
  print "Done!"

  #generates the rating predictions provided by the algorithms for the trainning file
  print  "Generating rating predictions for the trainning file..."
  cv_ratings = GenerateTrainingRatings(train_file, algorithms, item_attributes, user_attributes)
  print "Done!"

  sys.exit(2)
  #generates a dictionary[algorithm][user_id][movie_id] = rating, given the input files from the level-1 predictors
  print "Getting the predictions from level-1 predictors"
  predictions = GenerateRatings(in_file_folder, algorithms)
  print "Done!"
  
  #generates a user's real rating
  print "Getting real ratings"
  ratings = GetRealRatings(test_file)
  print "Done!"

  #generates Weka formatted trainning file
  print "Writing trainning file"
  train_out = "%strain.arff" % (out_file)
  PrintWeka(train_out, algorithms, cv_ratings, ratings, itens_rated_by_user, users_rated_item)
  print "Done!"

  #generates Weka formattd test file
  print "Writing test file"
  test_out = "%stest.arff" % (out_file)
  PrintWekaTest(test_out, algorithms, predictions, ratings, itens_rated_by_user, users_rated_item)
  print "Done!"

if __name__ == "__main__":
  main()
