# Spear
A quick experimental project focused on tracking profitable traders and monitoring projects in the Solana and Base ecosystems through Discord bots.

> **Note**: The Solana tracking component was discontinued due to high API costs. The Base virtuals tracking has seen limited utility due to low trading volume.

## Overview

Spear consists of two main components:

### 1. Discord Bots
- **Sailor.py**: Monitors Solana wallet addresses for significant transactions
- **BondingCurve.py**: Tracks Base protocol virtual agents that have "bonded" and graduated to Uniswap pools

### 2. Profitable Trader Finders
- **WhaleFinder.py**: Flask-based API for analyzing profitable traders
- **WhaleFinder2.py**: Standalone script version with enhanced rate limiting

## Installation

1. **Clone the Repository**:
```bash
git clone https://github.com/yourusername/Spear.git
cd Spear
```

2. **Install Dependencies**:
```bash
pip install -r bots/requirements.txt
```

3. **Environment Setup**:
Create a `.env` file in the `bots` directory:
```
DISCORD_TOKEN=your_discord_bot_token
SOLSCAN_API_KEY=your_solscan_api_key  # If using Solana tracking
```

## Running the Bots

### Discord Bots

1. **Start Sailor (Solana Tracking)**:
```bash
cd bots
python Sailor.py
```

2. **Start BondingCurve (Base Protocol)**:
```bash
cd bots
python bondingCurve.py
```

The bots will automatically connect to Discord and begin monitoring their respective networks.

### Whale Finder

1. **Start the Flask API**:
```bash
cd profitableTraderFinders
python whaleFinder.py
```
Access the analysis endpoint at `http://localhost:5000/analyze`

2. **Run Standalone Analysis**:
```bash
cd profitableTraderFinders
python whaleFinder2.py
```

## Configuration

### Wallet Tracking
Add wallet addresses to track in `bots/wallet.txt`:
```
WalletName: address
```

### Discord Channels
Update the channel IDs in the bot files to match your Discord server setup:
- Sailor.py: `DISCORD_CHANNEL_IDS`
- BondingCurve.py: `DISCORD_CHANNEL_ID`

## Project Goals

1. **Trader Analysis**: Identify and track successful traders on Solana to understand their strategies
2. **Virtual Agent Monitoring**: Track the lifecycle of Base protocol virtual agents from bonding to graduation
3. **Real-time Notifications**: Provide immediate alerts for significant trading activity and market events

## Limitations

- Solana API costs made continuous tracking unsustainable
- Base protocol virtual agents have seen limited trading volume
- Rate limiting affects the speed of data collection

## License

This project is built solely by Oliver Tipton.
