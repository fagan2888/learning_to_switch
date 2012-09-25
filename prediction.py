#!/usr/bin/env ipy
import sys
import clr

u = int(sys.argv[1])
i = int(sys.argv[2])

clr.AddReference("MyMediaLite.dll")
from MyMediaLite import *

#training data
train_data = IO.RatingData.Read("ml-100k/u1.base")
#test data
test_data  = IO.RatingData.Read("ml-100k/u1.test")

#set up the recommender
recommender = RatingPrediction.UserItemBaseline()
recommender.Ratings = train_data

#faz o treinamento
recommender.Train()

#Medidas de precisão/erro da predissão
print Eval.Ratings.Evaluate(recommender, test_data)

#prever item i para usuário u
print recommender.Predict(u,i)
