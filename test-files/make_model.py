import pandas as pd
import sqlite3

# Connecting to SQLite Database
connection = sqlite3.connect("data.db")
# cursor
crsr = connection.cursor()

sql = "SELECT * FROM Clicks"
clicks = connection.execute(sql).fetchall()

# Convert results to DataFrame
clicks_df = pd.DataFrame(clicks)

# Print out first 5 rows
print(clicks_df.head())
