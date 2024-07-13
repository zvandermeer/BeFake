import discord
import notification
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

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
        notification.resetNotification(False)

    if message.content.startswith("$hello"):
        await message.channel.send("Hello!")

client.run(os.environ["DISCORD_BOT_TOKEN"])