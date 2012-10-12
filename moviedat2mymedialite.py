#!/usr/python

def main():
  data = open("movies.dat", "r"
  out = open("moviesok.dat", "w")
  cats = { 'Action': 0, 'Adventure': 1, 'Animation': 2, "Children's": 3, 

  for line in data:
    line = line.rstrip("\n"
    linep = line.split("::")
    genres = linep[2].split("|")
    for genre in genres:
      out.write("%d 


if __name__ == "__main__":
  main()

