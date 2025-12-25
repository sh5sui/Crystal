import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv
from discord import app_commands
from discord import guild
import aiohttp

load_dotenv()

intents = discord.Intents.default()
intents.typing = False
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)
@bot.event
async def on_ready():
    print(f'Connected as {bot.user}')
    await bot.tree.sync()

@bot.tree.command(name="avatar", description="Get a users avatar")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def avatar(interaction: discord.Interaction, target: discord.User = None):

    await interaction.response.send_message(target.avatar.url)

@bot.tree.command(name="ping", description="Check if the bot is up and working")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def ping(interaction: discord.Interaction):
    
    await interaction.response.send_message("I'm online you fatass nigger")

@bot.tree.command(name="spam", description="Spam a message (6 times is the limit)")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def spam(interaction: discord.Interaction, message: str = None):
    await interaction.response.defer(ephemeral=False)

    await interaction.followup.send(message)
    await interaction.followup.send(message)
    await interaction.followup.send(message)
    await interaction.followup.send(message)
    await interaction.followup.send(message)
    await interaction.followup.send(message)

@bot.tree.command(name="funds", description="Shows info about a crypto wallet")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def funds(interaction: discord.Interaction, address: str = None):

    url = f"https://api.blockcypher.com/v1/ltc/main/addrs/{address}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                await interaction.response.send_message("API Error or invalid wallet address")
                return
            
            data = await resp.json()

            received = data["total_received"] / 100_000_000
            sent = data["total_sent"] / 100_000_000
            balance = data["balance"] / 100_000_000

            embed = discord.Embed(title="Litecoin wallet info", color=discord.Color.red())
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1436915087976960120/1452816495829844162/c74a69bb4fb30d1c3a8b722f07b593d7.jpg?ex=694e7c0c&is=694d2a8c&hm=73e4c351bb3eabfc939d3a2607a6ace500787ba2b005bae1c1e0e32b653eeaee&")
            embed.add_field(name="Wallet address", value=f"{address}", inline=False)
            embed.add_field(name="Received", value=f"{received:.8f} LTC", inline=False)
            embed.add_field(name="Sent", value=f"{sent:.8f} LTC", inline=False)
            embed.add_field(name="Balance", value=f"{balance:.8f} LTC", inline=False)

            await interaction.response.send_message(embed=embed)

@bot.tree.command(name="support", description="Support the creator of the bot")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def support(interaction: discord.Interaction):

    await interaction.resonpse.send.send_message("To support me, you can fund the creation of this bot or literally just use it so it gains traction. LTC Wallet: ltc1qq2mdrgw9svx8y2x0rd5mrmyv58r2g0psssvw3m")

@bot.tree.command(name="price", description="Check the price of litecoin in the current market")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def price(interaction: discord.Interaction):
    url = "https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                await interaction.response.send_message("API Error try again later")
                return
            
            data = await resp.json()

            current_price = data["litecoin"]["usd"]

            await interaction.response.send_message(f"The current price of litecoin is {current_price}")

@bot.tree.command(name="userinfo", description="Displays a users discord information")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def userinfo(interaction: discord.Interaction, target: discord.User = None):

    user_id = target.id

    embed=discord.Embed(title="User Information", color=discord.Color.red())
    embed.set_thumbnail(url=target.avatar.url)
    embed.add_field(name="Username", value=f"<@{user_id}>", inline=False)
    embed.add_field(name="Decoration", value=target.avatar_decoration)
    embed.add_field(name="Banner", value=target.banner.url)
    embed.add_field(name="IP", value="||Sudo apt install opsec||", inline=False)
    embed.add_field(name="Account created", value=target.created_at, inline=False)

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="robloxinfo", description="Get a roblox accounts info")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def robloxinfo(interaction: discord.Interaction, user: str = None):

    await interaction.response.send_message("In development")

Token = os.getenv("Token")
bot.run(Token)