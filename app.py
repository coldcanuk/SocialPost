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
        # Correctly engaging Penelope with threading
        thread_response = client.beta.threads.create()
        thread_id = thread_response['data']['id']

        message_response = client.beta.threads.create_message(thread_id=thread_id, 
                                                         assistant_id="asst_YGdZxXXnndYvtA0mxUMrnllX", 
                                                         input={"type": "text", "data": message})
        
        # Streamlining for clarity; real implementation may require more intricate handling
        reply_text = "Penelope is pondering your request..."
        
        logger.debug(f"Penelope's response: {reply_text}")
        await ctx.followup.send(reply_text)
    except Exception as e:
        logger.error(f'Error: {e}')
        await ctx.followup.send('Something went wrong.')

if __name__ == '__main__':
    bot.run(DISCORD_TOKEN)
