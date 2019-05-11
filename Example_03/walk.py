# !/usr/bin/python3
import os, sys, csv, hashlib
from multiprocessing import Pool
from hashlib import md5

BLOCKSIZE = 65536
n_jobs = 3

if  os.path.isdir(sys.argv[1]):
    path = sys.argv[1]
else:
    print("Usage: Please enter a valid file path to be used for scanning!")
    exit(1)


def md5(filename):
   hasher = hashlib.md5()
   with open(filename, 'rb') as afile:
      buf = afile.read(BLOCKSIZE)
      while len(buf) > 0:
         hasher.update(buf)
         buf = afile.read(BLOCKSIZE)

   return hasher.hexdigest()

def write_to_csv(filename, data):
   with open(filename, 'w') as csvFile:
      writer = csv.writer(csvFile)
      writer.writerows(data)

   csvFile.close()


def exec(path):
   csv_data = []

   for root, dirs, files in os.walk(path, topdown = True):
      for idx, name in enumerate(files):
         record = idx, os.path.join(root, name), md5(os.path.join(root, name))
         csv_data.append(record)

   write_to_csv("result.csv", csv_data)
   #print(csv_data)


#exec(path)

if __name__ == '__main__':
    with Pool(n_jobs) as p:
        print(p.map(exec, [path]))
