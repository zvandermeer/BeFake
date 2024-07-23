import sqlite3

def setup():

    db_connection = sqlite3.connect('befake.sqlite3')

    db_cursor = db_connection.cursor()

    db_cursor.execute("DROP TABLE IF EXISTS USERS")

    user_table = """    CREATE TABLE USERS (
                        id INTEGER PRIMARY KEY,
                        User_ID BIGINT NOT NULL,
                        Guild BIGINT NOT NULL,
                        Personal_Channel BIGINT NOT NULL,
                        Username CHAR(32) NOT NULL,
                        Display_Name CHAR(32) NOT NULL,
                        Real_Name CHAR(32)
                );  """

    db_cursor.execute(user_table)

    db_cursor.execute("DROP TABLE IF EXISTS GROUPS")

    group_table = """   CREATE TABLE GROUPS (
                        id INTEGER PRIMARY KEY,
                        Name CHAR(255) NOT NULL,
                        Guild BIGINT NOT NULL,
                        Shared_Channel BIGINT NOT NULL,
                        Notification_Message CHAR(255) NOT NULL,
                        Notification_Time INTEGER,
                        Notification_Triggered BOOL
                );  """

    db_cursor.execute(group_table)

    db_cursor.execute("DROP TABLE IF EXISTS MEMBERS")

    member_table = """  CREATE TABLE MEMBERS (
                        id INTEGER PRIMARY KEY,
                        Group_ID int NOT NULL,
                        User_ID BIGINT NOT NULL,
                        Personalized_Message CHAR(255),
                        FOREIGN KEY (Group_ID) REFERENCES GROUPS(id),
                        FOREIGN KEY (USER_ID) REFERENCES USERS(id)
                );  """

    db_cursor.execute(member_table)

    print("Database has been configured")

    db_connection.close()

def generateSampleData():
    db_connection = sqlite3.connect('befake.sqlite3')

    db_cursor = db_connection.cursor()

    db_cursor.execute('''INSERT INTO USERS (id, User_ID, Guild, Personal_Channel, Username, Display_Name, Real_Name) VALUES (1, 309771442763857931, 1261466340003287134, 1265050555806646386, "cosmosstarlightt", "CosmosStarlightt", "Zoey")''')
    db_cursor.execute('''INSERT INTO GROUPS (id, Name, Guild, Shared_Channel, Notification_Message, Notification_Time, Notification_Triggered) VALUES (1, "Example Group", 1261466340003287134, 1265051953063530609, "Time to befake!", 1721682324, 0)''')
    db_cursor.execute('''INSERT INTO MEMBERS (id, Group_ID, User_ID, Personalized_Message) VALUES (1, 1, 1, "Time to befake!")''')

    db_connection.commit()

    print("Sample data has been generated")

    db_connection.close()

if __name__ == "__main__":
    setup()
    generateSampleData()