# !/usr/bin/python3
import os, sys, csv, hashlib
from multiprocessing import Pool, cpu_count
from hashlib import md5

BLOCKSIZE = 65536
n_jobs = 3
path = ""
worksheet = []
file_count = 0

if len(sys.argv) != 2:
    print("Usage: You should provide one argument, path to be scanned")
    exit(1)

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
   with open(filename, 'a') as csvFile:
      writer = csv.writer(csvFile)
      writer.writerow(data)

   csvFile.close()

def sheet_builder():
    for root, dirs, files in os.walk(path, topdown = True):
      for idx, name in enumerate(files):
          record = str(idx), " "+os.path.join(root, name)
          worksheet.append(record)

    return  worksheet



def worker(path):

   #Getting the index and path concatenated and split them to obtain path alone
   cnt = ''.join(path)
   token = cnt.split()
   path = token[1]

   record = token[0], path, md5(path)
   write_to_csv("result.csv", record)


##Build the worksheet to be used
worksheet = sheet_builder()

if __name__ == '__main__':
    n_proc = cpu_count()
    with Pool(n_proc) as p:
        print(p.map(worker, worksheet))
