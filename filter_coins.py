import requests

def get_filtered_coins(market_cap_min=2_000_000, market_cap_max=10_000_000,
                      movement_max=20, volume_min=8_000_000):
    url = "https://api.dexscreener.com/latest/dex/tokens"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to fetch data: {response.status_code}")
        return []
    
    data = response.json()
    filtered_coins = []

    for token in data.get('pairs', []):
        market_cap = token.get('priceUsd', 0) * token.get('liquidity', 0)
        movement = token.get('priceChange1h', 0)
        volume = token.get('volume24h', 0)
        
        if (market_cap_min <= market_cap <= market_cap_max and
            abs(movement) <= movement_max and
            volume >= volume_min):
            filtered_coins.append({
                'name': token.get('name'),
                'symbol': token.get('symbol'),
                'market_cap': market_cap,
                'movement_1h': movement,
                'volume_24h': volume
            })
    
    return filtered_coins

if __name__ == "__main__":
    coins = get_filtered_coins()
    for coin in coins:
        print(f"{coin['name']} ({coin['symbol']}): Market Cap=${coin['market_cap']}, "
              f"1h Movement={coin['movement_1h']}%, Volume= ${coin['volume_24h']}")