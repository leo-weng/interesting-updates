import sqlite3
import praw

# input_file = open('allsubreddits.txt','r')
# output_file = open('testquery.txt','w')

# for lines in range(50):
#     line = input_file.readline()
#     output_file.write(line)
# with open('./allsubreddits.txt') as input_file:
#     sql = "BEGIN TRANSACTION;"
#     output_file.write(sql)
#
#     for cnt, line in enumerate(input_file):
#         line = line.strip()
#         sub = line[25:-1]
#         sql = "INSERT INTO Subreddits VALUES(" + str(cnt+1) + ", \"" + sub + "\");\n"
#         output_file.write(sql)
#         if cnt == 50:
#             break;
connection = sqlite3.connect("data.db")
# cursor
crsr = connection.cursor()

# sql = """
#         SELECT clicked_URL, COUNT(clicked_URL) AS num_clicked, SUM(time_passed)
#         FROM (SELECT * FROM Clicks LIMIT 10000000)
#         WHERE clicked_URL <= 1082444
#         GROUP BY clicked_URL
#         ORDER BY num_clicked DESC;
#     """
# for row in crsr.execute(sql):
#     writeRow = " ".join([str(i) for i in row])
#     writeRow = writeRow + "\n"
#     output_file.write(writeRow)

# sql = "SELECT * FROM Subreddits LIMIT 10"
# count = 0
# for row in crsr.execute(sql):
#     writeRow = " ".join([str(i) for i in row])
#     writeRow = writeRow + "\n"
#     output_file.write(writeRow)
#     count = count + 1
#     if count == 5000:
#         break;
sql = """
        SELECT url, (num_clicked/1)*(total_time/100)(log(num_subs)) AS weighted
        FROM (
            SELECT s.id, s.url AS url, COUNT(c.clicked_URL) AS num_clicked,
                SUM(c.time_passed) AS total_time, s.num_subs AS num_subs
            FROM (SELECT * FROM Clicks LIMIT 100000) AS c
            LEFT JOIN Subreddits AS s
            ON c.clicked_URL = s.id
            WHERE c.clicked_URL <= 1082444
            GROUP BY s.id
        )
        ORDER BY weighted DESC;
    """
# for row in crsr.execute(sql):
#     writeRow = " ".join([str(i) for i in row])
#     writeRow = writeRow + "\n"
#     output_file.write(writeRow)

# sql = "SELECT * FROM Subreddits LIMIT 100;"
for row in crsr.execute(sql):
    print(row)

connection.commit()
connection.close()

# def get_reddit():
#     return praw.Reddit(
#         client_id='Wp_rdHPW2jlcpQ',
#         client_secret='K3bSZlK122MvVyJ5lQF_JuSX7FM',
#         grant_type='client_credentials',
#         user_agent='mytestscript/1.0'
#     )
#
# def run():
#     reddit = get_reddit()
#     try:
#         num_subs = reddit.subreddit('kokok').subscribers
#     except:
#         num_subs = 0
#     print (num_subs)
#
# if __name__ == '__main__':
#     run()
