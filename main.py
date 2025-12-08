import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import requests
import time
import threading
import asyncio
from datetime import datetime

# ------------------ CONSTANTS ------------------

url_val = "https://val-api-wrapper.up.railway.app/"
url_twitch = "https://api.twitch.tv/helix/search/channels?query="
TOKEN_URL = "https://id.twitch.tv/oauth2/token"



# -------------- AUTHENTICATION --------------
load_dotenv()
val_api_auth = os.getenv("val_api_auth")
twitch_client_id = os.getenv("twitch_client_id")
twitch_client_token = os.getenv("twitch_client_token")
token = os.getenv("DISCORD_TOKEN")
twitch_client_secret= os.getenv("twitch_client_secret")
# --------------------------------------------

# ------------------ CONFIG ------------------
region = "na"
platform = "pc"
username = "cookie" # username without tag
tag = "tvoid" # tag without #
my_ign = f"{username}#{tag}"
# --------------------------------------------


# ---------------- FUNCTIONS -----------------
def time_to_minutes(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes}m {seconds}s"

def print_players(players):
    for ign in players:
        print(f" - {ign}")
# --------------------------------------------

# --------------- Variables ------------------
prefixes = ["TTV", "TTV_", "ttv", "its", "im", "itz",'','not', 'its', 'official', 'xxx', 'sir', 'mr', 'ms',""]
last_match_id = "a8e3e5ca-4de6-46c3-991f-9ded4df1a"
alert_channel_id = int(os.getenv("channel_id"))
# --------------------------------------------

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    print('------')
    thread = threading.Thread(target=match_watcher, daemon=True)
    thread.start()

@bot.command()
async def user(ctx, *, player: str):
    """Check any player's latest Valorant match and search Twitch for opponents"""
    await ctx.send(f"🔍 Searching match data for `{player}`...")

    try:
        # Split username and tag (example: "Not Milk#notme")
        if "#" not in player:
            await ctx.send("⚠️ Please use the correct format: `!user Username#Tag`")
            return

        username, tag = player.split("#", 1)

        # Fetch match list for that user
        matchlist = requests.get(
            f"{url_val}valorant/v4/matches/{region}/{platform}/{username}/{tag}",
            headers={"Authorization": f"{val_api_auth}"}
        ).json()

        # Handle invalid name/tag
        if not matchlist.get("data"):
            await ctx.send("❌ Could not find any matches for that user.")
            return

        # Gather opponent names
        players = []
        for player_data in matchlist["data"][0]["players"]:
            ign = f"{player_data['name']}#{player_data['tag']}"
            players.append(ign)
            print(f"Found player: {players}")

        # Filter out the user themselves
        opponents = [p for p in players if p.lower() != f"{username}#{tag}".lower()]

        # Create embed
        embed = discord.Embed(
            title=f"🟪 Opponents from {username}#{tag}'s Latest Match",
            description=f"✅ Found {len(opponents)} opponents\n",
            color=discord.Color.purple()
        )

        # Search Twitch for each opponent
        for opp in opponents:
            riot_name = opp.split("#")[0]
            twitch_users = get_possible_twitch_names(riot_name)

            if twitch_users:
                for user in twitch_users:
                    login = user["broadcaster_login"]
                    display = user["display_name"]
                    thumb = user["thumbnail_url"]

                    embed.add_field(
                        name=f"🔴 {opp}",
                        value=f"**[{display}](https://twitch.tv/{login})** is live",
                        inline=False
                    )
                    embed.set_thumbnail(url=thumb)
            else:
                embed.add_field(
                    name=f"⚪ {opp}",
                    value="Not streaming",
                    inline=False
                )

        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"❌ Error: `{e}`")


@bot.command()
async def latest(ctx):
    await ctx.send("Fetching latest game info...")

    embed = await latest_game_embed()   

    await ctx.send("Found!")
    await ctx.send("Searching Twitch streams...")
    await ctx.send(embed=embed) 

@bot.command()
async def test(ctx):
    await ctx.send("🔍 Running API tests...")

    val_result = test_valorant_api()
    twitch_result = test_twitch_api()
    disc_result = test_discord_token()

    embed = discord.Embed(
        title="✅ API Status Check",
        color=discord.Color.blue()
    )

    embed.add_field(name="🎯 Valorant API", value=val_result, inline=False)
    embed.add_field(name="🟪 Twitch API", value=twitch_result, inline=False)
    embed.add_field(name="🤖 Discord Token", value=disc_result, inline=False)

    await ctx.send(embed=embed)

@bot.command()
async def apivalues(ctx):
    await ctx.send("📡 Fetching API values...")
    val_text = f"val_api_auth: {val_api_auth}"
    twitch_text = f"twitch_client_id: {twitch_client_id}\n twitch_client_token: {twitch_client_token}\n twitch_client_secret: {twitch_client_secret}"
    disc_text = f"DISCORD_TOKEN: {token}"

    embed = discord.Embed(
        title="📊 API Values",
        color=discord.Color.green()
    )
    embed.add_field(name="🎯 Valorant", value=val_text, inline=False)
    embed.add_field(name="🟪 Twitch", value=twitch_text, inline=False)
    embed.add_field(name="🤖 Discord", value=disc_text, inline=False)

    await ctx.send(embed=embed)

async def latest_game_embed():
    matchlist = requests.get(
        f"{url_val}valorant/v4/matches/{region}/{platform}/{username}/{tag}",
        headers={"Authorization": f"{val_api_auth}"}
    ).json()

    if not matchlist.get("data"):
        return discord.Embed(
            title="❌ Could not fetch match list",
            description="Check name, tag, or region.",
            color=discord.Color.red()
        )

    players = []
    for player in matchlist["data"][0]["players"]:
        ign = f"{player['name']}#{player['tag']}"
        players.append(ign)

    opponents = [p for p in players if p.lower() != my_ign.lower()]

    embed = discord.Embed(
        title="🟪 Latest Match Opponents",
        description=f"✅ Found {len(opponents)} opponents\n",
        color=discord.Color.purple()
    )

    for opp in opponents:
        riot_name = opp.split("#")[0]
        twitch_users = get_possible_twitch_names(riot_name)

        if twitch_users:
            for user in twitch_users:
                login = user["broadcaster_login"]
                display = user["display_name"]
                thumb = user["thumbnail_url"]

                embed.add_field(
                    name=f"🔴 {opp}",
                    value=f"**[{display}](https://twitch.tv/{login})** is live",
                    inline=False
                )
                embed.set_thumbnail(url=thumb)
        else:
            embed.add_field(
                name=f"⚪ {opp}",
                value="Not streaming",
                inline=False
            )

    return embed

def get_possible_twitch_names(name):
    lower_name = name.lower()

    def search_twitch_player(name):
        searches = [f"{p} {name}".strip() for p in prefixes] + [name]
        all_results = []

        for search in searches:
            query = search.split("#")[0]
            url = f"https://api.twitch.tv/helix/search/channels?query={query}"

            try:
                res = requests.get(url, headers={
                    "Client-ID": twitch_client_id,
                    "Authorization": f"Bearer {twitch_client_token}"
                })

                data = res.json()
                print(f"Twitch search for '{query}' returned {len(data.get('data', []))} results.")
                if "data" not in data:
                    continue

                for c in data["data"]:
                    if c.get("is_live") and c.get("game_name") in ["VALORANT"]:
                        # Fix thumbnail URL
                        thumb = c.get("thumbnail_url", "")
                        if thumb:
                            thumb = thumb.replace("{width}x{height}", "320x180")
                            c["thumbnail_url"] = thumb
                        all_results.append(c)

            except Exception as e:
                print(f"Twitch API error: {e}")
                continue

        # Deduplicate
        unique = {}
        for ch in all_results:
            login = ch.get("broadcaster_login")
            if login not in unique:
                unique[login] = ch

        return list(unique.values())

    live_users = search_twitch_player(name)
    return live_users  # return full objects

def match_watcher():
    print("🕵️ Starting match watcher thread...")
    global last_match_id

    while True:
        try:
            data = requests.get(
                f"{url_val}valorant/v4/matches/{region}/{platform}/{username}/{tag}",
                headers={"Authorization": f"{val_api_auth}"}
            ).json()

            current_time = datetime.now().strftime("%H:%M")
            match_id = data["data"][0]["metadata"]["match_id"]
            print(f"[{current_time}] Checked match ID: {match_id}")
            
            if last_match_id is None:
                last_match_id = match_id

            elif match_id != last_match_id:
                last_match_id = match_id
                print("⚠️ New match detected!")

                channel = bot.get_channel(alert_channel_id)
                if channel:
                    asyncio.run_coroutine_threadsafe(
                        channel.send("✅ New match detected!"), bot.loop
                    )
                    asyncio.run_coroutine_threadsafe(
                        send_match_embed(channel), bot.loop
                    )

        except Exception as e:
            print("Watcher error:", e)


        tests()
        time.sleep(300)  # 5 mins

async def send_match_embed(channel):
    embed = await latest_game_embed()
    await channel.send(embed=embed)

def get_twitch_client_token():
    global twitch_client_token
    resp = requests.post(TOKEN_URL, data={
        "client_id": twitch_client_id,
        "client_secret": twitch_client_secret,
        "grant_type": "client_credentials"
    })

    resp.raise_for_status()
    twitch_client_token = resp.json()["twitch_client_token"]
    return twitch_client_token

def twitch_request(url, params=None):
    global twitch_client_token

    if not twitch_client_token:
        get_twitch_client_token()

    headers = {
        "Client-ID": twitch_client_id,
        "Authorization": f"Bearer {twitch_client_token}"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 401:
        print("⚠️ Token expired, refreshing...")
        get_twitch_client_token()
        headers["Authorization"] = f"Bearer {twitch_client_token}"
        response = requests.get(url, headers=headers, params=params)

    response.raise_for_status()
    return response.json()

# data = twitch_request(url_twitch + "d1ve")
# print(data)

# ------------------ TESTS -------------------
def tests():
    test_discord_token()
    test_twitch_api()
    test_valorant_api()


def test_valorant_api():
    try:
        res = requests.get(
            f"{url_val}status",
            headers={"Authorization": val_api_auth}
        )

        if res.status_code == 200:
            return "✅ OK"
        else:
            return f"❌ BAD RESPONSE ({res.status_code})"
    except Exception as e:
        return f"❌ FAILED\n`{e}`"
    
def test_twitch_api():
    try:
        res = requests.get(
            "https://api.twitch.tv/helix/search/channels?query=valorant",
            headers={
                "Client-ID": twitch_client_id,
                "Authorization": f"Bearer {twitch_client_token}"
            }
        )

        data = res.json()

        if res.status_code == 200 and "data" in data:
            return f"✅ OK ({len(data['data'])} results)"
        else:
            return f"❌ BAD RESPONSE ({res.status_code})"
    except Exception as e:
        return f"❌ FAILED\n`{e}`"
    
def test_discord_token():
    if token and len(token) > 10:
        return "✅ Token Loaded"
    else:
        return "❌ Missing / Invalid" 



bot.run(token, log_handler=handler, log_level=logging.DEBUG)
