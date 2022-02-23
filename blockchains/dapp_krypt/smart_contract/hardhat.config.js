// plugin for smart-contract testing
require('@nomiclabs/hardhat-waffle');

module.exports = {
  solidity: '0.8.0',
  networks: {
    ropsten: {
      url: 'https://eth-ropsten.alchemyapi.io/v2/SUsi4BnrzcY8ZB2cHrG9PEz_38KYlfKQ',
      accounts: ['5a9167ba2483308f1d6faa62d42555416e5030b40d4608057559c3c7df531c3e']
    }
  }
};

