import random

def listToVisual(l):
  for i in range(max(l)+1)[::-1]:
    row = []
    for j in range(len(l)):
      if l[j] > i:
        row.append('*')
      else:
        row.append(' ')
    print(' '.join(row))

def getInput():
    return [5,2,6,3,1,6,2,4,3]

# Get max left and right bounds for each position
# Sum position
def getRainfall(input):
    rainfall = 0
    n = len(input)
    lefts, rights = [], []
    left_max, right_max = 0, 0
    for i in range(n):
      left_max = max(input[i], left_max)
      lefts.append(left_max)
      right_max = max(input[n-1-i], right_max)
      rights = [right_max] + rights

    for i in range(n):
      val = input[i]
      rainfall += max(min(lefts[i], rights[i])-val, 0)

    return rainfall

listToVisual(getInput())
print(getRainfall(getInput()))
