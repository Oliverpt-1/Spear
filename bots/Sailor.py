import discord
from discord.ext import commands, tasks
import requests
import datetime
from typing import Dict, List
import os
from dotenv import load_dotenv
import http.server
import socketserver
import asyncio

# Load environment variables
load_dotenv()

class WhaleTracker(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)
        
        # Solscan configuration
        self.solscan_api_key = os.getenv('SOLSCAN_API_KEY')
        self.headers = {
            'token': self.solscan_api_key,
            'accept': 'application/json'
        }
        self.base_url = "https://pro-api.solscan.io/v2.0"
        
        # Discord channel configuration
        channel_ids_str = os.getenv('SAILOR_MAIN_CHANNEL_IDS', '1312524220722450604,1323537633095188520')
        self.DISCORD_CHANNEL_IDS = [int(id.strip()) for id in channel_ids_str.split(',')]
        self.SELL_CHANNEL_ID = int(os.getenv('SAILOR_SELL_CHANNEL_ID', '1313432989769924668'))

    async def setup_hook(self):
        print("🚀 Setup hook called...")
        try:
            self.track_whales.start()
            print("✅ Tracking loop started!")
        except Exception as e:
            print(f"❌ ERROR STARTING TRACKING LOOP: {e}")

    def get_balance_changes(self, wallet_address: str) -> Dict:
        """Get recent balance changes for a wallet"""
        endpoint = f"{self.base_url}/account/balance_change"
        params = {
            'address': wallet_address,
            'page': 1,
            'page_size': 20,
            'sort_by': 'block_time',
            'sort_order': 'desc'
        }
        
        try:
            print(f"Making API call to Solscan for {wallet_address[:8]}...")
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
                
        except Exception as e:
            print(f"API Error: {e}")
            return {"status": "error", "message": str(e)}

    async def send_alert(self, message: str):
        """Send Discord alert"""
        try:
            for channel_id in self.DISCORD_CHANNEL_IDS:  # Loop through all channel IDs
                channel = self.get_channel(channel_id)
                if channel:
                    await channel.send(message)
            else:
                print("Could not find Discord channel")
        except Exception as e:
            print(f"Error sending Discord alert: {e}")

    def get_token_price(self, token_address: str) -> float:
        """Get token price from Solscan"""
        endpoint = f"{self.base_url}/token/price"
        today = datetime.datetime.now().strftime('%Y%m%d')

        params = {
            'address': token_address,
            'time[]': today
        }
        
        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            return data['data'][0]['price']
        except Exception as e:
            print(f"Error getting token price: {e}")
            return 0

    def get_token_name(self, token_address: str) -> str:
        """Get token name from Solscan"""
        endpoint = f"{self.base_url}/token/meta"
        params = {
            'address': token_address
        }

        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()['data']['name']
        except Exception as e:
            print(f"Error getting token name: {e}")
            return "Unknown"


    async def monitor_wallet(self, wallet_address: str, wallet_name: str):
        """Monitor a single wallet for significant changes"""
        try:
            response = self.get_balance_changes(wallet_address)
            
            if response['success'] and 'data' in response:
                transactions = response['data']
                recent_txs = []
                
                for tx in transactions:
                    tx_time = datetime.datetime.fromtimestamp(tx.get('block_time', 0))
                    current_time = datetime.datetime.now()
                    
                    # Check if transaction is from the last 5 minutes
                    if tx_time > current_time - datetime.timedelta(minutes=5):
                        raw_amount = float(tx.get('post_balance')) - float(tx.get('pre_balance'))
                        token_decimals = tx.get('token_decimals', 9)
                        token_address = tx.get('token_address', 'Unknown')
                        token_name = self.get_token_name(token_address)
                        if token_address == 'So11111111111111111111111111111111111111111' or token_address == 'Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB' or token_address == 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v':
                            continue
                        
                        
                        # Get current token price
                        price_usd = self.get_token_price(token_address) if token_address else 0
                        
                        # Calculate actual amount and USD value
                        actual_amount = raw_amount / (10 ** token_decimals)
                        usd_value = actual_amount * price_usd


                        if usd_value > 1000 or usd_value < -1000:
                            recent_txs.append((actual_amount, usd_value, tx_time, token_address, token_name))
                
                if recent_txs:
                    # Sort by USD value, largest first
                    recent_txs.sort(key=lambda x: x[1], reverse=True)
                    
                    for amount, usd_value, tx_time, token_address, name in recent_txs:
                        message = (
                            f"💰 **Transaction Alert** 💰\n"
                            f"**Wallet:** <https://solscan.io/account/{wallet_address}>\n"
                            f"**Wallet Name:** {wallet_name}\n"
                            f"**Token:** <https://solscan.io/token/{token_address}>\n"
                            f"**Token Name:** {name}\n"
                            f"**Amount:** {amount:.4f}\n"
                            f"**USD Value:** ${usd_value:.2f}\n"
                            f"**Time:** {(tx_time - datetime.timedelta(hours=5)).strftime('%Y-%m-%d %H:%M:%S')}"
                        )
                        if usd_value >= 1000:
                            await self.send_alert(message)
                        if usd_value <= -1000:
                            channel = self.get_channel(self.SELL_CHANNEL_ID)
                            if channel:
                                await channel.send(message)
            
        except Exception as e:
            await self.send_alert(f"❌ Error monitoring wallet {wallet_address}: {e}")

    @tasks.loop(minutes=5)
    async def track_whales(self):
        """Check whale wallets every minute"""
        print("🔄 TRACK_WHALES LOOP RUNNING")
        try:
            print(f"\n[{datetime.datetime.now()}] 🔍 Starting wallet check cycle...")

            current_dir = os.path.dirname(os.path.abspath(__file__))
            wallet_file = os.path.join(current_dir, 'wallet.txt')

            with open(wallet_file, 'r') as f:
                whale_addresses = []
                for line in f:
                    name, address = line.strip().split(':', 1)
                    whale_addresses.append((address.strip(),name.strip()))

            for address, name in whale_addresses:
                await self.monitor_wallet(address, name)
                
            print(f"✅ Completed check cycle at {datetime.datetime.now()}\n")
                
        except Exception as e:
            print(f"❌ Error in tracking loop: {e}")

    @track_whales.before_loop
    async def before_tracking(self):
        """Wait until the bot is ready before starting the tracking loop"""
        await self.wait_until_ready()

    @commands.Cog.listener()
    async def on_ready(self):
        print("🤖 BOT IS READY AND CONNECTED TO DISCORD")
        try:
            # Loop through all channel IDs in the list and send the message
            for channel_id in self.DISCORD_CHANNEL_IDS:
                channel = self.get_channel(channel_id)
                if channel:
                    print("all")
                else:
                    print(f"Could not find channel {channel_id}")
        except Exception as e:
            print(f"Error sending ready message: {e}")

def start_server():
    PORT = int(os.getenv('PORT', 10000))
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()

def main():
    import threading
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True  # This ensures the thread closes when the main program exits
    server_thread.start()
    bot = WhaleTracker()
    bot.run(os.getenv('DISCORD_TOKEN'))

if __name__ == "__main__":
    print("🚀 MAIN FUNCTION STARTING")
    main()
