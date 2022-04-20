// Get count of a token in wallets

const fs = require('fs');

var ethereum_mainnet_rpc =
  'https://mainnet.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161';
var Web3 = require('web3');
const web3 = new Web3(Web3.givenProvider || ethereum_mainnet_rpc);
const ens = web3.eth.ens;
const erc20AbiJson = require('./interfaces.js');
const wallets = require('./wallets.js');


// $ORANGE
// https://etherscan.io/token/0x1bBD79f1Ecb3f2cCC586A5E3A26eE1d1D2E1991f
const token = '0x1bBD79f1Ecb3f2cCC586A5E3A26eE1d1D2E1991f'
const decimals = 18



async function handleEnsAddresses(wallet) {
  var resolvedAddress = wallet;
  // check for '.' not '.eth' per https://docs.ens.domains/dapp-developer-guide/resolving-names
  if (wallet.includes('.')) {
    resolvedAddress = await ens.getAddress(wallet);
  }
  return resolvedAddress
}

// Given a token address and a list of wallets...
// return a map of token address to count of token
async function getTokenQuantity(wallets, token) {
  const contract = new web3.eth.Contract(erc20AbiJson, token);
  const tokensInWallets = new Map();
  wallets.forEach(async (wallet) => {
    const resolvedAddress = await handleEnsAddresses(wallet);
    const tokenBalance = await contract.methods.balanceOf(resolvedAddress).call();
    tokensInWallets.set(wallet, tokenBalance);
  });
  return tokensInWallets;
}

function saveToFile(toSave) {
  const filePath = "./tokens.json"
  const jsonContent = JSON.stringify(tokens);
  fs.writeFile(filePath, jsonContent, 'utf8', function (err) {
      if (err) {
          return console.log(err);
      }
  })
}

async function main() {
  const tokens = await getTokenQuantity(wallets, token);
  const jsonContent = JSON.stringify(tokens);
  console.log("tokens")
  console.log(tokens)
  console.log("jsonContent")
  console.log(jsonContent)
}

main();
