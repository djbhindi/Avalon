from django.db import models

class Reporter(models.Model):
    full_name = models.CharField(max_length=70)

    def __str__(self):
        return self.full_name

class Article(models.Model):
    pub_date = models.DateField()
    headline = models.CharField(max_length=200)
    content = models.TextField()
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)

    def __str__(self):
        return self.headline

#TODO make this an internal class.
class Character(models.Model):
    ROLE = (
        (0, 'ASSASSIN'),
        (1, 'MORGANA'),
        (2, 'MORDRED'),
        (3, 'SPY'),
        (4, 'MERLIN'),
        (5, 'PERCIVAL'),
        (6, 'RESISTANCE'),
    )

    role = models.CharField(max_length=1, choices=ROLE)

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
