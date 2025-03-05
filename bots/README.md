# Spear Discord Bots

Welcome to the Discord Bots project! This repository contains two powerful bots designed to enhance your Discord experience by integrating blockchain technology. These bots allow you to monitor virtual agents and receive real-time updates on Solana wallets of your choice.

## Overview

### BondingCurve.py

`bondingCurve.py` is a Discord bot that leverages blockchain technology to track the lifecycle of virtual agents. By utilizing bonding curves, this bot can determine when virtual agents graduate or launch, depending on your level of engagement. 

- **Key Features**:
  - **Blockchain Integration**: Utilizes smart contracts to monitor the status of virtual agents.
  - **Real-Time Updates**: Get notified instantly when agents reach significant milestones.
  - **Customizable Alerts**: Tailor notifications based on your preferences and engagement level.

### Sailor.py

`Sailor.py` is a dedicated Discord bot for monitoring Solana wallets. With Sailor, you can watch specific wallets and receive updates on transactions, balances, and other important events.

- **Key Features**:
  - **Wallet Monitoring**: Keep track of multiple Solana wallets effortlessly.
  - **Instant Notifications**: Receive real-time alerts for transactions and updates.
  - **User-Friendly Interface**: Easily configure and manage your watched wallets through Discord commands.

## Installation

To set up these bots on your local machine, follow these steps:

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

3. **Configure the Bots**:
   - Create a `.env` file in the root directory and add your Discord bot token and any other necessary configuration variables.
   - Example:
     ```
     DISCORD_TOKEN=your_discord_bot_token
     ```

4. **Run the Bots**:
   Start the bots using the following command:
   ```bash
   python bondingCurve.py
   python sailor.py
   ```

## Usage

### Adding Bots to Your Discord Server

To add the bots to your Discord server, follow these steps:

1. **Create a Discord Bot**:
   - Go to the [Discord Developer Portal](https://discord.com/developers/applications).
   - Click on **"New Application"** and give your bot a name.
   - Navigate to the **"Bot"** tab and click **"Add Bot"**.

2. **Get Your Bot Token**:
   - Under the **"Bot"** tab, you will find the **"Token"** section. Click **"Copy"** to copy your bot token. You will need this for configuration.

3. **Invite Your Bot to Your Server**:
   - In the **"OAuth2"** tab, scroll down to **"Scopes"** and select **"bot"**.
   - Under **"Bot Permissions"**, select the permissions your bot needs (e.g., Send Messages, Read Message History).
   - Copy the generated URL and paste it into your browser to invite the bot to your server.

4. **Configure the Bots**:
   - Create a `.env` file in the root directory of your project and add your Discord bot token and any other necessary configuration variables.
   - Example:
     ```
     DISCORD_TOKEN=your_discord_bot_token
     ```

### Hosting the Bots

You can host these bots on platforms like Render or AWS to keep them running continuously. Here's a brief overview of how to do this:

#### Hosting on Render

1. **Create a Render Account**: Sign up at [Render.com](https://render.com/).

2. **Create a New Web Service**:
   - Click on **"New"** and select **"Web Service"**.
   - Connect your GitHub repository containing the bot code.

3. **Configure the Service**:
   - Set the environment to **Python** and specify the build command (e.g., `pip install -r requirements.txt`).
   - Set the start command to run your bot (e.g., `python bondingCurve.py` or `python sailor.py`).

4. **Add Environment Variables**: In the settings, add your Discord bot token as an environment variable.

5. **Deploy**: Click **"Create Web Service"** to deploy your bot.

#### Hosting on AWS

1. **Create an AWS Account**: Sign up at [aws.amazon.com](https://aws.amazon.com/).

2. **Set Up an EC2 Instance**:
   - Launch a new EC2 instance with a suitable Amazon Machine Image (AMI) (e.g., Ubuntu).
   - Configure security groups to allow inbound traffic on the necessary ports.

3. **SSH into Your Instance**: Use SSH to connect to your EC2 instance.

4. **Install Dependencies**:
   - Install Python and any required packages:
     ```bash
     sudo apt update
     sudo apt install python3-pip
     pip3 install -r requirements.txt
     ```

5. **Run Your Bot**: Start your bot using:
   ```bash
   python bondingCurve.py
   ```

6. **Keep the Bot Running**: Consider using a process manager like `screen` or `tmux` to keep your bot running in the background.

### Interacting with the Bots

Once the bots are running, they will post notifications in the channels which you give them permission.  This can be seen in the picture below
![Discord Bots](./pic.png)
![Discord Bots](./pic2.png)
## Contributing

We welcome contributions to improve these bots! If you have suggestions or find bugs, please open an issue or submit a pull request.

## License

These projects are built solely by Oliver Tipton