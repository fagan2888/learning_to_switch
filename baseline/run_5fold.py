#!/usr/bin/python

def main():
  for i in range(1,6):
    input_file = "fold%d.output" %(i)
    user_file = "/mnt/hd0/marcotcr/datasets/movielens1M/usersok.dat"
    item_file = "/mnt/hd0/marcotcr/datasets/movielens1M/moviesok.dat"
    train_file = "/mnt/hd0/marcotcr/datasets/movielens1M/5fold/r%d.test" % (i)
    test_file = "/mnt/hd0/marcotcr/datasets/movielens1M/5fold/r%d.test" %(i)
    output = "out1"
    cmd = ("./generate_weka.py -i %s -u %s -t %s -f %s -e %s -o %s") % (input_file, user_file, item_file, train_file, test_file, output)
 
if __name__ == "__main__":
  main()

