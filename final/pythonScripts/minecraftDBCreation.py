# Written by Nathan Lin and Philson Wong
# REQUIRES CSV FILES TO BE IN THE SAME DIRECTORY AS THIS FILE
# MAY NEED TO CHANGE THE DBNAME, USER AND PASSWORD VALUES
import psycopg2
import pprint
import csv

# Connect to an existing database
#conn = psycopg2.connect("dbname=test user=philsonw host=/tmp/")
conn = psycopg2.connect("dbname='postgres' user='postgres' password='password'")
# Open a cursor to perform database operations
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS Vehicle;")
cur.execute("DROP TABLE IF EXISTS Perv;")
cur.execute("DROP TABLE IF EXISTS EIA_t;")
cur.execute("DROP TABLE IF EXISTS EIA_e;")
cur.execute("DROP TABLE IF EXISTS Day;")
cur.execute("DROP TABLE IF EXISTS EIA_m;")
cur.execute("DROP TABLE IF EXISTS Minecraft;")


# Execute a command: this creates a new table
#cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")

# Pass data to fill a query placeholders and let Psycopg perform
# the correct conversion (no more SQL injections!)
#cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)",(100, "abc'def"))

# Query the database and obtain data as Python objects
#cur.execute("SELECT * FROM test;")
#cur.fetchone()
#(1, 100, "abc'def")

#day = open('DAYV2PUB.CSV')
#csv_day = csv.reader(day)

#hhv = open('HHV2PUB.CSV')
#csv_hhv = csv.reader(hhv)

#perv = open('PERV2PUB.CSV')
#csv_perv = csv.reader(perv)

#veh = open('VEHV2PUB.CSV')
#csv_veh = csv.reader(veh)

#eia_t = open('EIA_CO2_Transportation_2014.csv')
#csv_t = csv.reader(eia_t)

#eia_e = open('EIA_CO2_Electric_2014.csv')
#csv_e = csv.reader(eia_e)

#eia_m = open('EIA_MkWh_2014.csv')
#csv_m = csv.reader(eia_m)

mine = open('vedatapak_full.csv')
csv_minecraft = csv.reader(mine)


def getNum(csvFile, attrName):
	csvFile.seek(0)
	stringparse=csvFile.readline()
	stringparse=stringparse.strip()
	find=stringparse.split(",")
	count = 0
	found = False
	for i in find:
		if i == attrName:
			found = True
			break
		count = count + 1
	if found:
		return count
	else:
		return -1

m_start = 0
m_stop = 1
m_server = 2
m_playerA = 3
m_playerB = 4
m_key = 5
m_meta = 6
m_count = 7

cur.execute("CREATE TABLE Minecraft(START_T INT, STOP_T INT, SERVER_ID TEXT, PLAYER_A TEXT, PLAYER_B TEXT, KEY TEXT, META TEXT, COUNT REAL);")
#firstline = True
for row in csv_minecraft:
#	if firstline:
#		firstline = False
#		continue
	cur.execute("INSERT INTO Minecraft VALUES (%s, %s, %s, %s, %s, %s, %s, %s);", (int(row[m_start]), int(row[m_stop]), (row[m_server]), (row[m_playerA]), (row[m_playerB]), (row[m_key]), (row[m_meta]), (row[m_count]) ))

# Make the changes to the database persistent
conn.commit()

cur.execute("SELECT DISTINCT META FROM MINECRAFT;")
pprint.pprint(cur.fetchall())
print "\n"

'''
# This adds up all the TRPMILES per specific person (HOUSEID and PERSONID are keys and unique), then checks if they have traveled less than 5, 10, ..., 100 miles
print "3a:"
for i in range(5,101,5):
		print i
		cur.execute("SELECT COUNT(*)::FLOAT*10/(SELECT COUNT(DISTINCT(HOUSEID,PERSONID)) FROM Day) \
			FROM (SELECT SUM(TRPMILES) AS TRPMILE FROM Day GROUP BY HOUSEID, PERSONID) tot WHERE TRPMILE < %s;",[i])
		pprint.pprint(cur.fetchall())
		print "\n"

# This finds the average MPG of all trips under 5, 10, ..., 100 miles for VEHID >= 1
print "3b:"
for i in range(5, 101, 5):
		print i
		cur.execute("SELECT SUM(full_list.TRPMILES)/SUM(full_list.TRPMILES/full_list.EPATMPG) as result \
			FROM (Day NATURAL JOIN Vehicle) full_list WHERE VEHID >= 1 AND TRPMILES < %s", [i])
		pprint.pprint(cur.fetchall())
		print "\n"

# This does something silly
print "3c:"
cur.execute("SELECT YYYYMM, (SUM(full_list.TRPMILES/full_list.EPATMPG)*0.008887*.000001*30*100*(117538000/COUNT(DISTINCT(HOUSEID))))::FLOAT/Value AS result \
	FROM (SELECT msn, YYYYMM, value FROM EIA_t WHERE msn = 'TEACEUS') category, \
	(Day NATURAL JOIN Vehicle) full_list WHERE category.YYYYMM >= 200803 AND category.YYYYMM <= 200904 AND category.YYYYMM <> 200813 AND full_list.TDAYDATE = category.YYYYMM \
	GROUP BY YYYYMM, Value ORDER BY YYYYMM;")
pprint.pprint(cur.fetchall())
print "\n"

print "3d:"

for i in range(20,61,20):
	print i
	cur.execute("SELECT alt.YYYYMM, (SUM(full_list.TRPMILES/full_list.EPATMPG)*0.008887*(117538000/COUNT(DISTINCT(HOUSEID))))::FLOAT - altco2 AS result \
		FROM (SELECT gas.YYYYMM, tot_kwH_co2 + tot_gas_co2 AS altco2 FROM (SELECT YYYYMM, SUM(gallons)*0.008887 as tot_gas_co2\
		FROM(SELECT (TRIPMILE - %s) * 1/(EPATMPG) AS gallons, YYYYMM \
		FROM (SELECT SUM(TRPMILES) AS TRIPMILE, EPATMPG, TDAYDATE as YYYYMM FROM (VEHICLE NATURAL JOIN DAY) GROUP BY HOUSEID, VEHID, EPATMPG, YYYYMM) d1\
		WHERE TRIPMILE > %s GROUP BY YYYYMM, EPATMPG, TRIPMILE) dd GROUP BY YYYYMM ORDER BY YYYYMM) gas, (SELECT moreThanRange.yr AS YYYYMM, (lessThanRange.lkwH + moreThanRange.lkwH)*rat.ratio AS tot_kwH_co2 \
		FROM (SELECT co2_total.YYYYMM AS YYYYMM, co2_total.Value::float/electric_total.Value::float AS ratio \
			FROM (SELECT Value,YYYYMM FROM EIA_e WHERE YYYYMM >= 200803 AND YYYYMM <= 200904 AND MSN = 'TXEIEUS') co2_total, \
				(SELECT Value,YYYYMM FROM EIA_m WHERE YYYYMM >= 200803 AND YYYYMM <= 200904 AND MSN = 'ELETPUS') electric_total \
			WHERE co2_total.YYYYMM = electric_total.YYYYMM\
			ORDER BY co2_total.YYYYMM) rat,\
		(SELECT SUM(kwH) AS lkwH, YYYYMM AS yr\
		FROM (SELECT %s * 1/(BatEff) AS kwH, YYYYMM \
		FROM (SELECT SUM(TRPMILES) AS TRIPMILE, EPATMPG * 0.090634441 AS BatEff, TDAYDATE as YYYYMM FROM (VEHICLE NATURAL JOIN DAY) full_list GROUP BY HOUSEID, VEHID, EPATMPG, YYYYMM) d1\
		WHERE TRIPMILE >%s GROUP BY YYYYMM, BatEff, TRIPMILE) dd GROUP BY YYYYMM) moreThanRange, \
		(SELECT SUM(kwH) AS lkwH, YYYYMM AS yr\
		FROM (SELECT TRIPMILE * 1/(BatEff) AS kwH, YYYYMM \
		FROM (SELECT SUM(TRPMILES) AS TRIPMILE, EPATMPG * 0.090634441 AS BatEff, TDAYDATE as YYYYMM FROM (VEHICLE NATURAL JOIN DAY) full_list GROUP BY HOUSEID, VEHID, EPATMPG, YYYYMM) d1\
		WHERE TRIPMILE <=%s GROUP BY YYYYMM, BatEff, TRIPMILE) dd GROUP BY YYYYMM) lessThanRange\
		WHERE moreThanRange.yr = lessThanRange.yr AND moreThanRange.yr = rat.YYYYMM \
		ORDER BY YYYYMM) kwH \
		WHERE gas.YYYYMM = kwH.YYYYMM ORDER BY gas.YYYYMM) alt, (SELECT msn, YYYYMM, value FROM EIA_t WHERE msn = 'TEACEUS') category, \
		(Day NATURAL JOIN Vehicle) full_list WHERE category.YYYYMM >= 200803 AND category.YYYYMM <= 200904 AND category.YYYYMM <> 200813 AND alt.YYYYMM = category.YYYYMM AND full_list.TDAYDATE = category.YYYYMM \
		GROUP BY alt.YYYYMM, altco2, Value ORDER BY alt.YYYYMM;", (i,i,i,i,i))

	pprint.pprint(cur.fetchall())
	print "\n"
'''
# Close communication with the database
cur.close()
conn.close()

