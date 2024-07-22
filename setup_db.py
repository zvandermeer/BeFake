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
                        Notification_Configuration CHAR(255) NOT NULL,
                        Notification_Message CHAR(255) NOT NULL,
                        Notification_Time INTEGER NOT NULL,
                        Notification_Triggered BOOL NOT NULL
                );  """

    db_cursor.execute(group_table)

    db_cursor.execute("DROP TABLE IF EXISTS MEMBERS")

    member_table = """  CREATE TABLE MEMBERS (
                        id INTEGER PRIMARY KEY,
                        Group_ID int NOT NULL,
                        User_ID BIGINT NOT NULL,
                        FOREIGN KEY (Group_ID) REFERENCES GROUPS(id),
                        FOREIGN KEY (USER_ID) REFERENCES USERS(id)
                );  """

    db_cursor.execute(member_table)

    print("Database has been configured.")

    db_connection.close()

if __name__ == "__main__":
    setup()