import random

randomSearch = [
    "food", "cream", "recipe", "mix", "cook", "fresh"
]

# Returns a list of randomly sorted unique numbers that range from 0 upto the length
def randomSortedNumbers(length):
    randomPicks = [x for x in range(length)]
    random.shuffle(randomPicks)
    return randomPicks


# Returns a 'random' string to ask an edamam search for generating 'random' recipes on
# the Dashboard
def getRandomSearch():
    return randomSearch[random.randint(0, len(randomSearch) - 1)]
