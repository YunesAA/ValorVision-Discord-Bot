


# 🎮 Valorant Discord Bot

**Author:** Yunes Al Akwaa  

A Discord bot that integrates **Valorant** and **Twitch** APIs to provide **post-match streamer detection**. The bot monitors your matches automatically and sends alerts when new games are detected.

---

## 🚀 Features

- Query any player's latest Valorant match
- Identify opponents and check if they're streaming on Twitch
- Automatic match detection and Discord alerts
- API status checks and diagnostics
- Display match opponents with embedded Twitch links
- Smart Twitch username detection with prefix matching
- Deduplication of search results
- Live game filtering (only shows VALORANT players)
- Formatted Discord embeds with Twitch thumbnails

---

## ⚙️ Commands

| Command | Description |
|---------|-------------|
| `!user Username#Tag` | Search opponent info for any player |
| `!latest` | Get your latest match info with Twitch status |
| `!test` | Verify all APIs are working |
| `!apivalues` | Display current API configuration (debug) |

---

## 🖥️ Requirements

- Python 3.x  
- Discord account and bot token  

---

## 📦 Dependencies

- `discord.py` – Discord bot framework  
- `requests` – HTTP requests  
- `python-dotenv` – Environment variable management  

Install dependencies:

```bash
pip install -r requirements.txt
````

---

## ⚙️ Setup

1. Create a `.env` file in the project root with the following variables:

```env
DISCORD_TOKEN=<your_discord_bot_token>
val_api_auth=<valorant_api_token>
twitch_client_id=<twitch_client_id>
twitch_client_token=<twitch_client_token>
twitch_client_secret=<twitch_client_secret>
```

2. Update the **CONFIG** section in `main.py` with your Valorant info:

* `region` (e.g., `na`, `eu`)
* `platform` (e.g., `pc`)
* `username` (your in-game name)
* `tag` (your Valorant tag)

3. Set `alert_channel_id` to the Discord channel where you want alerts.

---

## ▶️ Usage

Run the bot:

```bash
python main.py
```

The bot will:

1. Connect to Discord and log in
2. Start watching for new matches every 5 minutes
3. Respond to commands in channels it has access to
4. Send alerts when new matches are detected
5. Provide real-time Twitch information

---

## ⏱️ Monitoring

* Automatic checks for new matches every 5 minutes
* Background threads prevent blocking bot commands
* Sends embeds with opponent info and Twitch links

---

## 📁 Project Structure

```text
.
├── main.py           # Main bot script
├── requirements.txt  # Python dependencies
└── .env              # Environment variables (create this)

```

---

## 🛠️ Tech Stack

### Language

* Python 3.x

### Libraries

* `discord.py` – Discord bot framework
* `requests` – HTTP requests
* `python-dotenv` – Environment variable management

### Features

* Async/await for non-blocking operations
* Threading for background monitoring

### APIs

* Discord API – Bot communication
* Valorant API – Match data and player stats
* Twitch API – Streamer search and live status

---

## ⚠️ Notes

* Requires all three APIs (Valorant, Twitch, Discord) to be properly configured
* Bot must have permission to send messages in the alert channel


