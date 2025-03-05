import requests
import time
import datetime
import os
from flask import Flask, jsonify  # Import Flask and jsonify

app = Flask(__name__)  # Initialize Flask app

class TokenAnalyzer:
    def __init__(self):
        self.solscan_api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVhdGVkQXQiOjE3MzIwNDMyMDgyMzYsImVtYWlsIjoibXJvbGl2ZXJwdEBnbWFpbC5jb20iLCJhY3Rpb24iOiJ0b2tlbi1hcGkiLCJhcGlWZXJzaW9uIjoidjIiLCJpYXQiOjE3MzIwNDMyMDh9.UWWlKFfc2To1kmeepReENIWJhvxtU6sdA5FZkrjUsuc'
        self.headers = {
            'token': self.solscan_api_key,
            'accept': 'application/json'
        }
        self.base_url = "https://pro-api.solscan.io/v2.0"
        self.wallet_file_path = os.path.join(os.path.dirname(__file__), "wallet.txt")
        print(f"Wallet file will be created at: {self.wallet_file_path}")  # Debug line

    def get_top_holders(self, token_address: str) -> list:
        """Get top holders across 25 pages"""
        endpoint = f"{self.base_url}/token/holders"
        all_holders = []
        
        for page in range(1, 3):
            params = {
                'address': token_address,
                'page': page,
                'page_size': 40 
            }
            
            try:
                response = requests.get(endpoint, headers=self.headers, params=params)
                response.raise_for_status()
                data = response.json()
                
                if data.get('success') and 'data' in data:
                    holders = [{'address': h['owner']} for h in data['data']['items']]
                    if not holders:  # If page is empty, stop fetching
                        break
                    all_holders.extend(holders)
                else:
                    break
                    
            except Exception as e:
                print(f"Error fetching holders page {page}: {e}")
                break
                
    
        return all_holders

    def get_balance_changes(self, wallet_address: str, token_address: str = None) -> list:
        """Get balance changes for a wallet across multiple pages"""
        endpoint = f"{self.base_url}/account/balance_change"
        all_changes = []
        
        for page in range(1, 5):
            params = {
                'address': wallet_address,
                'page': page,
                'page_size': 40,
                'sort_by': 'block_time',
                'sort_order': 'asc'
            }
            
            if token_address:
                params['token'] = token_address
                
            try:
                response = requests.get(endpoint, headers=self.headers, params=params)
                if response.status_code == 500:
                    print(f"Server error for wallet {wallet_address}, skipping...")
                    return []  # Return empty list instead of breaking
                response.raise_for_status()
                data = response.json()
                
                if data.get('success') and 'data' in data:
                    changes = data['data']
                    if not changes:  # If page is empty, stop fetching
                        break
                    all_changes.extend(changes)
                    
            except Exception as e:
                print(f"Error fetching balance changes page {page} for {wallet_address}: {e}")
                break
                
        
        return all_changes

    def get_token_price_at_time(self, token_address: str, timestamp: int) -> float:
        """Get the token price in USD at a specific timestamp"""
        endpoint = f"{self.base_url}/token/price"
        
        date_str = datetime.datetime.fromtimestamp(timestamp).strftime('%Y%m%d')
        
        params = {
            'address': token_address,
            'time[]': date_str
        }
        
        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get('success') and 'data' in data and data['data']:
                return float(data['data'][0].get('price', 0))
                
        except Exception as e:
            print(f"Error fetching token price: {e}")
            print(f"Token: {token_address}, Date: {date_str}")
            
        return 0

    def get_holder_top_holdings(self, wallet_address: str) -> list:
        """Get the top holdings of a wallet in USD"""
        endpoint = f"{self.base_url}/account/token-accounts"
        params = {
            'address': wallet_address,
            'type': 'token',
            'page_size': 10  # Adjust as needed
        }
        
        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get('success') and 'data' in data:
                holdings = []
                for token_account in data['data']:
                    token_address = token_account['token_address']
                    amount = token_account['amount'] / (10 ** token_account['token_decimals'])  # Adjust for decimals
                    price = self.get_token_price_at_time(token_address, int(time.time()))  # Get current price
                    holdings.append({
                        'token_address': token_address,
                        'amount': amount,
                        'usd_value': amount * price
                    })
                return sorted(holdings, key=lambda x: x['usd_value'], reverse=True)[:5]  # Top 5 holdings
        except Exception as e:
            print(f"Error fetching top holdings for {wallet_address}: {e}")
        
        return []

    def analyze_wallet_profits(self, wallet_address: str, token_address: str):
        """Analyze profits for a wallet's trades and get top holdings"""
        changes = self.get_balance_changes(wallet_address, token_address)
        token_positions = {}
        reported_trades = set()  # Track already reported trades
        profit_wallets = []
        top_holdings = {}  # To store holdings across all wallets

        for change in changes:
            token = change['token_address']
            amount = abs(float(change['amount'])) / (10 ** change['token_decimals'])
            timestamp = change['block_time']
            
            if change['change_type'] == 'inc':  # Buy/Receive
                entry_price = self.get_token_price_at_time(token, timestamp)
                if token not in token_positions:
                    token_positions[token] = {
                        'amount': 0,
                        'entry_price': 0,
                        'entry_time': timestamp
                    }
                
                # Average down entry price
                position = token_positions[token]
                total_cost = (position['amount'] * position['entry_price']) + (amount * entry_price)
                total_amount = position['amount'] + amount
                position['entry_price'] = total_cost / total_amount if total_amount > 0 else 0
                position['amount'] = total_amount
                
            elif change['change_type'] == 'dec':  # Sell/Send
                if token in token_positions:
                    position = token_positions[token]
                    exit_price = self.get_token_price_at_time(token, timestamp)
                    
                    if position['amount'] > 0:
                        profit_percentage = ((exit_price / position['entry_price']) - 1) * 100
                        
                        if profit_percentage >= 500:  # Temporarily lowered for testing (change back to 500 later)
                            # Create a unique key for this trade
                            trade_key = f"{wallet_address}_{token}_{position['entry_time']}"
                            
                            if trade_key not in reported_trades:
                                profit_wallets.append([wallet_address, profit_percentage])
                                trade_time = datetime.datetime.fromtimestamp(timestamp)
                                starting_amount_usd = position['amount'] * position['entry_price']
                                ending_amount_usd = position['amount'] * exit_price
                                
                                trade_info = f"""=== Large Profit Found! ===
Wallet: {wallet_address}
Token: {token}
Entry Time: {datetime.datetime.fromtimestamp(position['entry_time'])}
Exit Time: {trade_time}
Starting Amount (USD): ${starting_amount_usd:.2f}
Ending Amount (USD): ${ending_amount_usd:.2f}
Profit Percentage: {profit_percentage:.2f}%
\n"""
                                try:
                                    with open(self.wallet_file_path, 'a') as f:
                                        f.write(trade_info)
                                except IOError as e:
                                    print(f"Error writing to {self.wallet_file_path}: {e}")
                                    print(f"Trade info that couldn't be written: {trade_info}")
                                
                                reported_trades.add(trade_key)
                    
                    # Update remaining position
                    position['amount'] -= amount
                    if position['amount'] <= 0:
                        del token_positions[token]

        # Get top holdings for the wallet
        wallet_holdings = self.get_holder_top_holdings(wallet_address)
        for holding in wallet_holdings:
            token_address = holding['token_address']
            if token_address in top_holdings:
                top_holdings[token_address] += holding['usd_value']
            else:
                top_holdings[token_address] = holding['usd_value']

        return profit_wallets, top_holdings

@app.route('/analyze', methods=['GET'])  # Create API endpoint
def analyze():
    token_addresses = ['HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC',
                       'EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm', 
                       'DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263', 
                       'CzLSujWBLFsSjncfkh59rUFqvafWcY5tzedWJSuypump', 
                       '9BB6NFEcjBCtnNLFko2FqVQBq8HHM13kCyYcdQbgpump', 
                       '2zMMhcVQEXDtdE6vsFS7S7D5oUodfJHE8vd1gnBouauv', 
                       'EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm',
                       '7GCihgDB8fe6KNjn2MYtkzZcRjQy3t9GHdC8uHYmW2hr', 
                       '8x5VqbHA8D7NkD52uNuS5nnt3PwA8pLD34ymskeSo2Wn']

    all_top_holdings = {}  # To store conglomerated top holdings
    top_5_holders = []

    for token_address in token_addresses:
        analyzer = TokenAnalyzer()
        
        # Get top holders
        holders = analyzer.get_top_holders(token_address)
        print(f"Found {len(holders)} holders")
        
        # Analyze each holder's wallet
        for idx, holder in enumerate(holders[20:]):
            print(f"\nAnalyzing holder {idx + 1}/{len(holders)}: {holder['address']}")
            profits, holdings = analyzer.analyze_wallet_profits(holder['address'], token_address)
            largest_profit = 0
            for profit in profits:
                largest_profit = max(profit[1], largest_profit)
            top_5_holders.append((holder['address'], largest_profit))  # Store address and profit
            
            # Conglomerate holdings
            for token_address, usd_value in holdings.items():
                if token_address in all_top_holdings:
                    all_top_holdings[token_address] += usd_value
                else:
                    all_top_holdings[token_address] = usd_value

    # Get top 10 holdings across all analyzed wallets
    top_10_holdings = sorted(all_top_holdings.items(), key=lambda x: x[1], reverse=True)[:10]

    return jsonify({
        'top_10_holdings': top_10_holdings,
        'top_5_gainers': top_5_holders
    })

if __name__ == "__main__":
    app.run(debug=True)  # Run the Flask app
