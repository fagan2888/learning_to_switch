#!/usr/bin/python

def main():
  data = open("movies.dat", "r") 
  outfile = open("moviesok.dat", "w")
  cats = { 'Action': 0, 'Adventure': 1, 'Animation': 2, "Children's": 3, "Comedy": 4, "Crime": 5, "Documentary": 6,
      "Drama":7, "Fantasy":8, "Film-Noir":9, "Horror": 10, "Musical": 11, "Mystery": 12, "Romance": 13, "Sci-Fi": 14,
      "Thriller": 15, "War": 16, "Western": 18}

  for line in data:
    line = line.rstrip("\n")
    linep = line.split("::")
    linep[0] = int(linep[0])
    genres = linep[2].split("|")
    for genre in genres:
      out = "%d %d\n" % (linep[0], cats[genre])
      outfile.write(out)


if __name__ == "__main__":
  main()

