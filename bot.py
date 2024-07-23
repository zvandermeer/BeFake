import os
import sqlite3

import discord
from discord.ext import commands
from discord.ui import Select, View

import notification
import registration
import groups
import setup_db

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client=commands.Bot(intents=intents, test_guilds=[1261466340003287134])

if not os.path.isfile("realcord.sqlite3"):
    setup_db.setup()

db_connection = sqlite3.connect('realcord.sqlite3')

db_cursor = db_connection.cursor()

class AddGroupSelectMenu(Select):
    def __init__(self, newMember, groups):

        self.groupOptions = []
        self.newMember = newMember

        for group in groups:
            self.groupOptions.append(discord.SelectOption(
                label=group[1],
                description=f"Add {newMember.display_name} to \"{group[1]}\"",
                value=str(group[0])
            ))

        super(AddGroupSelectMenu, self).__init__(
            placeholder=f"Select a group:",
            min_values=1,
            max_values=1,
            options=self.groupOptions
        )

    async def callback(self, interaction: discord.Interaction):
        await groups.addToGroup(client, self.newMember, self.values[0], db_connection, db_cursor)
        await interaction.response.edit_message(content="Done!", view=None)

class AddGroupSelectView(View):
    def __init__(self, newMember, groups):
        super(AddGroupSelectView, self).__init__()
        self.menu = AddGroupSelectMenu(newMember, groups)
        self.add_item(self.menu)

@client.event
async def on_ready():
    print(f'Bot logged in as {client.user}')
    await notification.initializeNotification(client, db_connection, db_cursor)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$timer'):
        await notification.timer(message.channel)

    if message.content.startswith("$hello"):
        await message.channel.send("Hello!")

@client.event
async def on_member_join(member):
    await registration.memberJoin(member, client, db_connection, db_cursor)

@client.slash_command(description="Creates a new RealCord group")
async def create_new_group(ctx: discord.ApplicationContext, name: discord.Option(discord.SlashCommandOptionType.string)):
    await groups.createGroup(ctx.author, name, db_connection, db_cursor)

# TODO: Reorganize this to not be in bot.py
@client.slash_command(description="Adds a new user to a RealCord group")
async def add_user_to_group(ctx: discord.ApplicationContext, member: discord.Option(discord.SlashCommandOptionType.user)):

    db_cursor.execute('''SELECT id FROM USERS WHERE User_ID = ? AND Guild = ?''', (ctx.author.id, ctx.guild.id))

    userId = db_cursor.fetchall()[0][0]

    db_cursor.execute('''SELECT MEMBERS.Group_ID, GROUPS.Name FROM MEMBERS LEFT JOIN GROUPS ON MEMBERS.Group_ID = GROUPS.id WHERE User_ID = ?''', (userId,))

    groups = db_cursor.fetchall() # Will need to change this, select menus have a limit of 25 entries

    await ctx.respond(f"Select a group to add {member.display_name} to:", ephemeral=True, view=AddGroupSelectView(member, groups))

@client.user_command(name="Add user to RealCord group", guild_ids=[1261466340003287134])  # create a user command for the supplied guilds
async def account_creation_date(ctx, member: discord.Member):  # user commands return the member

    db_cursor.execute('''SELECT id FROM USERS WHERE User_ID = ? AND Guild = ?''', (ctx.author.id, ctx.guild.id))

    userId = db_cursor.fetchall()[0][0]

    db_cursor.execute('''SELECT MEMBERS.Group_ID, GROUPS.Name FROM MEMBERS LEFT JOIN GROUPS ON MEMBERS.Group_ID = GROUPS.id WHERE User_ID = ?''', (userId,))

    groups = db_cursor.fetchall() # Will need to change this, select menus have a limit of 25 entries

    await ctx.respond(f"Select a group to add {member.display_name} to:", ephemeral=True, view=AddGroupSelectView(member, groups))

client.run(os.environ["DISCORD_BOT_TOKEN"])

db_connection.close()