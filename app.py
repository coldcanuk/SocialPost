import sys
import os
from flask import Flask
from discord.ext import commands
import discord
from loguru import logger
from openai import OpenAI

# Load environment variables
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Create the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Setup logging
DEBUG_MODE = os.getenv('DEBUG_MODE', 'False').lower() in ('true', '1', 't')
log_level = "DEBUG" if DEBUG_MODE else "INFO"
logger.add(sys.stdout, level=log_level)

app = Flask(__name__)

# Configure Discord
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    logger.info('Bot is online and ready.')
    print('Bot is online and marked as healthy.')

@bot.slash_command(name="post", description="Invoke Penelope for a message")
async def post(ctx, message: str):
    logger.debug(f"Received post command with text: {message}")
    await ctx.defer()
    try:
        # Step 2 Create a thread
        thread = client.beta.threads.create()
        thread_id=thread['id']
        logger.debug(f"the thread ID is {thread_id} ")
        # Step 3 Add a message to the thread
        message_response = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message  # Correct way to pass the message
        )
        # Step 4: Create and stream a run - this part needs adjustment based on API capabilities and desired behavior

        # Simplification for demonstration - adjust according to actual requirements
        reply_text = "Message received and processed by Penelope."  # Placeholder response

        logger.debug(f"Penelope's response: {reply_text}")
        await ctx.followup.send(reply_text)
    except Exception as e:
        logger.error(f'Error: {e}')
        await ctx.followup.send('Something went wrong.')

if __name__ == '__main__':
    bot.run(DISCORD_TOKEN)
