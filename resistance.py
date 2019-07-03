# Imports
from collections import Counter
from char import Character
import random

# Defaults
RES, SPY = 1,0
ASSASSIN, MORGANA, MORDRED, MERLIN, PERCIVAL = 0,1,2,3,4
APPROVE, REJECT = 1, 0

class Result(Enum):
  SUCCEEDED = 0
  FAILED = 1
  TBD = 2

class Mission(object):
  def __init__(self, team_size, fails_required = 1):
    self.team_size = team_size
    self.fails_required = fails_required
    self.result = Result.TBD

  def evaluate(votes):
    num_fails = votes.count(REJECT)
    if num_fails >= fails_required:
      self.result = Result.SUCCEEDED
    else:
      self.result = Result.FAILED
    print("Mission %s with %d fails", self.result.name, num_fails)

class Game(object):
  def __init__(self, num_players=7):
    # Initialize missions
    self.missions = [Mission(s, f) for s, f in getNumPlayersAndFailsRequired()]
    assert(len(self.missions) == 5)
    self.current_mission = 0
    self.n = num_players
    #TODO
    self.votes_remaining = 5
    self.roles = self.getRoles(self.n)
    self.names = Character.GetNames(num_players)
    spies, resistance = self.initCharacters(self.names, self.roles)
    # TODO Assign randomly
    self.players = dict(zip(self.names, spies+resistance)) 
   
  @staticmethod
  def initCharacters(names, roles):
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

  @staticmethod
  def getNumPlayersAndFailsRequired(num):
    mission_count_dict = {
      7: [(2, 1), (3, 1), (3, 1), (4, 2), (4, 1)]
    }
    return mission_count_dict[num] 
 
  # Returns the team proposed.
  # TODO decide whether / how to store previous team propositions for later query.
  def runVote(self, captain_name):
    print("Evaluating mission %d" %  self.current_mission)
    num_players, num_fails = self.getNumPlayersAndFailsRequired()
    print("%s is captain. Please select %d players. This mission fails with %d FAIL votes" % (captain_name, num_players, num_fails))
    team = self.players[captain_name].nominate(num_players, self.names)
    print("Team members proposed: ")
    for member in team:
      print(member)
    
    # Hold vote, conditional on there being remaining votes.
    if self.votes_remaining == 0:
      self.votes_remaining = 5
      print("Mission forced; can't reject 5 teams in a row")
      return (team, num_fails)

    print("Vote APPROVE or REJECT")

    votes = [p.vote() for p in self.players.values()]
    approvals, rejects = votes.count(APPROVE), votes.count(REJECT)
    
    if approvals > rejects:
      self.votes_remaining = 5
      print("Mission was APPROVED. Team is: ")
      for member in team:
        print(member)
    else:
      self.votes_remaining -= 1
      print("Mission was REJECTED. Moving to next captin."
            "Remaining votes: %d" % self.votes_remaining)
    return team
    
  def runMission(self):
    # TODO start with random captain
    # Get team
    captain = self.names[0]
    # This should be a loop?
    team = self.runVote(captain)

    # Get mission votes (TODO change name?)
    votes = [self.players[player].mission() for player in team]
    self.missions[self.current_mission].evaluate(votes)
    self.current_mission += 1 
 
  # Return 1 if resistance won, 0 if spies won, -1 if game not over
  def gameOver(self):
    results = [m.result for m in self.missions]
    succeeded, failed = results.count(Result.SUCCEEDED), results.count(Result.FAILED)
    assert(succeeded <= 3 and failed <= 3)    
    return Result.SUCCEEDED if succeeded == 3 else (Result.FAILED if failed == 3 else Result.TBD)
  
  # Keeps calling runMission until game is over; evaluates assassination if required.
  def runGame(self):
    print("Starting game with %d players." % self.n) 
    while self.gameOver() == Result.TBD:
      self.runMission()
    if self.gameOver() == Result.SUCCEEDED:
      print("RESISTANCE succeeded three missions.")
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










