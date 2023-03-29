import os
import openai
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# Set up the Discord client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Set up the GPT-3 API client
openai.api_key = os.getenv('OPENAI_API_KEY')

# Set up a function to generate a response using the GPT-3 API
def generate_response(message):
    # Send the message to the GPT-3 API and get the response
    response = openai.Completion.create(
        engine="davinci",
        prompt=message.content,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Get the generated text from the response
    generated_text = response.choices[0].text.strip()

    # Return the generated text as the bot's response
    return generated_text

# Set up an event listener for incoming messages
@client.event
async def on_message(message):
    # Ignore messages sent by the bot itself
    if message.author == client.user:
        return

    # Generate a response using the GPT-3 API
    response = generate_response(message)

    # Send the response back to the Discord server
    await message.channel.send(response)

# Start the Discord client
client.run(TOKEN)
