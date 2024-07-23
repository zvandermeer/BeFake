import asyncio
import datetime
from discord.ext import tasks
import time
import random

if time.localtime().tm_isdst:
    notificationResetTime = datetime.time(hour=4, minute=0)
else:
    notificationResetTime = datetime.time(hour=5, minute=0)

async def triggerNotification(groupId, client, dbCursor):
    dbCursor.execute('''SELECT MEMBERS.Personalized_Message, USERS.Personal_Channel, GROUPS.Notification_Message FROM MEMBERS LEFT JOIN USERS ON MEMBERS.User_ID = USERS.id LEFT JOIN GROUPS ON MEMBERS.Group_ID = GROUPS.id WHERE Group_ID = ?''', (groupId,))

    for member in dbCursor.fetchall():
        message = member[0]

        if not member[0]:
            message = member[2]

        channel = client.get_channel(member[1])

        await channel.send(message)

async def scheduleNotification(notificationTimestamp, groupId, client, dbConnection, dbCursor):
    now = datetime.datetime.now()
    notificationTime = datetime.datetime.fromtimestamp(notificationTimestamp)

    delta = (notificationTime - now).total_seconds()

    await asyncio.sleep(delta)

    await triggerNotification(groupId, client, dbCursor)

    dbCursor.execute('''UPDATE GROUPS SET Notification_Triggered = 1 WHERE id = ?''', (groupId,))

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

async def initializeNotification(client, dbConnection, dbCursor):
    resetNotificationSchedule.start(client, dbConnection, dbCursor)

    dbCursor.execute('''SELECT id, Notification_Time, Notification_Triggered FROM GROUPS''')

    for group in dbCursor.fetchall():

        lastNotification = datetime.datetime.fromtimestamp(group[1])
        now = datetime.datetime.now()

        if lastNotification.date() != now.date() or (not group[2] and lastNotification.time() < now.time() and now.time() < datetime.time(hour=22, minute=30)):
            notificationTimestamp = await resetNotification(group[0], dbConnection, dbCursor)
        else:
            notificationTimestamp = lastNotification.timestamp()

        await scheduleNotification(notificationTimestamp, group[0], client, dbConnection, dbCursor)

@tasks.loop(time=notificationResetTime)
async def resetNotificationSchedule(client, dbConnection, dbCursor):
    dbCursor.execute('''SELECT id, Notification_Time, Notification_Triggered FROM GROUPS''')

    for group in dbCursor.fetchall():
        notificationTimestamp = await resetNotification(group[0], dbConnection, dbCursor)
        await scheduleNotification(notificationTimestamp, group[0], client, dbConnection, dbCursor)