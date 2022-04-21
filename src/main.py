# Functions and methods to understand snapshot voting.
# Designed for use with 1 (governance) token
# 
# For exploring quadratic voting, 
# each Proposal has many voters
# each voter has one amount of votes
# each voter has many choices
#
# https://docs.snapshot.org/graphql-api
#
# 
# Note: tokens means the raw value, if decimals are applied that will be noted
# 

import requests
from collections import OrderedDict
from pprint import pprint
import pandas as pd
import proposal
import voter as voter_module


# OIP-37 - Four Test Events PULP 001: "0xa81c75b847e5038bcb61963f4871cc36cbf58d9e416990c212d18a31a1e19614"
#  S1 Governance Committee Candidates: "0xed66018cf282c555c0868558e14454f7edf4d4030cb999244e0c7efb151a579b"
# S1 Treasury: 0xd9afc0617e1a898f71f92a88f9e07c82e9d26ec27ef8fd54c706bd8e6999a368
# S1 Dev: 0x29f555de38faf2cc815d9d32d95904b1c5da1be1ee1a2c7ed8f4ad2628c2e594
power = 3
proposal_id = "0x29f555de38faf2cc815d9d32d95904b1c5da1be1ee1a2c7ed8f4ad2628c2e594"
address = '0x1bBD79f1Ecb3f2cCC586A5E3A26eE1d1D2E1991f'
decimals = 18  # etherscan csv download already accounts for this


def get_unique_voters() -> set:
  """
  get all unique voters forever
  """
  URL = "https://hub.snapshot.org/graphql?operationName=Votes&query=query%20Votes%20%7B%0A%20%20votes%20(%0A%20%20%20%20first%3A%201000000000%0A%20%20%20%20skip%3A%200%0A%20%20%20%20where%3A%20%7B%0A%20%20%20%20%20%20space%3A%20%22orangedaoxyz.eth%22%0A%20%20%20%20%7D%0A%20%20%20%20orderBy%3A%20%22created%22%2C%0A%20%20%20%20orderDirection%3A%20desc%0A%20%20)%20%7B%0A%20%20%20%20id%0A%20%20%20%20voter%0A%20%20%20%20created%0A%20%20%20%20proposal%20%7B%0A%20%20%20%20%20%20id%0A%20%20%20%20%7D%0A%20%20%20%20choice%0A%20%20%20%20space%20%7B%0A%20%20%20%20%20%20id%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D%0A"

  res = requests.get(URL)
  res = res.json()
  df = pd.DataFrame.from_dict(res)
  df = df['data']
  df = df['votes']
  unique_voters = set()
  for item in df:
    unique_voters.add(item.get('voter'))
  num_unique_voters = len(unique_voters)
  print ({
      'num_unique_voters': num_unique_voters
  })
  return num_unique_voters


def get_wallets(proposal) -> list[str]:
  # #TODO: this may have been superceded by: get_unique_voters()
  """Given a proposal with voting records,
  a list of unique wallets that voted.
  save to file and return"""

  file_path = "./snapshot/data/voters.py"
  wallets = set()
  vote_records: dict = proposal.votes
  # vote: dict
  for vote in vote_records:
    wallet = vote.get('voter')
    wallets.add(wallet)
  with open(file_path, "w+") as file:
    file.write(str(list(wallets)))
  return list(wallets)


def calculate_outcomes(voters: list[voter_module.Voter], proposal: proposal.Proposal) -> ():
  """Given voters and a proposal, return outcome"""
  # sum of votes times choices
  # for each voter, their choice times their votes
  # sum
  # voters track index of option, proposal is a list of title strings
  start, end = 0, len(proposal.choices)
  outcomes = [0 for i in range(start, end)]
  hypothetical_outcomes = [0 for i in range(start, end)]
  for v in voters:
    normalized_choices = voter_module.calculate_normalized_choices(v.choices)
    adjusted_votes = v.votes ** (1 / power)
    for choice, allocation in normalized_choices.items():
      choice_index = int(choice) - 1
      outcomes[int(choice_index)] += v.votes * allocation
      hypothetical_outcomes[int(choice_index)] += adjusted_votes * allocation
  
  return (outcomes, hypothetical_outcomes)



def rank_results(choices, outcomes, hypothetical_outcomes, rounding=True):
  if rounding:
    outcomes_sorted = {choices[i]: round(outcomes[i]) for i in range(0, len(choices))}
    hypothetical_outcomes_sorted = {choices[i]: round(hypothetical_outcomes[i]) for i in range(0, len(choices))}
  else:
    outcomes_sorted = {choices[i]: outcomes[i] for i in range(0, len(choices))}
    hypothetical_outcomes_sorted = {choices[i]: hypothetical_outcomes[i] for i in range(0, len(choices))}

  value_for_key = lambda item: item[1]
  outcomes_sorted = OrderedDict(sorted(outcomes_sorted.items(), key=value_for_key, reverse=True))
  hypothetical_outcomes_sorted = OrderedDict(sorted(hypothetical_outcomes_sorted.items(), key=value_for_key, reverse=True))
  return (outcomes_sorted, hypothetical_outcomes_sorted)


def main():
  quadratic_proposal = proposal.get_proposal(proposal_id)
  voting_wallets = proposal.get_unique_voters(proposal_id)

  voters = []
  for wallet in voting_wallets:
    votes = voter_module.get_token_balance(wallet)
    choices = proposal.get_choices(wallet, quadratic_proposal)
    voter = voter_module.Voter(wallet=wallet, votes=votes, choices=choices)
    voters.append(voter)

  outcomes, hypothetical_outcomes = calculate_outcomes(voters, quadratic_proposal)
  outcomes, hypothetical_outcomes = rank_results(quadratic_proposal.choices, outcomes, hypothetical_outcomes)

  print("title")
  print(quadratic_proposal.title)
  print("outcomes")
  pprint(outcomes)
  pprint("hypothetical_outcomes")
  pprint(hypothetical_outcomes)



if __name__ == "__main__":
  main()