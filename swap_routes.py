import requests

# Define the router endpoint
GMGN_ROUTER_URL = 'https://gmgn.ai/defi/router/v1/sol/tx/get_swap_route'

def get_swap_route(input_token, output_token, amount, from_address, slippage):
    params = {
        'token_in_address': input_token,
        'token_out_address': output_token,
        'in_amount': amount,
        'from_address': from_address,
        'slippage': slippage
    }
    
    try:
        response = requests.get(GMGN_ROUTER_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching swap route: {e}")
        return None

# Example usage
if __name__ == "__main__":
    input_token = 'TOKEN_IN_ADDRESS'
    output_token = 'TOKEN_OUT_ADDRESS'
    amount = '1000'  # Amount in smallest unit, e.g., lamports for SOL
    from_address = 'YOUR_WALLET_ADDRESS'
    slippage = '0.5'  # 0.5% slippage
    
    swap_route = get_swap_route(input_token, output_token, amount, from_address, slippage)
    
    if swap_route:
        print("Swap Route:", swap_route)