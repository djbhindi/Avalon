# Imports
from collections import Counter
from char import Character
import random

# Defaults
RES, SPY = 1,0
ASSASSIN, MORGANA, MORDRED, MERLIN, PERCIVAL = 0,1,2,3,4
APPROVE, SUCCEED = 1, 1
REJECT, FAIL = 0, 0
TO_RUN, SUCCEEDED, FAILED = -1, 1, 0

class Game(object):
  def __init__(self, num_players=7):
    self.missions = [-1]*5
    self.next_mission = 0
    self.n = num_players
    #TODO
    self.votes = 5
    self.roles = self.getRoles(self.n)
    self.names = Character.GetNames(num_players)
    spies, resistance = self.initCharacters(self.names, self.roles)
    # TODO Assign randomly
    self.players = dict(zip(self.names, spies+resistance)) 
   
  def initCharacters(self, names, roles):
    resistance, spies = [], []
    for spy_role in roles['s']:
      spies.append(Character(SPY, spy_role))
    for res_role in roles['r']:
      resistance.append(Character(RES, res_role))
    return resistance, spies

  @staticmethod
  def getRoles(num_players):
    roles = {}
    if num_players == 7:
      roles['s'] = [ASSASSIN, MORGANA, None]
      roles['r'] = [MERLIN, PERCIVAL, None, None]
    else:
      print("Can only do 7 players for now")
    return roles

  def getNumPlayersAndFailsRequired(self):
    mission_count_dict = {
      7: [(2, 1), (3, 1), (4, 1), (3, 1), (4, 1)]
    }
    return mission_count_dict[self.n][self.next_mission] 
 
  # Returns the team proposed.
  # TODO decide whether / how to store previous team propositions for later query.
  def runVote(self, captain_name):
    print("Evaluating mission %d" %  self.next_mission)
    num_players, num_fails = self.getNumPlayersAndFailsRequired()
    print("%s is captain. Please select %d players. This mission fails with %d FAIL votes" % (captain_name, num_players, num_fails))
    team = self.players[captain_name].nominate(num_players, self.names)
    print("Team members proposed: ")
    for member in team:
      print(member)
    
    # Hold vote, conditional on their being remaining votes.
    if self.votes == 0:
      self.votes = 5
      print("Mission forced; can't reject 5 teams in a row")
      return (team, num_fails)

    print("Vote APPROVE or REJECT")

    for player in self.players.values():
      approvals, rejects = 0, 0
      v = player.vote()
      if v == APPROVE:
        approvals += 1
      else:
        rejects += 1
    if approvals > rejects:
      self.votes = 5
      print("Mission was APPROVED. Team is: ")
      for member in team:
        print(member)
    else:
      self.votes -= 1
      print("Mission was REJECTED. Moving to next captin. Remaining votes: %d" % self.votes)
    return team
    
  def runMission(self):
    # TODO start with random captain
    captain = self.names[0]
    team = self.runVote(captain)
    succeeds, fails = 0, 0
    print("TEAM SIZE: %d" % len(team))
    votes = []
    for player in team:
      votes.append(self.players[player].mission())
    c = Counter(votes)
    succeeds, fails = c[SUCCEED], c[FAIL]
    _, fails_required = self.getNumPlayersAndFailsRequired()
    
    if fails < fails_required:
      self.missions[self.next_mission] = SUCCEED
      result_str = "SUCCEEDS"
    else:
      self.missions[self.next_mission] = FAILED
      result_str = "FAILS"
    self.next_mission += 1 
    print("Mission %s with %s success votes and %d fail votes" % (result_str, succeeds, fails))      
 
  # Returns whether the game is over and (if so) whether the Resistance won.
  def gameOver(self):
    succeeded, failed = 0, 0
    for mission in self.missions:
      if mission == FAILED:
        failed += 1
      elif mission == SUCCEEDED:
        succeeded += 1
    return (succeeded == 3 or failed == 3, succeeded == 3)
  
  # Keeps calling runMission until game is over; evaluates assassination if required.
  def runGame(self):
    print("Starting game with %d players." % self.n) 
    while not self.gameOver()[0]:
      self.runMission()
    _, resistance_won = self.gameOver()
    if resistance_won:
      print("RESISTANCE WON by succeeding three missions")
      # Evaluate spy logic
      #TODO fix this garbage code.
      assassin = [x for x in self.players.values() if x.role==ASSASSIN][0]
      target = assassin.assassinate(self.players)
      # TODO populate role / name in printout
      if self.players[target].role==MERLIN:
        print("MERLIN[] was assassinated by the assassin []. SPIES WIN.")
      else:
        print("VANILLA[] was assassinated by the assassin []. RESISTANCE WIN.")
    else:
      print("SPIES WON by failing three missions")
   
    # Print game summary.
    print(self.missions)
    
g = Game(7)
g.runGame()










