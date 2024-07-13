import asyncio
import datetime
from discord.ext import tasks
import time
import json
import random

if time.localtime().tm_isdst:
    notificationResetTime = datetime.time(hour=4, minute=0)
else:
    notificationResetTime = datetime.time(hour=5, minute=0)

async def timer(channel):
    print("we are timing")

    count = 10
    message = await channel.send(str(count))
    while count > 1:
        await asyncio.sleep(1)
        count -= 1
        await message.edit(content=str(count))
    
    print("done")

async def scheduleNotification(notificationTimestamp):
    now = datetime.datetime.now()
    notificationTime = datetime.datetime.fromtimestamp(notificationTimestamp)

    delta = (notificationTime - now).total_seconds()

    await asyncio.sleep(delta)

    # Fire off notification here

    notificationInfo = {
        "timestamp": notificationTimestamp,
        "triggered": True
    }

    with open('notification.json', 'w') as fp:
        json.dump(notificationInfo, fp)

async def resetNotification(scheduled):
    now = datetime.datetime.now()
    if scheduled:
        notificationStartTime = datetime.datetime(year=now.year, month=now.month, day=now.day, hour=8, minute=30)
    else:
        notificationStartTime = datetime.datetime(year=now.year, month=now.month, day=now.day, hour=now.hour, minute=now.minute, second=now.second)
        
    delta = (datetime.datetime(year=now.year, month=now.month, day=now.day, hour=22, minute=30) - notificationStartTime).total_seconds()
    notificationTimestamp = (notificationStartTime + datetime.timedelta(seconds=random.randrange(60, delta))).timestamp()

    notificationInfo = {
        "timestamp": notificationTimestamp,
        "triggered": False
    }

    with open('notification.json', 'w') as fp:
        json.dump(notificationInfo, fp)

    return notificationTimestamp

async def initializeNotification():
    resetNotificationSchedule.start()

    with open("notification.json", "r") as fp:
        notificationInfo = json.load(fp)

    lastNotification = datetime.datetime.fromtimestamp(notificationInfo["timestamp"])
    now = datetime.datetime.now()

    if lastNotification.date() != now.date() or (not notificationInfo["triggered"] and lastNotification.time() < now.time() and now.time() < datetime.time(hour=22, minute=30)):
        notificationTimestamp = await resetNotification(False)
    else:
        notificationTimestamp = lastNotification.timestamp()

    return notificationTimestamp

@tasks.loop(time=notificationResetTime)
async def resetNotificationSchedule():
    notificationTimestamp = await resetNotification(True)
    await scheduleNotification(notificationTimestamp)