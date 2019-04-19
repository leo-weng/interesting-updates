import sqlite3


def get_top_interests():
    output_file = open('testquery.txt','w')

    connection = sqlite3.connect("data.db")
    # cursor
    crsr = connection.cursor()

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
            ORDER BY weighted DESC
            LIMIT 10;
        """
    interests = []
    for row in crsr.execute(sql):
        interests.append(row[0])
    return interests

    # d = {'total_times': total_times, 'total_clicked': total_clicked}
    # df = pd.DataFrame(data=d)
    # # for i in range(len(total_clicked)):
    # #     output_file.write(total_clicked[i] + " " + total_times[i] + "\n")
    # return df


def run():
    get_top_interests()

if __name__ == '__main__':
    run()
