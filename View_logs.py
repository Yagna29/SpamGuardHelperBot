import sqlite3
import csv

conn = sqlite3.connect('spam_guard.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM spam_logs")
rows = cursor.fetchall()

with open("spam_logs.csv", "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["ID", "Username", "User ID", "Message", "Action", "Log Time"])
    writer.writerows(rows)

print("✅ Logs exported to spam_logs.csv")
conn.close()
