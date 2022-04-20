import json
from typing import Union
import requests
from pydantic import BaseModel
import pandas as pd


votes_for_proposal = '' # TODO: import proposal.json

class Proposal(BaseModel):
  id: str
  choices: Union[dict, dict[str, float], list[str]] = {} # number
  title: str = ''
  voters: list[str] = [''] # unique wallets
  outcome: Union[dict, dict[str, float]] = {} # votes per choice
  hypothetical_outcome: Union[dict, dict[str, float]] = {} # votes per choice


def get_choices(wallet: str, proposal: Proposal) -> list[int]:
    """Return the choices made by a wallet,
    given that wallet and proposal.

    Always return as dict;
    
    TODO: see if more recent votes show up twice"""

    votes = _get_votes(proposal.id)
    for vote in votes:
        if vote.get('voter') == wallet:
            choices = vote.get('choice')
            # TODO: feels like the wrong place to type transform
            if type(choices) == int:
                choices = {choices: 1}
            return choices


def get_unique_voters(proposal_id: str) -> list:
    """Get unique voters using helper funtion to grab source data
    """
    votes = _get_votes(proposal_id)
    wallets = set()
    for vote in votes:
        wallets.add(vote.get('voter'))
    return list(wallets)


def _get_votes(proposal_id: str):
    """"""
    file_path = "./snapshot/data/votes.json"

    # use local file if available
    try:
        res = json.load(open(file_path))
    except Exception as error:
        print(error)
        try:
            URL = f"https://hub.snapshot.org/graphql?query=query%20%7B%0A%20%20votes%20(%0A%20%20%20%20first%3A%201000%0A%20%20%20%20skip%3A%200%0A%20%20%20%20where%3A%20%7B%0A%20%20%20%20%20%20proposal%3A%20%22{proposal_id}%22%0A%20%20%20%20%7D%0A%20%20%20%20orderBy%3A%20%22created%22%2C%0A%20%20%20%20orderDirection%3A%20desc%0A%20%20)%20%7B%0A%20%20%20%20id%0A%20%20%20%20voter%0A%20%20%20%20created%0A%20%20%20%20proposal%20%7B%0A%20%20%20%20%20%20id%0A%20%20%20%20%7D%0A%20%20%20%20choice%0A%20%20%20%20space%20%7B%0A%20%20%20%20%20%20id%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D%0A"
            res = requests.get(URL)
            type(json)
            res = res.json()
            json.dump(res, open(file_path, 'w+'))
        except Exception as error:
            raise Exception(error)

    data: dict = res.get('data')
    votes: list[dict] = data.get('votes')
    return votes


def get_proposal(proposal_id: str) -> Proposal:
    """Given a proposal id, return a complete object.
    
    Load local data or call API if needed."""
    file_path = "./snapshot/data/proposal.json"

    # use local file if available
    try:
        res = json.load(open(file_path))
    except Exception as error:
        print(error)
    if res is None:
        try:
            URL = f"https://hub.snapshot.org/graphql?operationName=Proposal&query=query%20Proposal%20%7B%0A%20%20proposal(id%3A%22{proposal_id}%22)%20%7B%0A%20%20%20%20id%0A%20%20%20%20title%0A%20%20%20%20body%0A%20%20%20%20choices%0A%20%20%20%20start%0A%20%20%20%20end%0A%20%20%20%20snapshot%0A%20%20%20%20state%0A%20%20%20%20author%0A%20%20%20%20space%20%7B%0A%20%20%20%20%20%20id%0A%20%20%20%20%20%20name%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D"
            res = requests.get(URL)
            res = res.json()
            json.dump(res, open(file_path, 'w+'))
        except Exception as error:
            raise Exception(error)

    data = res.get('data')
    proposal = data.get('proposal')
    title = proposal.get('title')
    choices = proposal.get('choices')
    try:
        votes = _get_votes(proposal_id)
    except Exception as error:
        print(error)
        votes=''
    proposal = Proposal(title=title, choices=choices, id=proposal_id, votes=votes)
    return proposal


