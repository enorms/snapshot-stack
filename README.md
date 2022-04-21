# snapshot-stack

Do things with votes including counting unique wallets, and simulating quadratic voting.

based on https://gist.github.com/enxyz/53c1dbc807c69da0aaefcd68f4b3cf17

For JavaScript wallet functions use https://github.com/enxyz/wallet-pals/tree/count-orange
Roughly, take the output of unique wallets, run in wallet-pals to get a map to token balance, paste that here into the wallet_balances variable.


# usage

Adjust `proposal_id` and delete any existing local data files; it will broadly prefer any local data file even if for a different proposal. i.e.
- proposal.json
- votes.json

Helper function to clear: 
```sh
rm src/data/*.json
```


Update $ORANGE token holders stored in `./snapshot/snapshot/data/tokenholders.csv` using csv download from 

```sh
https://etherscan.io/token/0x1bBD79f1Ecb3f2cCC586A5E3A26eE1d1D2E1991f#balances
```
