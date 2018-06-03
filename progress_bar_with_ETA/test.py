from main import iterate_with_ETA_output as wrapper
import sys


def count():
    i = 0
    while True:
        if i > 10**9:
            break
        yield i
        i += 1

with open('/Users/oay/tmp.txt', 'w') as f:
    for x in wrapper(count(), total=10**7):
        pass
