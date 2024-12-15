import requests
import pandas as pd
import time
import websocket
import json

# Configuration
PUMPFUN_API_URL = 'https://pumpportal.fun/api/data'
DEXSCREENER_URL = 'https://api.dexscreener.com/latest/dex/tokens'
GMGN_URL = 'https://gmgn.ai/api/holders'

API_KEYS = {
    'gmgn': '<your-api-key>'
}

# Fetch data from Pump.fun
def get_pumpfun_data():
    response = requests.get(PUMPFUN_API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        print('Failed to fetch Pump.fun data')
        return []

# Fetch data from Dexscreener with filters
def get_dexscreener_data():
    params = {
        'pair_age': '24h',
        '1h_txns': 150,
        '5m_txns': 25
    }
    response = requests.get(DEXSCREENER_URL, params=params)
    if response.status_code == 200:
        return response.json()['tokens']
    else:
        print('Failed to fetch Dexscreener data')
        return []

# Fetch data from GMG.N.ai
def get_gmgn_data(token_address):
    headers = {
        'Authorization': f"Bearer {API_KEYS['gmgn']}"
    }
    response = requests.get(f"{GMGN_URL}/{token_address}", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Failed to fetch GMG.N data for {token_address}')
        return {}

# Analyze and filter coins
def filter_coins():
    pumpfun_coins = get_pumpfun_data()
    dexscreener_coins = get_dexscreener_data()
    
    filtered_coins = []
    for coin in pumpfun_coins:
        symbol = coin.get('symbol')
        migrated = coin.get('migrated', False)
        if migrated:
            matching_tokens = [token for token in dexscreener_coins if token['symbol'] == symbol]
            if matching_tokens:
                token = matching_tokens[0]
                gmgn_data = get_gmgn_data(token['address'])
                holders = gmgn_data.get('holders', [])
                supply_distribution = gmgn_data.get('supply_distribution', {})
                connected_wallets = gmgn_data.get('connected_wallets', [])
                
                coin_info = {
                    'Name': coin['name'],
                    'Symbol': symbol,
                    'MarketCap': coin.get('market_cap'),
                    'Volume': coin.get('volume'),
                    'Holders': len(holders),
                    'SupplyDistribution': supply_distribution,
                    'ConnectedWallets': connected_wallets
                }
                filtered_coins.append(coin_info)
                time.sleep(1)  # To respect API rate limits
                
    df = pd.DataFrame(filtered_coins)
    df.to_excel('filtered_coins.xlsx', index=False)
    print('Filtered coins saved to filtered_coins.xlsx')

if __name__ == "__main__":
    filter_coins()