from pydantic import BaseModel

class Voter(BaseModel):
  wallet: str
  tokens: int = -1
  votes: float = -1 # adjust for decimals
  choices: dict = {} # for a particular vote


def calculate_adjusted_votes(voter: Voter, power: int = 2) -> float:
  return voter.votes ** (1 / power)

  
def get_votes_per_choice(voter: Voter) -> dict:
    if type(voter.choices) == dict:
        raise Exception("Cannot handle multi-choice voting yet")

    return {voter.choices: voter.votes}


def get_adjusted_votes_per_choice(voter: Voter) -> dict:
    if type(voter.choices) == dict:
        raise Exception("Cannot handle multi-choice voting yet")

    adjusted_votes = calculate_adjusted_votes(voter)
    return {voter.choices: adjusted_votes}


def calculate_normalized_choices(choices: dict):
    """format is: choices { choice: value, choice: value }
    """
    sum = 0
    for choice, value in choices.items():
        sum += value

    normalized_choices = {}
    for choice, value in choices.items():
        normalized_choices[choice] = value / sum

    return normalized_choices

