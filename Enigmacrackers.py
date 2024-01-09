import requests
import time
from web3 import Web3
from dotenv import load_dotenv
from random_words import generate
import bip39  # Make sure to install this library using pip

load_dotenv()

# Check if required environment variables are present and not empty
etherscan_key = os.getenv("ETHERSCAN_KEY")
bscscan_key = os.getenv("BSCSCAN_KEY")
polygonscan_key = os.getenv("POLYGONSCAN_KEY")
arbiscan_key = os.getenv("ARBISCAN_KEY")
optimism_etherscan_key = os.getenv("OPTIMISM_ETHERSCAN_KEY")

if not all([etherscan_key, bscscan_key, polygonscan_key, arbiscan_key, optimism_etherscan_key]):
    print('Please provide valid API keys in the .env file.')
    exit(1)  # Exit the script with an error code

# Function to check if the generated mnemonic phrase is valid
def is_valid_mnemonic(phrase):
    return 12 <= len(phrase.split(' ')) <= 24

# Function to generate a valid random mnemonic phrase using bip39
def generate_valid_random_words():
    random_words = bip39.generateMnemonic(strength=256)  # 256 bits for increased entropy
    while not is_valid_mnemonic(random_words):
        random_words = bip39.generateMnemonic(strength=256)
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

        # Add similar calls for other networks if needed

        if any(float(wallet_info['balance']) > 0, float(bnb_wallet_info['balance']) > 0,
               float(matic_wallet_info['balance']) > 0, float(arbitrum_wallet_info['balance']) > 0,
               float(avalanche_wallet_info['balance']) > 0):
            print('Wallet with balance found!')
            print('Address:', check_wallet.address)
            print('Private Key:', check_wallet.privateKey)
            print('ETH Balance:', wallet_info['balance'])
            print('BNB Balance:', bnb_wallet_info['balance'])
            print('MATIC Balance:', matic_wallet_info['balance'])
            print('Arbitrum Balance:', arbitrum_wallet_info['balance'])
            print('Avalanche Balance:', avalanche_wallet_info['balance'])
            exit()

        # Write wallet information to a file
        write_to_file({
            'address': check_wallet.address,
            'privateKey': check_wallet.privateKey,
            'eth': wallet_info,
            'bnb': bnb_wallet_info,
            'matic': matic_wallet_info,
            'arbitrum': arbitrum_wallet_info,
            'avalanche': avalanche_wallet_info,
            'mnemonic': random_words
        })

        # Introduce a delay before the next iteration
        delay(1000)

    except Exception as error:
        print(f'Your program encountered an error: {error}')

# Function to write data to a file
def write_to_file(data):
    eth_balance = f'{data["eth"]["balance"]} ETH' if data.get('eth') else '0.0 ETH'
    bnb_balance = f'{data["bnb"]["balance"]} BNB' if data.get('bnb') else '0.0 BNB'
    matic_balance = f'{data["matic"]["balance"]} MATIC' if data.get('matic') else '0.0 MATIC'
    arbitrum_balance = f'{data["arbitrum"]["balance"]} ETH' if data.get('arbitrum') else '0.0 ETH'
    avalanche_balance = f'{data["avalanche"]["balance"]} AVAX' if data.get('avalanche') else '0.0 AVAX'

    balance_info = ' || '.join([eth_balance, bnb_balance, matic_balance, arbitrum_balance, avalanche_balance])

    with open('results.txt', 'a', encoding='utf-8') as file:
        file.write(f'{data["address"]} || {data["mnemonic"]} || {balance_info}\n')

if __name__ == "__main__":
    main()
