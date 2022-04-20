from snapshot import voter

def test_calculate_normalized_choices():

  v = voter.Voter(
    wallet = "enx.eth",
    choices = {
          "2": 20,
          "3": 40,
          "5": 40
        }
  )
  assert v.choices.get('2') == 20

  normalized = voter.calculate_normalized_choices(v.choices)
  assert normalized.get('2') == 20 / 100

  v.choices = {
            "2": 100,
            "3": 100,
            "4": 100
          }
  normalized = voter.calculate_normalized_choices(v.choices)
  assert normalized.get('4') == 100 / 300
  assert normalized.get('4') != 100 / 3001


def test_calculate_adjusted_votes():
  v = voter.Voter(
    wallet = "enx.eth",
    votes = 10 ** 2
  )
  assert voter.calculate_adjusted_votes(v, 2) == 10
  assert voter.calculate_adjusted_votes(v, 2) != v.votes



def main():
  test_calculate_normalized_choices()
  test_calculate_adjusted_votes()


if __name__ == "__main__":
  main()