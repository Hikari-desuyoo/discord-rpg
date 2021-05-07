#Links the tools functionality to discord bot using Input_manager class

import discord
from input_manager import Input_manager

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

#related to answer commands
input_manager = Input_manager(client)

@client.event
async def on_message(message):
    output = input_manager.process(message.content, message.author.id, message.guild.id)

    if output:
        #formats username in ex: "=get_user=13131241=get_user=" -> "Hikari"
        output_list = output.split('=get_user=')
        final_output = ""
        for i in range(len(output_list)):
            if i%2 == 0:
                final_output += output_list[i]
            else:
                #odd indexes means that substring was between '**'
                final_output += str(await client.fetch_user(int(output_list[i])))

        final_msg = "```python\n"
        final_msg += final_output
        final_msg += "\n```"
        await message.channel.send(final_msg)

#token.txt contains a discord bot token to connect to
with open("token.txt", "r") as f:
    token = f.read()

client.run(token)