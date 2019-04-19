# Python code to demonstrate table creation and
# insertions with SQL

# importing module
import sqlite3

def create_table():
    # connecting to the database
    connection = sqlite3.connect("data.db")
    # cursor
    crsr = connection.cursor()

    sql = "DROP TABLE IF EXISTS Clicks;"
    crsr.execute(sql)
    sql = "DROP TABLE IF EXISTS Queries;"
    crsr.execute(sql)
    sql = "DROP TABLE IF EXISTS URL_IDs;"
    crsr.execute(sql)

    # SQL command to create a table in the database
    sql = """ CREATE TABLE Clicks (
        count           INT         NOT NULL,
        session_id      INT         NOT NULL,
        time_passed     INT         NOT NULL,
        label           INT         NOT NULL,
        clicked_URL     INT         NOT NULL,
        PRIMARY KEY (count, session_id, time_passed)
        );"""
    crsr.execute(sql)

    sql = """ CREATE TABLE Queries (
        count           INT         NOT NULL,
        session_id      INT         NOT NULL,
        time_passed     INT         NOT NULL,
        query_id        INT         NOT NULL,
        region_id       INT         NOT NULL,
        PRIMARY KEY (count, session_id, time_passed)
        );"""
    crsr.execute(sql)

    sql = """ CREATE TABLE URL_IDs (
        count           INT         NOT NULL,
        session_id      INT         NOT NULL,
        time_passed     INT         NOT NULL,
        url_label       INT         NOT NULL,
        url_id          CHAR        NOT NULL,
        PRIMARY KEY (count, session_id, time_passed),
        FOREIGN KEY (count) REFERENCES Queries(count),
        FOREIGN KEY (session_id) REFERENCES Queries(session_id),
        FOREIGN KEY (time_passed) REFERENCES Queries(time_passed)
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

    with open('./data/train/train.txt') as input_file:
        sql = "BEGIN TRANSACTION;"
        crsr.execute(sql)

        for cnt, line in enumerate(input_file):
            # if (cnt % 500 == 0):

            # line = input_file.readline()
            line = line.strip()
            data = line.split("\t")
            sql = ""
            sql2 = ""
            urls = ""
            isQuery = True
            isMorT = False
            for i in range(len(data)):
                if i == 0 or i == 1 or i == 3:
                    sql = sql + "\"" + data[i] + "\", "
                    sql2 = sql2 + "\"" + data[i] + "\", "
                elif i == 2:
                    # print(data[i])
                    if data[i] == "C":
                        sql = "INSERT INTO Clicks VALUES(\"" + str(cnt%500) + "\", " + sql
                        isQuery = False
                    elif data[i] == "Q":
                        sql = "INSERT INTO Queries VALUES(\"" + str(cnt%500) + "\", " + sql
                        sql2 = "INSERT INTO URL_IDs VALUES(\"" + str(cnt%500) + "\", " + sql2
                    else:
                        isMorT = True
                        break
                elif i == 4:
                    sql = sql + "\"" + data[i] + "\");"
                else:
                    urls = urls + data[i] + " "
            if isQuery:
                sql2 = sql2 + "\"" + urls[:-1] + "\");"

            if not isMorT:
                crsr.execute(sql)
                if isQuery:
                    crsr.execute(sql2)
            if (cnt % 10000 == 9999):
                print ("adding record " + str(cnt) + "...")
            # if cnt == 101:
            #     break;
        print ("ending transaction" + "...")
        sql = "END TRANSACTION;"
        crsr.execute(sql)
    connection.commit()
    connection.close()

if __name__ == '__main__':
    create_table()
    insert_data()
