import random
from functools import reduce



def getRandomStr(length = 40):
    rst = []
    for i in range(length):
        rst += chr(random.randint(0, 26) % 26 + ord('a'))
    return reduce(lambda x, y: x + y, rst)

def getRandomInt():
    return random.randint(0, 2**31 - 1)

def getRandomLong():
    return random.randint(0, 2**63 - 1)

def crap(prop):
    return random.random() < prop
