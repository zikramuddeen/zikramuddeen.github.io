import os
import requests
from web3 import Web3
import time
import json
import mnemonic

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Check if required environment variables are present and not empty
etherscan_key = os.getenv("ETHERSCAN_KEY")
bscscan_key = os.getenv("BSCSCAN_KEY")
polygonscan_key = os.getenv("POLYGONSCAN_KEY")
arbiscan_key = os.getenv("ARBISCAN_KEY")
optimism_etherscan_key = os.getenv("OPTIMISM_ETHERSCAN_KEY")

if not all([etherscan_key, bscscan_key, polygonscan_key, arbiscan_key, optimism_etherscan_key]):
    print('Please provide valid API keys in the .env file.')
    exit(1)

# Function to check if the generated mnemonic phrase is valid
def is_valid_mnemonic(phrase):
    return len(phrase.strip().split(' ')) >= 12 and len(phrase.strip().split(' ')) <= 24

# Function to generate a valid random mnemonic phrase using bip39
def generate_valid_random_words():
    while True:
        random_words = mnemonic.Mnemonic().make_mnemonic(strength=256)
        if is_valid_mnemonic(random_words):
            return random_words

# Function to get wallet information from the Etherscan API
def get_wallet_info(address, api_key):
    api_url = f'https://api.etherscan.io/api?module=account&action=balance&address={address}&apikey={api_key}'
    max_retries = 3

    for i in range(max_retries):
        try:
            response = requests.get(api_url)
            data = response.json()
            if data.get('result') is not None:
                balance_wei = int(data['result'])
                balance_eth = Web3.fromWei(balance_wei, 'ether')
                return {'balance': balance_eth, 'address': address}
            else:
                raise ValueError('Failed to retrieve valid wallet balance from Etherscan API.')
        except Exception as error:
            print(f'Error retrieving wallet info (retry {i + 1}): {error}')
            time.sleep(1)

    raise ValueError(f'Max retries reached. Unable to retrieve wallet info for address {address}')

# Function to get wallet information from the Bscscan API
def get_bnb_wallet_info(address, api_key):
    api_url = f'https://api.bscscan.com/api?module=account&action=balance&address={address}&apikey={api_key}'
    max_retries = 3

    for i in range(max_retries):
        try:
            response = requests.get(api_url)
            data = response.json()
            if data.get('result') is not None:
                balance_wei = int(data['result'])
                balance_bnb = Web3.fromWei(balance_wei, 'ether')
                return {'balance': balance_bnb, 'address': address}
            else:
                raise ValueError('Failed to retrieve valid wallet balance from BscScan API.')
        except Exception as error:
            print(f'Error retrieving BNB wallet info (retry {i + 1}): {error}')
            time.sleep(1)

    raise ValueError(f'Max retries reached. Unable to retrieve BNB wallet info for address {address}')

# Function to get wallet information from the Polygonscan API
def get_matic_wallet_info(address, api_key):
    api_url = f'https://api.polygonscan.com/api?module=account&action=balance&address={address}&apikey={api_key}'
    max_retries = 3

    for i in range(max_retries):
        try:
            response = requests.get(api_url)
            data = response.json()
            if data.get('result') is not None:
                balance_wei = int(data['result'])
                balance_matic = Web3.fromWei(balance_wei, 'ether')
                return {'balance': balance_matic, 'address': address}
            else:
                raise ValueError('Failed to retrieve valid wallet balance from PolygonScan API.')
        except Exception as error:
            print(f'Error retrieving MATIC wallet info (retry {i + 1}): {error}')
            time.sleep(1)

    raise ValueError(f'Max retries reached. Unable to retrieve MATIC wallet info for address {address}')

# Function to get wallet information from the Arbiscan API
def get_arbitrum_wallet_info(address, api_key):
    api_url = f'https://api.arbiscan.io/api?module=account&action=balance&address={address}&apikey={api_key}'
    max_retries = 3

    for i in range(max_retries):
        try:
            response = requests.get(api_url)
            data = response.json()
            if data.get('result') is not None:
                balance_wei = int(data['result'])
                balance_arbitrum = Web3.fromWei(balance_wei, 'ether')
                return {'balance': balance_arbitrum, 'address': address}
            else:
                raise ValueError('Failed to retrieve valid wallet balance from Arbiscan API.')
        except Exception as error:
            print(f'Error retrieving Arbitrum wallet info (retry {i + 1}): {error}')
            time.sleep(1)

    raise ValueError(f'Max retries reached. Unable to retrieve Arbitrum wallet info for address {address}')

# Function to get wallet information from the Avax API
def get_avalanche_wallet_info(address):
    api_url = 'https://api.avax.network/ext/bc/C/rpc'
    data = {
        'jsonrpc': '2.0',
        'id': 1,
        'method': 'eth_getBalance',
        'params': [address, 'latest'],
    }

    response = requests.post(api_url, json=data)
    data = response.json()
    if data.get('result') is not None:
        balance_wei = int(data['result'], 16)
        balance_avax = Web3.fromWei(balance_wei, 'ether')
        return {'balance': balance_avax, '
                .fromWei(balance_wei, 'ether')
                return {'balance': balance_arbitrum, 'address': address}
            else:
                raise ValueError('Failed to retrieve valid wallet balance from Arbiscan API.')
        except Exception as error:
            print(f'Error retrieving Arbitrum wallet info (retry {i + 1}): {error}')
            time.sleep(1)

    raise ValueError(f'Max retries reached. Unable to retrieve Arbitrum wallet info for address {address}')

# Function to get wallet information from the Avax API
def get_avalanche_wallet_info(address):
    api_url = 'https://api.avax.network/ext/bc/C/rpc'
    data = {
        'jsonrpc': '2.0',
        'id': 1,
        'method': 'eth_getBalance',
        'params': [address, 'latest'],
    }

    response = requests.post(api_url, json=data)
    data = response.json()
    if data.get('result') is not None:
        balance_wei = int(data['result'], 16)
        balance_avax = Web3.fromWei(balance_wei, 'ether')
        return {'balance': balance_avax, 'address': address}
    else:
        raise ValueError('Failed to retrieve valid wallet balance from Avax network.')

# Function to introduce a delay using time.sleep
def delay(ms):
    time.sleep(ms / 1000)

# Main execution block
def main():
    try:
        random_words = generate_valid_random_words()
        check_wallet = Web3.Wallet.from_mnemonic(random_words)

        wallet_info = get_wallet_info(check_wallet.address, etherscan_key)
        print('Wallet Address:', wallet_info['address'])
        print('ETH Wallet Balance:', wallet_info['balance'], 'ETH')

        bnb_wallet_info = get_bnb_wallet_info(check_wallet.address, bscscan_key)
        print('BNB Wallet Balance:', bnb_wallet_info['balance'], 'BNB')

        matic_wallet_info = get_matic_wallet_info(check_wallet.address, polygonscan_key)
        print('MATIC Wallet Balance:', matic_wallet_info['balance'], 'MATIC')

        arbitrum_wallet_info = get_arbitrum_wallet_info(check_wallet.address, arbiscan_key)
        print('Arbitrum Wallet Balance:', arbitrum_wallet_info['balance'], 'ETH')

        avalanche_wallet_info = get_avalanche_wallet_info(check_wallet.address)
        print('Avalanche Wallet Balance:', avalanche_wallet_info['balance'], 'AVAX')

        # Continue with the rest of your code...
    
    except Exception as error:
        print('Your program encountered an error:', error)

if __name__ == "__main__":
    main()


