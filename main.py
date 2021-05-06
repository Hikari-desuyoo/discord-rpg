#Links the tools functionality to discord bot using Input_manager class

import discord
from input_manager import Input_manager

client = discord.Client()

@client.event
async def on_ready():
    print(client.get_user(378628192581320706))
    print('Logged in as {0.user}'.format(client))

#related to answer commands
input_manager = Input_manager()

@client.event
async def on_message(message):
    output = input_manager.process(message.content, message.author.id, message.guild.id)
    if output:
        final_msg = "```python\n"
        final_msg += output
        final_msg += "\n```"
        await message.channel.send(final_msg)

#token.txt contains a discord bot token to connect to
with open("token.txt", "r") as f:
    token = f.read()

client.run(token)