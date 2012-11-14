#!/usr/bin/python
import sys
import random


in_file = open(sys.argv[1], "r")

test_file = open("test", "w")
train_file = open("train", "w")

data = in_file.readlines()
random.shuffle(data)

size = len(data)

for i in range(1, size):
  if i <= size*0.2:
    test_file.write(data[i])
  else:
    train_file.write(data[i])
