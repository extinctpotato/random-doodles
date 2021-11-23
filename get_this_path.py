import os

# Get the absolute path of the file where this statement is invoked,
# no matter what your current working directory is.
this_path = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

if __name__ == '__main__':
    print(this_path)
