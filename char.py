import random

#TODO make this an internal class.
class Character(object):
  @staticmethod
  # Default names
  def GetNames(n=7):
    names = ["Alfred", "Bob", "Charlie", "Dan", "Emily", "Frank", "George", "Hank", "Ian", "Jacob"]
    return names[:n]


  def __init__(self, allegiance, name, role=None):
    self.allegiance = allegiance
    self.name = name
    self.role = role

  def vote(self):
    # Get user input...
    vote = random.randint(0,1)
    # (usually hidden)
    print("VOTING %d" % vote)
    return vote

  def mission(self):
    # Get user input...
    vote = random.randint(0,1)
    # (usually hidden)
    print("CASTING %d" % vote)
    return vote

  @staticmethod
  #TODO implement some picking mechanism
  def nominate(num_players, players):
    return players[:num_players]

  # Assassin should extend class.
  def assassinate(self, players):
    return players.keys()[0]
