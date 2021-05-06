#Provides a class with all methods from rolling dices to storing sheets.(in progress)

from db_manager import *

class Request():
    def __init__(self, user_id, guild_id):
        self.user_id = user_id
        self.guild_id = guild_id

    #methods that only affects the user themself
    def set_active_group(self, group_name):
        group = get_group_by_name(self.guild_id, group_name)
        if group:
            members = get_group_members(group.id)
            member_id = -1
            for member in members:
                if member.user_id == self.user_id:
                    #user's Member object was found
                    member_id = member.id
            
            if member_id != -1:
                set_active_id(self.user_id, member_id)
                return "success"
            else:
                return "notmember"
        else:
            return "nogroup"

    def quit_group(self):
        member_id = get_active_id(self.user_id)
        delete_member(member_id)

    #methods for displaying data
    def show_active_group(self):
        group = get_active_group(self.user_id)
        if group:
            return group.name
        else:
            return False

    def show_group_members(self, group_name):
        members = get_group_members(get_group_by_name(self.guild_id, group_name).id)
        return members   
        
    def show_active_group_members(self):
        members = get_group_members(get_active_group(self.user_id).id)
        return members

    def show_all_groups(self):
        groups = get_groups_by_guild(self.guild_id)
        return [group.name for group in groups]

    def show_active_content(self):
        self.show_content(self.user_id)

    def show_content(self, user_id):
        return get_active_content(user_id)

    
    #others
    def new_group(self, name):
        if not get_group_by_name(self.guild_id, name):
            create_group(name, self.user_id, self.guild_id)
            self.set_active_group(name)
            return "success"
        else:
            return "nametaken"

    def add_user(self, new_user_id):
        create_member(new_user_id, get_active_group(self.user_id).id)

    def delete_user(self, delete_user_id):
        get_active_member(delete_user_id)
        if member:
            delete_member(member_id)
            return success
        else:
            return "notingroup"

    def delete_group(self):
        group_id = get_member_by_id(get_active_id(self.user_id)).group_id
        delete_group(group_id)


if __name__ == "__main__":
    request = Request(123,789)
    print(request.create())


