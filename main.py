#Links the tools functionality to discord bot using Input_manager class

from discord.ext import commands
from input_manager import Input_manager

bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))

#related to answer commands
input_manager = Input_manager()

#assigns a function to all bots commands for finding and executing the right input_manager command
for command_name in input_manager.commands.keys():
    @bot.command(name = command_name)
    async def right_command(ctx, *args):
        user_id = ctx.author.id
        guild_id = ctx.guild.id
        command = ctx.invoked_with

        output = input_manager.process(command, args, user_id, guild_id)
        

        if output:
            #formats username as in ex: "=get_user=13131241=get_user=" -> "Hikari"
            output_list = output.split('=get_user=')
            final_output = ""
            for i in range(len(output_list)):
                if i%2 == 0:
                    final_output += output_list[i]
                else:
                    try:
                        final_output += str(await bot.fetch_user(int(output_list[i])))
                    except:
                        #avoids crashing by injection
                        final_output += output_list[i]

            final_msg = "```python\n"
            final_msg += final_output
            final_msg += "\n```"
            await ctx.send(final_msg)

#token.txt contains a discord bot token to connect to
with open("token.txt", "r") as f:
    token = f.read()

bot.run(token)