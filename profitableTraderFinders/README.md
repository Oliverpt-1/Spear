# WhaleFinder

WhaleFinder is a Python script that utilizes the Solscan API to analyze token holders and their transactions on the Solana blockchain. This tool is designed to help users identify significant holders (whales) of specific tokens and track their balance changes, profits, and top holdings.

## Features

- **Top Holders Analysis**: Retrieve the top holders of a specified token and analyze their wallet activities.
- **Balance Change Tracking**: Monitor balance changes for specific wallets over time, allowing you to see when significant transactions occur.
- **Token Price Retrieval**: Get the price of a token at a specific timestamp to analyze profits and losses.
- **Top Holdings Overview**: Identify the top holdings of a wallet in USD, providing insights into the most valuable assets held.

## Installation

To set up WhaleFinder on your local machine, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/discord-bots.git
   cd discord-bots
   ```

2. **Install Dependencies**:
   Make sure you have Python 3.7 or higher installed. Then, install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:
   - Create a `.env` file in the root directory and add your Solscan API key:
     ```
     SOLSCAN_API_KEY=your_solscan_api_key
     ```

## Usage

To use WhaleFinder, you can run the script directly or integrate it into a larger application. Here's how to run it as a standalone Flask application:

1. **Run the Flask App**:
   ```bash
   python whaleFinder.py
   ```

2. **Access the API Endpoint**:
   - Once the app is running, you can access the analysis endpoint by navigating to:
     ```
     http://127.0.0.1:5000/analyze
     ```
   - This will trigger the analysis of specified token holders and return the top holdings and top gainers in JSON format.

## API Endpoint

### `/analyze`

- **Method**: `GET`
- **Description**: Analyzes the top holders of predefined tokens and returns their top holdings and profit information.
- **Response**: Returns a JSON object containing:
  - `top_10_holdings`: The top 10 holdings across all analyzed wallets.
  - `top_5_gainers`: The top 5 wallets with the largest profit percentages.

## Example Response

```json
{
  "top_10_holdings": [
    {"token_address": "Token1", "usd_value": 10000},
    {"token_address": "Token2", "usd_value": 8000},
    ...
  ],
  "top_5_gainers": [
    ["wallet_address_1", 600],
    ["wallet_address_2", 550],
    ...
  ]
}
```

## Contributing

We welcome contributions to improve WhaleFinder! If you have suggestions or find bugs, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgments

- Special thanks to the developers of the libraries and frameworks that made this project possible.
- Thanks to the Solana community for their support and resources.

---

Feel free to customize this README further to fit your project's specific needs and branding! 