def isMagic(s):
  col_sums = [sum(x) for x in zip(s[0], s[1], s[2])]
  row_sums = [sum(x) for x in s]
  return len(set(col_sums)) == 1 and len(set(row_sums)) == 1 and s[0][0]+s[2][2] == s[0][2] + s[2][0]

def toOneD(s):
  return [s[0] + s[1] + s[2]]

def getSquare(string_s):
  list_s = [int(x) for x in string_s.split(' ')]
  return [list_s[:3], list_s[3:6], list_s[6:9]]

def swapAndWeight(s, i, j):
  s[i], s[j] = s[i], s[j]
  return abs(s[i]-s[j])

def findMinMagic(s, seen):
  if isMagic(s):
    return 0
  # Search all possible swaps?
  

  min_possible = 0
  for i in range(9):
    for j in range(9):
      min_possible = findMinMagic(



 
