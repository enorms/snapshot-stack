import logging
from test_data import test_wallet_balances
# from snapshot import main
# from snapshot.main import main, calculate_outcomes
import main as main_file
from src import crypto_token
from src import proposal
from src import voter



address = '0x1bBD79f1Ecb3f2cCC586A5E3A26eE1d1D2E1991f'
decimals = 18
def _create_token():
    return crypto_token.CryptoToken(address=address, decimals=decimals)

def _create_proposal():
    proposal_id = "0xed6601...7efb151a579b" # avoid using a real number
    file_path = "./tests/test_data/test_proposal.json"
    test_proposal = proposal.get_proposal(proposal_id, file_path=file_path)
    assert type(test_proposal) == proposal.Proposal
    return test_proposal


def _create_voters(test_proposal: proposal.Proposal):
  """expects decimals"""
  balances: list[dict[str: str, str: int]] = test_wallet_balances.balances

  voters = []
  for item in balances:
    wallet = item.get('wallet') # DEBUG test this
    tokens = item.get('tokenBalance') # DEBUG test this
    votes = int(tokens) / decimals
    choices = proposal.get_choices(wallet, test_proposal)
    new_voter = voter.Voter(wallet=wallet, tokens=tokens, votes=votes, choices=choices)
    voters.append(new_voter)
  return voters


def test_calculate_outcomes(power=2):
    choices = [1,2,3,4,5]
    dividend = (1+2+3+1)
    normalized = [1 / dividend, 2 / dividend, 3 / dividend, 0, 1 / dividend]
    tokens = "117787590000000005505024"
    votes = int(tokens) / decimals
    adjusted_votes = pow(int(votes), 1 / power)
    expected_vote_1 = [votes * i for i in normalized]
    expected_adjusted_vote_1 = [adjusted_votes * i for i in normalized]

    dividend = (1+1+1)
    normalized = [0, 1 / dividend, 2 / dividend, 3 / dividend, 0]
    tokens = "15206360000000000000000"
    votes = int(tokens) / decimals
    adjusted_votes = pow(int(votes), 1 / power)
    expected_vote_2 = [votes * i for i in normalized]
    expected_adjusted_vote_2 = [adjusted_votes * i for i in normalized]

    expected_outcomes = [expected_vote_1[i] + expected_vote_2[i] 
                        for i in range (0,len(choices))]
    expected_hypothetical_outcomes = [expected_adjusted_vote_1[i] + expected_adjusted_vote_2[i] 
                        for i in range (0,len(choices))]

    test_proposal = _create_proposal()
    voters = _create_voters(test_proposal)
    outcomes, hypothetical_outcomes = main_file.calculate_outcomes(voters=voters, proposal=test_proposal)
    assert [expected_outcomes[i] == outcomes[i] for i in range (0,len(choices))]
    assert [expected_hypothetical_outcomes[i] == hypothetical_outcomes[i]
            for i in range (0,len(choices))]


def main():
  test_calculate_outcomes()


if __name__ == "__main__":
  main()