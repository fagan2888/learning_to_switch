#!/usr/bin/python

def main():
  data = open("users.dat", "r")
  outfile = open("usersok.dat", "w")

  for line in data:
    linep = line.rstrip("\n")
    linep = line.split("::")
    if linep[1] == "M":
      gender = 11
    else:
      gender = 12
    uid = int(linep[0])
    age = int(linep[2])
    job = int(linep[3]) + 100

    out = "%d %d\n%d %d\n%d %d\n" % (uid, gender, uid, age, uid, job)
    outfile.write(out)

if __name__ == "__main__":
  main()
