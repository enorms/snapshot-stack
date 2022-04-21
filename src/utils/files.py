"""Get token balance

Download all holders from 
https://etherscan.io/token/0x1bBD79f1Ecb3f2cCC586A5E3A26eE1d1D2E1991f#balances
rename file
check expected format is 
"HolderAddress","Balance","PendingBalanceUpdate"
"0x00d6e10aa6675906fe8eebf7dfb35fe2e7204c98","10373.44","No"
"0x00fcb6f244c45a4e6baa812ddee0bdb7996518bd","10000","No"
"""

import csv


file_path = "./src/data/tokenholders.csv"
wallet = '0x7D25CB84CdfBDAF9A35dF24Be0a854E4D9d96f9d'

wallet_balances = {}

def _load_balances() -> None:
    """load data once for performance

    adjust data types so that 
    tokens are a float
    wallets are lower case"""
    global wallet_balances
    if wallet_balances != {}:
        return wallet_balances
    
    rows = {}
    with open(file_path) as f:
        reader = csv.DictReader(f)
        assert "HolderAddress" in reader.fieldnames
        assert "Balance" in reader.fieldnames
        for row in reader:
            rows.update({row["HolderAddress"].casefold(): float(row["Balance"])})
    wallet_balances = rows


def get_decimal_adjusted_tokens(wallet) -> float:
    """Given a wallet public address
    return tokens, with decimals already taken into account"""
    global wallet_balances
    if wallet_balances == {}:
        _load_balances()

    return wallet_balances.get(wallet)