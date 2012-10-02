#!/usr/bin/python
"""This script is built for converting Netflix Awards Database into the same format used for movielens1M.
A possible next step would be to run the new, unified file using another script in order to use 5fold validation
"""
import time
import datetime

def correctDate(date):
  "Correct date from Netflix Format (iso) to a timestamp"
  return int(time.mktime(datetime.datetime.strptime(date.strip(), "%Y-%m-%d").timetuple()))

def main():
  oFile = open('out.dat', 'w')
  for i in range (1, 17771):
    print "Running for %dth file" % (i)
    if i<10:
      fName = 'mv_000000%d.txt' % (i)
      print fName
      f = open(fName, 'r')
      f.readline()
      lines = f.readlines()
      for line in lines:
        line = line.split(',')
        #transform the date into a valid timestamp
        date = correctDate(line[2])
        #Transform the netflix format to movielens1M format
        out = '%s::%d::%s::%d\n' % (line[0], i, line[1], date)
        oFile.write(out)
    elif i>=10 and i<100:
      fName = 'mv_00000%d.txt' %(i)
      f = open(fName, 'r')
      f.readline()
      lines = f.readlines()
      for line in lines:
        line = line.split(',')
        data = correctDate(line[2])
        out = '%s::%d::%s::%d\n' % (line[0], i, line[1], date)
        oFile.write(out)
    elif i>=100 and i<1000:
      fName = 'mv_0000%d.txt' %(i)
      f = open(fName, 'r')
      f.readline()
      lines = f.readlines()
      for line in lines:
        line = line.split(',')
        data = correctDate(line[2])
        out = '%s::%d::%s::%d\n' % (line[0], i, line[1], date)
        oFile.write(out)
    elif i>1000 and i<=10000:
      fName = 'mv_000%d.txt' % (i)
      f = open(fName, 'r')
      f.readline()
      lines = f.readlines()
      for line in lines:
        line = line.split(',')
        data = correctDate(line[2])
        out = '%s::%d::%s::%d\n' % (line[0], i, line[1], date)
        oFile.write(out)
    elif i>10000 and i<=100000:
      fName = 'mv_00%d.txt' % (i)
      f = open(fName, 'r')
      f.readline()
      lines = f.readlines()
      for line in lines:
        line = line.split(',')
        date = correctDate(line[2])
        out = '%s::%d::%s::%d\n' % (line[0], i, line[1], date)
        oFile.write(out)
      f.close()

if __name__ == '__main__':
  main()
