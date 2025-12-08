================================================================================
                        VALORANT DISCORD BOT
================================================================================

AUTHOR: Yunes Al Akwaa

DESCRIPTION:
A Discord bot that integrates Valorant and Twitch APIs to provide real-time
match analysis and streamer detection. The bot automatically monitors your
matches and alerts when new games are detected.

PURPOSE:
- Query any player's latest Valorant match
- Identify opponents and check if they're streaming on Twitch
- Automatically detect new matches and send alerts
- Provide API status checks and diagnostics
- Display match opponents with embedded Twitch links

KEY FEATURES:
- !user <Name>#<Tag> - Search any player's latest match opponents
- !latest - Get your latest match with opponent Twitch status
- !test - Check all API connections and status
- Automatic match detection with Discord alerts
- Live Twitch stream detection for opponents
- Prefix matching for better Twitch search results

DEPENDENCIES:
- discord.py
- requests
- python-dotenv

SETUP:
1. Create a .env file with the following environment variables:
   DISCORD_TOKEN=<your_discord_bot_token>
   val_api_auth=<valorant_api_token>
   twitch_client_id=<twitch_client_id>
   twitch_client_token=<twitch_client_token>
   twitch_client_secret=<twitch_client_secret>

2. Configure your Valorant player info in the CONFIG section:
   - region (e.g., "na", "eu")
   - platform (e.g., "pc")
   - username (your in-game name)
   - tag (your in-game tag number)

3. Set the alert_channel_id to the Discord channel where you want alerts

4. Install dependencies:
   pip install -r requirements.txt

USAGE:
python main.py

The bot will:
- Connect to Discord and log in
- Start watching for new matches every 5 minutes
- Respond to commands in channels where it has permission
- Send alerts when new matches are detected
- Provide real-time Twitch information

COMMANDS:
- !user Username#Tag - Search opponent info for any player
- !latest - Get your latest match info
- !test - Verify all APIs are working
- !apivalues - Display current API configuration (debug)

MONITORING:
- Automatically checks for new matches every 5 minutes
- Sends embeds with opponent info and Twitch links
- Uses threading to run background checks without blocking bot

FEATURES:
- Smart Twitch username detection with prefix matching
- Deduplication of search results
- Live game filtering (only shows VALORANT players)
- Formatted Discord embeds with Twitch thumbnails
- Error handling and logging to discord.log

FILES:
- main.py: Main bot script
- requirements.txt: Python dependencies
- .env: Environment variables (create this)
- discord.log: Bot activity logs

NOTES:
- Requires all three APIs (Valorant, Twitch, Discord) to be properly configured
- Twitch tokens may need refresh if stale
- Bot must have permission to send messages in alert channel

================================================================================

LANGUAGES, TOOLS & FRAMEWORKS/LIBRARIES:

Languages:
- Python 3.x

Libraries:
- discord.py - Discord bot framework
- requests - HTTP library for API calls
- python-dotenv - Environment variable management

Features:
- Async/await for non-blocking operations
- Threading for background match monitoring
- Logging system (discord.log)

APIs:
- Discord API - Bot communication
- Valorant API - Match data and player stats
- Twitch API - Streamer search and live status

================================================================================
