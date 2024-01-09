import os
import random
import requests
import time
import json
from web3 import Web3
from dotenv import load_dotenv
import bip39

load_dotenv()

ETHERSCAN_KEY = os.getenv('ETHERSCAN_KEY')
BSCSCAN_KEY = os.getenv('BSCSCAN_KEY')
POLYGONSCAN_KEY = os.getenv('POLYGONSCAN_KEY')
ARBISCAN_KEY = os.getenv('ARBISCAN_KEY')
OPTIMISM_ETHERSCAN_KEY = os.getenv('OPTIMISM_ETHERSCAN_KEY')

if not ETHERSCAN_KEY or not BSCSCAN_KEY or not POLYGONSCAN_KEY or not ARBISCAN_KEY or not OPTIMISM_ETHERSCAN_KEY:
    print('Please provide valid API keys in the .env file.')
    exit(1)

def is_valid_mnemonic(phrase):
    return len(phrase.strip().split(' ')) >= 12 and len(phrase.strip().split(' ')) <= 24

def generate_valid_random_words():
    random_words = ''
    while not is_valid_mnemonic(random_words):
        random_words = bip39.create_mnemonic(strength=256)
    return random_words

def get_wallet_info(address):
    api_key = ETHERSCAN_KEY
    api_url = f'https://api.etherscan.io/api?module=account&action=balance&address={address}&apikey={api_key}'
    max_retries = 3

    for i in range(max_retries):
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                response_json = json.loads(response.text)
                if response_json and response_json['result']:
                    balance_wei = int(response_json['result'])
                    balance_ether = Web3.fromWei(balance_wei, 'ether')
                    return {'balance': balance_ether, 'address': address}
                else:
                    raise Exception('Failed to retrieve wallet balance from Etherscan API.')
            else:
                raise Exception('Failed to retrieve wallet balance from Etherscan API.')
        except Exception as e:
            print(f'Error retrieving wallet info (retry {i + 1}): {e}')
            time.sleep(1)

    raise Exception(f'Max retries reached. Unable to retrieve wallet info for address {address}')

def get_bnb_wallet_info(address):
    api_key = BSCSCAN_KEY
    api_url = f'https://api.bscscan.com/api?module=account&action=balance&address={address}&apikey={api_key}'
    max_retries = 3

    for i in range(max_retries):
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                response_json = json.loads(response.text)
                if response_json and response_json['result']:
                    balance_wei = int(response_json['result'])
                    balance_bnb = Web3.fromWei(balance_wei, 'ether')
                    return {'balance': balance_bnb, 'address': address}
                else:
                    raise Exception('Failed to retrieve wallet balance from BscScan API.')
            else:
                raise Exception('Failed to retrieve wallet balance from BscScan API.')
        except Exception as e:
            print(f'Error retrieving BNB wallet info (retry {i + 1}): {e}')
            time.sleep(1)

    raise Exception(f'Max retries reached. Unable to retrieve BNB wallet info for address {address}')

def get_matic_wallet_info(address):
    api_key = POLYGONSCAN_KEY
    api_url = f'https://api.polygonscan.com/api?module=account&action=balance&address={address}&apikey={api_key}'
    max_retries = 3

    for i in range(max_retries):
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                response_json = json.loads(response.text)
                if response_json and response_json['result']:
                    balance_wei = int(response_json['result'])
                    balance_matic = Web3.fromWei(balance_wei, 'ether')
                    return {'balance': balance_matic, 'address': address}
                else:
                    raise Exception('Failed to retrieve wallet balance from PolygonScan API.')
            else:
                raise Exception('Failed to retrieve wallet balance from PolygonScan API.')
        except Exception as e:
            print(f'Error retrieving MATIC wallet info (retry {i + 1}): {e}')
            time.sleep(1)

    raise Exception(f'Max retries reached. Unable to retrieve MATIC wallet info for address {address}')

def get_arbitrum_wallet_info(address):
    api_key = ARBISCAN_KEY
    api_url = f'https://api.arbiscan.io/api?module=account&action=balance&address={address}&apikey={api_key}'
    max_retries = 3

    for i in range(max_retries):
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                response_json = json.loads(response.text)
                if response_json and response_json['result']:
                    balance_wei = int(response_json['result'])
                    balance_arbitrum = Web3.fromWei(balance_wei, 'ether')
                    return {'balance': balance_arbitrum, 'address': address}
                else:
                    raise Exception('Failed to retrieve wallet balance from Arbiscan API.')
            else:
                raise Exception('Failed to retrieve wallet balance from Arbiscan API.')
        except Exception as e:
            print(f'Error retrieving Arbitrum wallet info (retry {i + 1}): {e}')
            time.sleep(1)

    raise Exception(f'Max retries reached. Unable to retrieve Arbitrum wallet info for address {address}')
