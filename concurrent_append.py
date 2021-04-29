#
# Shamelessly stolen from the following StackOverflow response:
# https://stackoverflow.com/a/56792928/6150271
#

import time
from concurrent.futures import ProcessPoolExecutor

id_array = [*range(10)]

def myfunc(id):
    time.sleep(5)
    if id % 2 == 0:
        return id, id
    else:
        return id, id ** 2


result = []
with ProcessPoolExecutor() as executor:
    for r in executor.map(myfunc, id_array):
        result.append(r)

print(result)
