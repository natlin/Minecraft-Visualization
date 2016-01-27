# Written by Nathan Lin and Philson Wong
# REQUIRES CSV FILES TO BE IN THE SAME DIRECTORY AS THIS FILE
# MAY NEED TO CHANGE THE DBNAME, USER AND PASSWORD VALUES
import psycopg2
import pprint
import csv

# Connect to an existing database
conn = psycopg2.connect("dbname=test user=philsonw password=")

# Open a cursor to perform database operations
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS Vehicle;")
cur.execute("DROP TABLE IF EXISTS Perv;")
cur.execute("DROP TABLE IF EXISTS EIA_t;")
cur.execute("DROP TABLE IF EXISTS EIA_e;")
cur.execute("DROP TABLE IF EXISTS Day;")
cur.execute("DROP TABLE IF EXISTS EIA_m;")


# Execute a command: this creates a new table
#cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")

# Pass data to fill a query placeholders and let Psycopg perform
# the correct conversion (no more SQL injections!)
#cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)",(100, "abc'def"))

# Query the database and obtain data as Python objects
#cur.execute("SELECT * FROM test;")
#cur.fetchone()
#(1, 100, "abc'def")

day = open('DAYV2PUB.CSV')
csv_day = csv.reader(day)

hhv = open('HHV2PUB.CSV')
csv_hhv = csv.reader(hhv)

#perv = open('PERV2PUB.CSV')
#csv_perv = csv.reader(perv)

veh = open('VEHV2PUB.CSV')
csv_veh = csv.reader(veh)

eia_t = open('EIA_CO2_Transportation_2014.csv')
csv_t = csv.reader(eia_t)

eia_e = open('EIA_CO2_Electric_2014.csv')
csv_e = csv.reader(eia_e)

eia_m = open('EIA_MkWh_2014.csv')
csv_m = csv.reader(eia_m)


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

veh_houseID = getNum(veh, 'HOUSEID')
veh_VEHID = getNum(veh, 'VEHID')
veh_EPATMPG = getNum(veh, 'EPATMPG')
veh_TDAYDATE = getNum(veh, 'TDAYDATE')

cur.execute("CREATE TABLE Vehicle(HOUSEID INT, VEHID INT, EPATMPG REAL, TDAYDATE INT);")
firstline = True
for row in csv_veh: # row reads in one row in csv file
	#content = (row[i] for i in included_cols)
	if firstline:
		firstline = False
		continue
	cur.execute("INSERT INTO Vehicle VALUES (%s, %s, %s, %s);", (int(row[veh_houseID]), int(row[veh_VEHID]), float(row[veh_EPATMPG]), int(row[veh_TDAYDATE])))

	#print row[0]

#cur.execute("CREATE TABLE Perv(HOUSEID INT);")

day_HOUSEID = getNum(day, 'HOUSEID')
day_PERSONID = getNum(day, 'PERSONID')
day_VEHID = getNum(day, 'VEHID')
day_TRPMILES = getNum(day, 'TRPMILES')
day_TDAYDATE = getNum(day, 'TDAYDATE')

cur.execute("CREATE TABLE Day(HOUSEID INT, PERSONID INT, VEHID INT, TRPMILES REAL, TDAYDATE INT);")
firstline = True
for row in csv_day:
	if firstline:
		firstline = False
		continue
	cur.execute("INSERT INTO Day VALUES (%s, %s, %s, %s, %s);", (int(row[day_HOUSEID]), int(row[day_PERSONID]), int(row[day_VEHID]), float(row[day_TRPMILES]), int(row[day_TDAYDATE])))

t_MSN = getNum(eia_t, 'MSN')
t_YYYYMM = getNum(eia_t, 'YYYYMM')
t_Value = getNum(eia_t, 'Value')
t_Column_Order = getNum(eia_t, 'Column_Order')

cur.execute("CREATE TABLE EIA_t(MSN VARCHAR(7), YYYYMM INT, Value REAL, Column_Order INT);")
firstline = True
for row in csv_t:
	if firstline:
		firstline = False
		continue
	cur.execute("INSERT INTO EIA_t VALUES (%s, %s, %s, %s);", ((row[t_MSN]), int(row[t_YYYYMM]), float(row[t_Value]), int(row[t_Column_Order])))

e_MSN = getNum(eia_e, 'MSN')
e_YYYYMM = getNum(eia_e, 'YYYYMM')
e_Value = getNum(eia_e, 'Value')
e_Column_Order = getNum(eia_e, 'Column_Order')

cur.execute("CREATE TABLE EIA_e(MSN VARCHAR(7), YYYYMM INT, Value VARCHAR(20), Column_Order INT);")
firstline = True
for row in csv_e:
	if firstline:
		firstline = False
		continue
	cur.execute("INSERT INTO EIA_e VALUES (%s, %s, %s, %s);", ((row[e_MSN]), int(row[e_YYYYMM]), (row[e_Value]), int(row[e_Column_Order])))


m_MSN = getNum(eia_m, 'MSN')
m_YYYYMM = getNum(eia_m, 'YYYYMM')
m_Value = getNum(eia_m, 'Value')
m_Column_Order = getNum(eia_m, 'Column_Order')

cur.execute("CREATE TABLE EIA_m(MSN VARCHAR(7), YYYYMM INT, Value VARCHAR(20), Column_Order INT);")
firstline = True
for row in csv_m:
	if firstline:
		firstline = False
		continue
	cur.execute("INSERT INTO EIA_m VALUES (%s, %s, %s, %s);", ((row[m_MSN]), int(row[m_YYYYMM]), (row[m_Value]), int(row[m_Column_Order])))

# Make the changes to the database persistent
conn.commit()


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

# Close communication with the database
cur.close()
conn.close()

