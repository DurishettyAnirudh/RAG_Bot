# bot.py

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import logging
from rag import initial_setup, handle_user_query

# Load .env variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Setup Discord bot
intents = discord.Intents.default()
intents.message_content = True  # Required for reading message content

bot = commands.Bot(command_prefix="!", intents=intents)

# Load vector store
db = initial_setup()

YOUR_USER_ID = 137794018932581990

@bot.event
async def on_ready():
    logging.info(f"{bot.user} is online and ready!")

@bot.command(name="hello")
async def hello(ctx):
    await ctx.send("👋 Hello!")

@bot.command(name="ask")
async def ask(ctx, *, query: str = None):
    if ctx.author.id == YOUR_USER_ID:
        logging.info("Skipping query from YOUR_USER_ID.")
        return

    if not query:
        await ctx.send("❓ Please provide a question. Usage: `!ask <your question>`")
        return

    logging.info(f"Received query from {ctx.author}: {query}")

    async with ctx.typing():
        response = handle_user_query(query, db)

    if not response:
        await ctx.send("❌ Sorry, I couldn't generate an answer right now. Please try again later.")
    else:
        await ctx.send(response)

# Run bot
bot.run(os.getenv("BOT_TOKEN"))
