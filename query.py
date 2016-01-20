import psycopg2
import pprint
import csv

conn = psycopg2.connect("dbname='postgres' user='postgres' password='password'")
# Open a cursor to perform database operations
cur = conn.cursor()

m_start = 0
m_stop = 1
m_server = 2
m_playerA = 3
m_playerB = 4
m_key = 5
m_meta = 6
m_count = 7

#cur.execute("SELECT DISTINCT key FROM Minecraft;")
#pprint.pprint(cur.fetchall())
#print "\n"

cur.execute("\COPY (SELECT * FROM Minecraft WHERE key=' KilledBy') To 'C:\KilledBy.csv' With CSV;")
#with open('KilledBy.csv', 'w') as f:
#	writer = csv.writer(f, delimiter=",")
#	
# Close communication with the database
cur.close()
conn.close()