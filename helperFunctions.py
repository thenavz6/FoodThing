import random

# Returns a list of randomly sorted unique numbers that range from 0 upto the length
def randomSortedNumbers(length):
    randomPicks = [x for x in range(length)]
    random.shuffle(randomPicks)
    return randomPicks
