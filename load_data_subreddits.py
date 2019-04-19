# Python code to demonstrate table creation and
# insertions with SQL

# importing module
import sqlite3
import praw

def create_table():
    # connecting to the database
    connection = sqlite3.connect("data.db")
    # cursor
    crsr = connection.cursor()

    sql = "DROP TABLE IF EXISTS Subreddits;"
    crsr.execute(sql)

    # SQL command to create a table in the database
    sql = """ CREATE TABLE Subreddits (
        id              INT         NOT NULL    PRIMARY KEY,
        url             CHAR        NOT NULL
        );"""
    crsr.execute(sql)
    # To save the changes in the files. Never skip this.
    # If we skip this, nothing will be saved in the database.
    connection.commit()
    # close the connection
    connection.close()

def insert_data():
    # connecting to the database
    connection = sqlite3.connect("data.db")
    # cursor
    crsr = connection.cursor()

    # input_file = open('./train/train.txt','r')
    # output_file = open('output.txt','w')

    with open('./txt-files/allsubreddits.txt') as input_file:
        sql = "BEGIN TRANSACTION;"
        crsr.execute(sql)
        for cnt, line in enumerate(input_file):
            line = line.strip()
            sub = line[25:-1]
            sql = "INSERT INTO Subreddits VALUES(" + str(cnt+1) + ", \"" + sub + "\");"
            crsr.execute(sql)

        print ("ending transaction" + "...")
        sql = "END TRANSACTION;"
        crsr.execute(sql)
    connection.commit()
    connection.close()

def get_reddit():
    return praw.Reddit(
        client_id='Wp_rdHPW2jlcpQ',
        client_secret='K3bSZlK122MvVyJ5lQF_JuSX7FM',
        grant_type='client_credentials',
        user_agent='mytestscript/1.0'
    )

def add_subs():
    # connecting to the database
    connection = sqlite3.connect("data.db")
    # cursor
    crsr = connection.cursor()
    reddit = get_reddit()

    # sql = """ALTER TABLE Subreddits
    #         ADD num_subs    INT;"""
    # crsr.execute(sql)

    sql = """BEGIN TRANSACTION;"""
    crsr.execute(sql)
    sql = "SELECT id, url FROM Subreddits;"
    crsr.execute(sql)
    for row in crsr.fetchall():
        try:
            num_subs = reddit.subreddit(row[1]).subscribers
        except:
            num_subs = 0
        sql2 = "UPDATE Subreddits SET num_subs = " + str(num_subs) + " WHERE id = " + str(row[0]) + ";"
        crsr.execute(sql2)

    sql = "SELECT * FROM Subreddits LIMIT 1000;"
    for row in crsr.execute(sql):
        print(row)

    connection.commit()
    connection.close()

    num_subs = reddit.subreddit('leagueoflegends').subscribers

if __name__ == '__main__':
    # create_table()
    # insert_data()
    add_subs()
