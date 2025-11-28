import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv
from discord import app_commands
from discord import guild

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

@bot.tree.command(name="userinfo", description="Displays a users discord information")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def userinfo(interaction: discord.Interaction, target: discord.User = None):

    user_id = target.id

    embed=discord.Embed(title="User Information", color=discord.Color.red())
    embed.set_thumbnail(url=target.avatar.url)
    embed.add_field(name="Username", value=f"<@{user_id}>", inline=False)
    embed.add_field(name="Decoration", value=target.avatar_decoration)
    embed.add_field(name="Banner", value=target.banner)
    embed.add_field(name="IP", value="||Sudo apt install opsec||", inline=False)
    embed.add_field(name="Account created", value=target.created_at, inline=False)

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="robloxinfo", description="Get a roblox accounts info")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def robloxinfo(interaction: discord.Interaction, user: str = None):

    await interaction.response.send_message("In development")

Token = os.getenv("Token")
bot.run(Token)