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

async def scheduleNotification(notificationTimestamp, groupId, dbConnection, dbCursor):
    now = datetime.datetime.now()
    notificationTime = datetime.datetime.fromtimestamp(notificationTimestamp)

    delta = (notificationTime - now).total_seconds()

    await asyncio.sleep(delta)

    # Fire off notification here

    dbCursor.execute('''UPDATE GROUPS SET Notification_Triggered 1 WHERE id = ?''', (groupId))

    dbConnection.commit()

async def resetNotification(groupId, dbConnection, dbCursor):
    now = datetime.datetime.now()
    if now < datetime.datetime(year=now.year, month=now.month, day=now.day, hour=8, minute=30):
        notificationStartTime = datetime.datetime(year=now.year, month=now.month, day=now.day, hour=8, minute=30)
    else:
        notificationStartTime = datetime.datetime(year=now.year, month=now.month, day=now.day, hour=now.hour, minute=now.minute, second=now.second)
        
    delta = (datetime.datetime(year=now.year, month=now.month, day=now.day, hour=22, minute=30) - notificationStartTime).total_seconds()
    notificationTimestamp = int((notificationStartTime + datetime.timedelta(seconds=random.randrange(60, delta))).timestamp())

    dbCursor.execute('''UPDATE GROUPS SET Notification_Time = ?, Notification_Triggered = 0 WHERE id = ?''', (notificationTimestamp, groupId))

    dbConnection.commit()

    return notificationTimestamp

async def initializeNotification(dbConnection, dbCursor):
    resetNotificationSchedule.start(dbConnection, dbCursor)

    dbCursor.execute('''SELECT id, Notification_Time, Notification_Triggered FROM GROUPS''')

    for group in dbCursor.fetchall():

        lastNotification = datetime.datetime.fromtimestamp(group[1])
        now = datetime.datetime.now()

        if lastNotification.date() != now.date() or (not group[2] and lastNotification.time() < now.time() and now.time() < datetime.time(hour=22, minute=30)):
            notificationTimestamp = await resetNotification(group[0], dbConnection, dbCursor)
        else:
            notificationTimestamp = lastNotification.timestamp()

        await scheduleNotification(notificationTimestamp, group[0], dbConnection, dbCursor)

@tasks.loop(time=notificationResetTime)
async def resetNotificationSchedule(dbConnection, dbCursor):
    dbCursor.execute('''SELECT id, Notification_Time, Notification_Triggered FROM GROUPS''')

    for group in dbCursor.fetchall():
        notificationTimestamp = await resetNotification(group[0], dbConnection, dbCursor)
        await scheduleNotification(notificationTimestamp, group[0], dbConnection, dbCursor)