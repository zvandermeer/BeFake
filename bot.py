import sqlite3
import discord
import os

import notification
import registration
import setup_db

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

if not os.path.isfile("befake.sqlite3"):
    setup_db.setup()

db_connection = sqlite3.connect('befake.sqlite3')

db_cursor = db_connection.cursor()

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

client.run(os.environ["DISCORD_BOT_TOKEN"])

db_connection.close()