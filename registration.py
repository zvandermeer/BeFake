import json
import discord

async def memberJoin(member, client):
    with open("users.json", "r") as fp:
        userDB = json.load(fp)

    if not str(member.id) in userDB["users"].keys():
        overwrites = {
            member.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            member: discord.PermissionOverwrite(view_channel=True)
        }

        channel = await member.guild.create_text_channel(f"{member.display_name}-befake", overwrites=overwrites)

        userDB["users"][member.id] = {
            "username": member.display_name,
            "real_name": "",
            "guild": member.guild.id,
            "personal_channel": channel.id,
            "groups": []
        }

        with open("users.json", "w") as fp:
            json.dump(userDB, fp)
    else:
        print(userDB["users"][str(member.id)]["personal_channel"])

        channel = client.get_channel(userDB["users"][str(member.id)]["personal_channel"])

        await channel.set_permissions(member, view_channel=True)