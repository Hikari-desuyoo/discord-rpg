#Deals with received messages and request the right commands to rpg_tools

import asyncio
import json 
from rpg_tools import Request

class Formatting():
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

    def insert_user(self, user_id=False):
        if not user_id:
            user_id = self.user_id
        
        return f"=get_user={user_id}=get_user="

    def get_reply(self, command_key, reply_key):
        reply_string = self.replies[command_key][reply_key]
        return self.smart_format(reply_string)

#commands to display info, strongly linked to replies.json
class Show_commands():
    def get_show(self, key):
        #made to be used from inside replies.json or Show class
        return self.smart_format(self.replies['show'][key])

    def show_groups(self):
        all_groups = self.request.show_all_groups()
        group_string_list = [f"{count+1}) {{{group}}}" for count, group in enumerate(all_groups)]
        group_string = '\n'.join(group_string_list)
        return group_string
        
    def show_members(self):
        member_list = self.request.show_active_group_members()
        if member_list == "nogroup":
            return self.get_show("now_empty")

        final_string = ''
        for member_obj in member_list:
            sheet_info = json.loads(member_obj.content).name if member_obj.content!="" else "Sem ficha"

            final_string += f"\n{{{self.insert_user(member_obj.user_id)}}} - {sheet_info}"
        return final_string

class Group_management():
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

    #add member
    def add(self, request, parameters):
        output = "explain"
        if parameters:
            output = "notmention"
            user_id = self.validate_mention(parameters[0])
            if user_id:
                self.added_user_id = user_id
                self.active_group = request.show_active_group()
                output = self.request.add_member(user_id)
            
        return self.get_reply("add", output)


    #remove member
    def remove(self, request, parameters):
        output = "explain"
        if parameters:
            output = "notmention"
            user_id = self.validate_mention(parameters[0])
            if user_id:
                self.removed_user_id = user_id
                self.active_group = request.show_active_group()
                output = self.request.delete_member(user_id)
            
        return self.get_reply("delete", output)

    #exits group
    def quit(self, request, parameters):
        if parameters and parameters[0] == "quit":
            self.left_group = request.show_active_group()
            output = request.quit_group()
        else:
            output = "explain"

        return self.get_reply("quit", output)

class Sheet_management():
    pass

#wraps command classes
class Commands(Formatting, Show_commands, Group_management, Sheet_management):
    def validate_mention(self, mention_string):
        #mention_string is expected to be <@!23132131321>
        invalid_mention = True
        user_mention = mention_string.replace("<@!","").replace(">","")
        if user_mention.isdigit() and mention_string.startswith("<@!") and mention_string.endswith(">"):
            user_id = int(user_mention)
            invalid_mention = False
        
        if invalid_mention:
            return False
        else:
            return user_id

class Input_manager(Commands):
    def __init__(self):
        #opens json with proper responses
        with open("replies.json", "r") as f:
            json_string = f.read()

        #this is for allowing breaking lines on json file
        json_string = json_string.replace("\n        ","")
        self.replies = json.loads(json_string)
        
        self.commands = {
            #group management
            "novo":self.new,
            "criar":self.new,
            "new":self.new,
            "create":self.new,
            "grupo":self.new,
            "group":self.new,
            "grupos":self.new,
            "groups":self.new,

            "quit":self.quit,
            "exit":self.quit,
            "sair":self.quit,

            "now":self.now,
            "select":self.now,
            "sel":self.now,
            "s":self.now,
            "selecionar":self.now,
            "ativar":self.now,
            "jogar":self.now,
            "play":self.now,

            "add":self.add,
            "member":self.add,
            "membro":self.add,
            "members":self.add,
            "membros":self.add,

            "remove":self.remove,
            "del":self.remove,
            "ban":self.remove
        }

    def process(self, command, args, user_id, guild_id):
        self.request = Request(user_id, guild_id)
        self.user_id = user_id
        self.guild_id = guild_id

        parameters = args

        command_method = self.commands.get(command, None)
        if command_method:
            return command_method(self.request, parameters)



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

