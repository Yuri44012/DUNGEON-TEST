import discord
from discord.ext import commands, tasks
import random
import datetime
import os

# === CONFIG === (load from environment)
TOKEN = os.getenv("DISCORD_TOKEN")  # Set this on Render
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "0"))  # Also set on Render

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

# Simulated data
islands = ['XZ City', 'Island-9', 'Neo Tokyo']
maps = ['Alienship', 'Desert Ruins', 'Cyber Factory']
bosses = ['Paitama', 'Lord Vex', 'Zoroid']
ranks = ['E', 'D', 'C', 'B', 'A']

# Image map for bosses
boss_images = {
    'Paitama': 'https://i.imgur.com/MEZ5K17.png',
    'Lord Vex': 'https://i.imgur.com/JX8I5cV.png',
    'Zoroid': 'https://i.imgur.com/3UwKqjB.png'
}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    send_dungeon_alert.start()

@tasks.loop(minutes=5)
async def send_dungeon_alert():
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        print("Invalid channel ID.")
        return

    data = {
        "Island": random.choice(islands),
        "Map": random.choice(maps),
        "Boss": random.choice(bosses),
        "Rank": random.choice(ranks),
        "Red Dungeon": random.choice([True, False]),
        "Double Dungeon": random.choice([True, False]),
        "Spawn Time": datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    }

    rank_colors = {
        'E': discord.Color.dark_red(),
        'D': discord.Color.red(),
        'C': discord.Color.orange(),
        'B': discord.Color.blue(),
        'A': discord.Color.gold(),
    }
    color = rank_colors.get(data["Rank"], discord.Color.default())

    embed = discord.Embed(
        title=f"**{get_rank_icon(data['Rank'])} RANK {data['Rank']} DUNGEON SPAWNED!**",
        description="A dungeon has just appeared in **Arise Crossover!**",
        color=color,
        timestamp=datetime.datetime.utcnow()
    )

    embed.add_field(name="**🌍 Island**", value=f"`{data['Island']}`", inline=True)
    embed.add_field(name="**🗺️ Map**", value=f"`{data['Map']}`", inline=True)
    embed.add_field(name="**👹 Boss**", value=f"`{data['Boss']}`", inline=True)
    embed.add_field(name="**🏅 Rank**", value=f"`{data['Rank']}`", inline=True)
    embed.add_field(name="**🔥 Red Dungeon**", value="✅ Yes" if data["Red Dungeon"] else "❌ No", inline=True)
    embed.add_field(name="**⚔️ Double Dungeon**", value="✅ Yes" if data["Double Dungeon"] else "❌ No", inline=True)
    embed.add_field(name="**⏰ Time**", value=f"`Spawned at: {data['Spawn Time']}`", inline=False)

    embed.set_footer(text="Dungeon Alert • Arise Crossover", icon_url="https://cdn-icons-png.flaticon.com/512/616/616408.png")

    if data["Boss"] in boss_images:
        embed.set_thumbnail(url=boss_images[data["Boss"]])

    await channel.send(embed=embed)

def get_rank_icon(rank):
    icons = {
        'E': '⚪',
        'D': '🟢',
        'C': '🔵',
        'B': '🟣',
        'A': '🟡',
    }
    return icons.get(rank, '⚔️')

bot.run(TOKEN)
