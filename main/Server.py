import os
from os import listdir
from os.path import isfile, join
from pathlib import Path


data_folder = Path("files")

# Returns a list of files inside the "files" directory
def listFiles():
    print("Getting files in: " + str(data_folder))
    files = [f for f in listdir(str(data_folder)) if isfile(join(str(data_folder), f))]
    return files


print(listFiles())
