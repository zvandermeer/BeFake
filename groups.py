import discord
import notification

async def createGroup(member, groupName, dbConnection, dbCursor):
    overwrites = {
            member.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            member: discord.PermissionOverwrite(view_channel=True)
        }

    channel = await member.guild.create_text_channel(f"{groupName}", overwrites=overwrites)

    params = (groupName, member.guild.id, channel.id, "It's time to BeFake!")

    dbCursor.execute('''INSERT INTO GROUPS (Name, Guild, Shared_Channel, Notification_Message) VALUES (?, ?, ?, ?)''', params)

    groupId = dbCursor.lastrowid

    print(member.id)

    dbCursor.execute('''SELECT id FROM USERS WHERE User_ID = ?''', (member.id,))

    userId = dbCursor.fetchall()[0][0]

    dbCursor.execute('''INSERT INTO MEMBERS (Group_ID, User_ID) VALUES (?, ?)''', (groupId, userId))

    dbConnection.commit()

    await notification.resetNotification(groupId, dbConnection, dbCursor)
    