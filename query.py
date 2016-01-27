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

for i in range(11,15):
	for j in range(0,8):
		if j == 0:
			keyVal = "Logins"
		elif j == 1:
			keyVal = "KilledBy"
		elif j == 2:
			keyVal = "Chat"
		elif j == 3:
			keyVal = "BlockPlace"
		elif j == 4:
			keyVal = "Death"
		elif j == 5:
			keyVal = "BlockBreak"
		elif j == 6:
			keyVal = "Kicks"
		elif j == 7:
			keyVal = "CraftedItems"
		cur.execute("select sum(count) from minecraft where server_id='Server %s' AND key=%s;", (int(i), keyVal))
		print i
		print keyVal
		pprint.pprint(cur.fetchall())
		print "\n"

#cur.execute("\COPY (SELECT * FROM Minecraft WHERE key=' KilledBy') To 'C:\KilledBy.csv' With CSV;")
#with open('KilledBy.csv', 'w') as f:
#	writer = csv.writer(f, delimiter=",")
#	
# Close communication with the database
cur.close()
conn.close()

#\copy (select start_t, stop_t, server_id, count from minecraft where key='KilledBy' ORDER BY start_t) To 'C:\serverkills.csv' With CSV;

#select count(*) from (select distinct start_t from minecraft where minecraft.key='Kicks') as test;

#\copy (SELECT DISTINCT start_t, server_id, sum(count) from minecraft where key='KilledBy' GROUP BY start_t, server_id ORDER BY start_t) to 'C:\newkilltest.csv' With CSV;