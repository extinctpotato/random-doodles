import os, sys

files_directory = sys.argv[1]
metadata_file = sys.argv[2]

with open(metadata_file, 'r') as f:
    while (line := f.readline().rstrip()):
        file_path, epoch = line.split('\t')

        full_path = os.path.join(files_directory, file_path)
        file_info = os.stat(full_path)

        os.utime(full_path, times=(file_info.st_atime, int(epoch[1:])))
