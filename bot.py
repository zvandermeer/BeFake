import sqlite3
import discord
import os

import notification
import registration

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

db_connection = sqlite3.connect('befake.sqlite3')

db_cursor = db_connection.cursor()

@client.event
async def on_ready():
    notificationTimestamp = await notification.initializeNotification()
    print(f'Bot logged in as {client.user}')
    await notification.scheduleNotification(notificationTimestamp)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$timer'):
        await notification.timer(message.channel)

    if message.content.lower().startswith("$resetnotification"):
        await notification.resetNotification(False)

    if message.content.startswith("$hello"):
        await message.channel.send("Hello!")

@client.event
async def on_member_join(member):
    await registration.memberJoin(member, client, db_connection, db_cursor)

client.run(os.environ["DISCORD_BOT_TOKEN"])