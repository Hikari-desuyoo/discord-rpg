#Provides functions for dealing with the database indirectly.

import json
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

#initial json for rpg sheets
start_content = ""

#starts db for all rpg games
engine = create_engine('sqlite:///all_games.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

#users-active_sheet relation table
class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, unique=True)#discord user id
    active_member_id = Column(Integer)
    def __repr__(self):
        return f"<[User object]user_id:{self.user_id}; active_member_id:{self.active_member_id}>"

#group table
class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    guild_id = Column(Integer)
    def __repr__(self):
        return f"<[Group object]id:{self.id}; name:{self.name}>"

#sheet table
class Member(Base):
    __tablename__ = "members"

    #identifies the sheet
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer)
    user_id = Column(Integer)

    #sheet json or gm stuff
    content = Column(String)

    def __repr__(self):
        return f"<[Member object]id:{self.id};group_id:{self.group_id}; user_id:{self.user_id}>"

#create all
Base.metadata.create_all(engine)

#functions to use the database


#user related
def create_user(user_id):
    user = User(user_id=user_id, active_member_id=-1)
    session.add(user)
    session.commit()
    return user

def get_or_create_user(user_id):
    user = session.query(User).filter_by(user_id=user_id).first()
    if not user:
        user = create_user(user_id)
    return user


#member related
def create_member(user_id, group_id):
    group = session.query(Group).filter_by(id=group_id).first()
    if not group:
        raise Exception("Assigned group to new member does not exist")
    get_or_create_user(user_id)
    member = Member(group_id=group_id, user_id=user_id, content=start_content)
    session.add(member)
    session.commit()

def delete_member(member_id):
    member = session.query(Member).filter_by(id=member_id).first()
    user = session.query(User).filter_by(user_id=member.user_id).first()
    user.active_member_id = -1
    session.delete(member)
    members = session.query(Member).filter_by(group_id=member.group_id).all()
    if not members:
        try:
            delete_group(member.group_id)
        except:
            raise Exception("Error removing deleted member's group")
    session.commit()

def get_member_by_id(member_id):
    member = session.query(Member).filter_by(id=member_id).first()
    return member

def get_group_members(group_id):
    members = session.query(Member).filter_by(group_id=group_id).all()
    return members


#group related
def get_group_by_name(guild_id, group_name):
    group = session.query(Group).filter_by(name=group_name, guild_id=guild_id).first()
    return group

def get_group_by_id(group_id):
    group = session.query(Group).filter_by(id=group_id).first()
    return group

def get_active_group(user_id):
    user = get_or_create_user(user_id)
    member_id = get_active_id(user_id)
    if member_id == -1:
        return
    member = get_member_by_id(member_id)
    return session.query(Group).filter_by(id=member.group_id).first()

def get_groups_by_guild(guild_id):
    groups = session.query(Group).filter_by(guild_id=guild_id).all()
    return groups

def create_group(group_name, creator_id, guild_id):
    get_or_create_user(creator_id)
    group = Group(name=group_name, guild_id=guild_id)
    
    session.add(group)
    session.commit()#necessary to get group id
    create_member(creator_id, group.id)
    session.commit()
    return group

def delete_group(group_id):
    group = session.query(Group).filter_by(id=group_id).first()
    session.delete(group)

    members = get_group_members(group_id)
    for member in members:
        session.delete(member)
    session.commit()


#active member related
def set_active_id(user_id, member_id):
    user = get_or_create_user(user_id)
    user.active_member_id = member_id
    session.commit()

def get_active_id(user_id):
    user = get_or_create_user(user_id)
    member_id = user.active_member_id
    return member_id

def get_active_member(user_id):
    user = get_or_create_user(user_id)
    member_id = get_active_id(user_id)
    member = get_member_by_id(member_id) 
    return member

def get_active_content(user_id):
    user = get_or_create_user(user_id)
    active = user.active_member_id
    if active != -1:
        member = session.query(Member).filter_by(id=active).first()
        if not member:
            raise Exception("User's active does not correspond to a member")
        return json.loads(member.content)
    else:
        return

def set_active_content(user_id, content_dict):
    user = get_or_create_user(user_id)
    active = user.active_member_id
    if active != -1:
        member = session.query(Member).filter_by(id=user.active_member_id).first()
        member.content = json.dumps(content_dict)
        session.commit()
    else:
        return


