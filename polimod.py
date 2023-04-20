import discord
import openai
import os
import aiohttp

# Create a custom aiohttp client session with SSL verification disabled
session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False))

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    # Set the bot's status to invisible
    await client.change_presence(status=discord.Status.invisible)
    print(f"Logged in as {client.user}")

# You'll need to set your API key as an environment variable, or enter it manually here:
openai.api_key = "YOUR-OPENAI-API-KEY"

# Replace "your_role_name" with the name of the role you want to assign
YOUR_ROLE_NAME = "Politics"

async def check_message_for_politics(message):
    # Only check messages in text channels and ignore bots
    if isinstance(message.channel, discord.TextChannel) and not message.author.bot:
        # Check if the message is in the #politics channel
        if message.channel.name.lower() != 'politics':
            # Get the content of the message
            content = message.content
            # Generate a response from GPT-3
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"Is the following message political in nature, or involve politicians, for example, Donald Trump?\n{content}\n",
                temperature=0.8,
                max_tokens=200,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            # Check if GPT-3 identified the message as political
            if "yes" in response.choices[0].text.lower():
                # Find the politics channel on the server
                politics_channel = discord.utils.get(message.guild.text_channels, name='politics')
                # Send a message to the channel asking members to visit the politics channel
                message = await message.channel.send(f"{message.author.mention}, please use the {politics_channel.mention} channel for political discussions.\n \nClick the reaction button below to gain access to {politics_channel.mention}")
                # Add the "🔑" reaction to the message
                await message.add_reaction("🔑")


@client.event
async def on_reaction_add(reaction, user):
    # Check if the reaction is the "🔑" emoji
    if reaction.emoji == "🔑":
        # Get the server the reaction was made on
        server = reaction.message.guild
        # Find the role with the name specified above
        role = discord.utils.get(server.roles, name=YOUR_ROLE_NAME)
        # Assign the role to the user who reacted
        await user.add_roles(role)


@client.event
async def on_message(message):
    await check_message_for_politics(message)

client.run('YOUR-DISCORD-BOT-TOKEN')
