#Deals with received messages and request the right commands to rpg_tools

import asyncio
import json 
from rpg_tools import Request

#contains methods for each command
class Commands():
    #formats strings like "example 1+1=**1+1**"
    def smart_format(self, target_string):
        #variables for confusing discord python highlight to be used by the json
        multiline_f = "f\"\"\"\n"
        multiline_f_end = "\n\"\"\"\n"
        normal_f = "f\""
        normal_f_end = "\"\n"
        br = "\n"
        comment = "#"

        string_list = target_string.split('**')
        final_string = ""
        for i in range(len(string_list)):
            if i%2 == 0:
                final_string += string_list[i]
            else:
                #odd indexes means that substring was between '**'
                final_string += str(eval(string_list[i]))
        return final_string

    def get_reply(self, command_key, reply_key):
        reply_string = self.replies[command_key][reply_key]
        return self.smart_format(reply_string)


    #commands

    #creates group
    def new(self, request, parameters):
        if parameters:
            self.new_group_name = parameters[0]
            output = request.new_group(self.new_group_name)
        else:
            output = "explain"

        return self.get_reply("new", output)

    #sets active
    def now(self, request, parameters):
        if parameters:
            self.wanted_group = parameters[0]
            output = request.set_active_group(self.wanted_group)
        else:
            self.active_group = request.show_active_group()
            output = "show" if self.active_group else "show_empty"

        return self.get_reply("now", output)

    #add member(in progress)
    def add(self, request, parameters):
        if parameters:
            self.new_group_name = parameters[0]
            output = request.new_group(self.new_group_name)
        else:
            output = "explain"

        return self.get_reply("add", output)

    def quit(self, request, parameters):
        if parameters[0] == "quit":
            self.left_group = request.show_active_group()
            output = request.quit_group()
        else:
            output = "explain"

        return self.get_reply("quit", output)


class Input_manager(Commands):
    def __init__(self):
        #opens json with proper responses
        with open("replies.json", "r") as f:
            self.replies = json.loads(f.read())
         
        self.commands = {
            "new":self.new,
            "create":self.new,

            "quit":self.quit,
            "exit":self.quit,

            "now":self.now,
            "select":self.now,
            "sel":self.now,
            "s":self.now,

            "add":self.add
        }

    def process(self, command, args, user_id, guild_id):
        request = Request(user_id, guild_id)
        self.user_id = user_id
        self.guild_id = guild_id

        parameters = args

        command_method = self.commands.get(command, None)
        if command_method:
            return command_method(request, parameters)



if __name__ == "__main__":
    #can be seem as an discord message emulator for debugging.
    input_manager = Input_manager()

    user_id = 1
    guild_id = 1
    while True:
        message = input(f"u{user_id}|g{guild_id}>")
        if message.startswith("c"):#changes user and guild, ex: "c 23 34"
            try:
                message = message.split(" ")[1:]
                user_id, guild_id = [int(item) for item in message]
            except:
                print("wrong input for changing user")
        else:
            if message.startswith('.'):
                message_list = message[1:].split(" ")
                command = message_list[0]
                args = message_list[1:]
                try:
                    args.remove("")
                except:
                    pass
                processed = input_manager.process(command, args, user_id, guild_id)
                print(processed) if processed else ""

