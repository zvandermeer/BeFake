import json
import discord

async def memberJoin(member, client, dbConnection, dbCursor):
    params = (member.id, member.guild.id)

    dbCursor.execute('''SELECT Personal_Channel FROM USERS WHERE User_ID = ? AND Guild = ?''', params)

    foundUser = dbCursor.fetchall()

    if len(foundUser) == 0:
        overwrites = {
            member.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            member: discord.PermissionOverwrite(view_channel=True)
        }

        channel = await member.guild.create_text_channel(f"{member.display_name}-befake", overwrites=overwrites)

        params = (member.id,
                  member.guild.id,
                  channel.id,
                  member.name,
                  member.display_name)

        dbCursor.execute('''INSERT INTO USERS (User_ID, Guild, Personal_Channel, Username, Display_Name) VALUES (?, ?, ?, ?, ?)''', params)

        dbConnection.commit()

    elif len(foundUser) == 1:
        channel = client.get_channel(foundUser[0][0])

        await channel.set_permissions(member, view_channel=True)
    
    else:
        print("ERROR: Duplicate users matching criteria found in database, an unknown problem has occurred.")