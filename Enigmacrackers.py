import 'dotenv/config';
import { generate } from 'random-words';
import { ethers } from 'ethers';
import axios from 'axios';
import fs from 'fs';
import bip39 from 'bip39'; // Added the bip39 library

// Check if required environment variables are present and not empty
if (!process.env.ETHERSCAN_KEY || !process.env.BSCSCAN_KEY || !process.env.POLYGONSCAN_KEY || !process.env.ARBISCAN_KEY || !process.env.OPTIMISM_ETHERSCAN_KEY) {
  console.error('Please provide valid API keys in the .env file.');
  process.exit(1); // Exit the script with an error code
}

// Function to check if the generated mnemonic phrase is valid
const isValidMnemonic = (phrase) => {
  return (
    phrase.trim().split(' ').length >= 12 &&
    phrase.trim().split(' ').length <= 24
  );
};

// Function to generate a valid random mnemonic phrase using bip39
const generateValidRandomWords = () => {
  let randomWords;
  do {
    randomWords = bip39.generateMnemonic(256); // 256 bits for increased entropy
  } while (!isValidMnemonic(randomWords));
  return randomWords;
};

// Function to get wallet information from the Etherscan API
const getWalletInfo = async (address) => {
  const apiKey = process.env.ETHERSCAN_KEY;
  const apiUrl = `https://api.etherscan.io/api?module=account&action=balance&address=${address}&apikey=${apiKey}`;
  const maxRetries = 3;

  for (let i = 0; i < maxRetries; i++) {
    try {
      const response = await axios.get(apiUrl);
      if (response.data && response.data.result) {
        const balanceWei = response.data.result;

        if (balanceWei !== undefined) {
          const balanceEther = ethers.utils.formatEther(balanceWei);
          return { balance: balanceEther, address };
        } else {
          throw new Error(
            'Failed to retrieve valid wallet balance from Etherscan API.'
          );
        }
      } else {
        throw new Error(
          'Failed to retrieve wallet balance from Etherscan API.'
        );
      }
    } catch (error) {
      console.error(
        `Error retrieving wallet info (retry ${i + 1}): ${error.message}`
      );
      await delay(1000);
    }
  }

  throw new Error(
    `Max retries reached. Unable to retrieve wallet info for address ${address}`
  );
};

// Function to get wallet information from the Bscscan API
const getBnbWalletInfo = async (address) => {
  const apiKey = process.env.BSCSCAN_KEY;
  const apiUrl = `https://api.bscscan.com/api?module=account&action=balance&address=${address}&apikey=${apiKey}`;
  const maxRetries = 3;

  for (let i = 0; i < maxRetries; i++) {
    try {
      const response = await axios.get(apiUrl);
      if (response.data && response.data.result) {
        const balanceWei = response.data.result;

        if (balanceWei !== undefined) {
          const balanceBnb = ethers.utils.formatEther(balanceWei);
          return { balance: balanceBnb, address };
        } else {
          throw new Error(
            'Failed to retrieve valid wallet balance from BscScan API.'
          );
        }
      } else {
        throw new Error('Failed to retrieve wallet balance from BscScan API.');
      }
    } catch (error) {
      console.error(
        `Error retrieving BNB wallet info (retry ${i + 1}): ${error.message}`
      );
      await delay(1000);
    }
  }

  throw new Error(
    `Max retries reached. Unable to retrieve BNB wallet info for address ${address}`
  );
};

// Function to get wallet information from the Polygonscan API
const getMaticWalletInfo = async (address) => {
  const apiKey = process.env.POLYGONSCAN_KEY;
  const apiUrl = `https://api.polygonscan.com/api?module=account&action=balance&address=${address}&apikey=${apiKey}`;
  const maxRetries = 3;

  for (let i = 0; I < maxRetries; i++) {
    try {
      const response = await axios.get(apiUrl);
      if (response.data && response.data.result) {
        const balanceWei = response.data.result;

        if (balanceWei !== undefined) {
          const balanceMatic = ethers.utils.formatEther(balanceWei);
          return { balance: balanceMatic, address };
        } else {
          throw new Error(
            'Failed to retrieve valid wallet balance from PolygonScan API.'
          );
        }
      } else {
        throw new Error(
          'Failed to retrieve wallet balance from PolygonScan API.'
        );
      }
    } catch (error) {
      console.error(
        `Error retrieving MATIC wallet info (retry ${i + 1}): ${error.message}`
      );
      await delay(1000);
    }
  }

  throw new Error(
    `Max retries reached. Unable to retrieve MATIC wallet info for address ${address}`
  );
};

// Function to get wallet information from the Arbiscan API
const getArbitrumWalletInfo = async (address) => {
  const apiKey = process.env.ARBISCAN_KEY;
  const apiUrl = `https://api.arbiscan.io/api?module=account&action=balance&address=${address}&apikey=${apiKey}`;
  const maxRetries = 3;

  for (let i = 0; i < maxRetries; i++) {
    try {
      const response = await axios.get(apiUrl);
      if (response.data && response.data.result) {
        const balanceWei = response.data.result;

        if (balanceWei !== undefined) {
          const balanceArbitrum = ethers.utils.formatEther(balanceWei);
          return { balance: balanceArbitrum, address };
        } else {
          throw new Error(
            'Failed to retrieve valid wallet balance from Arbiscan API.'
          );
        }
      } else {
        throw new Error('Failed to retrieve wallet balance from Arbiscan API.');
      }
    } catch (error) {
      console.error(
        `Error retrieving Arbitrum wallet info (retry ${i + 1}): ${
          error.message
        }`
      );
      await delay(1000);
    }
  }

  throw new Error(
    `Max retries reached. Unable to retrieve Arbitrum wallet info for address ${address}`
  );
};

// Function to get wallet information from the Avax API
const getAvalancheWalletInfo = async (address) => {
  const apiUrl = `https://api.avax.network/ext/bc/C/rpc`;
  const data = {
    jsonrpc: '2.0',
    id: 1,
    method: 'eth_getBalance',
    params: [address, 'latest'],
  };

  const response = await axios.post(apiUrl, data);
  if (response.data && response.data.result) {
    const balanceWei = response.data.result;

    if (balanceWei !== undefined) {
      const balanceAvax = ethers.utils.formatEther(balanceWei);
      return
