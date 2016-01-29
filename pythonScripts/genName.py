import names
import csv

dict={};

f = open('chatdata.csv', 'rb');
fr = open('newChat.csv', 'wb');
reader = csv.reader(f, delimiter=',')
for row in reader:
	try: 
		dict[row[0]]
	except:
		dict[row[0]] = names.get_first_name() +'_'+ names.get_last_name()
	try:
		dict[row[1]]
	except:
		dict[row[1]] = names.get_first_name() +'_'+ names.get_last_name()

	replace = dict[row[0]] + ',' + dict[row[1]] + ',' + row[2] +',' +row[3] +'\n'
	fr.write(replace)
f.close();

'''
fo = open('chatdata.csv', 'rb');
reader = csv.reader(fo, delimiter=',')
for row in reader:
	replace = dict[row[0]] + ',' + dict[row[1]] + ',' + row[2] +',' +row[3]
	fr.write(replace)

fo.close()
'''
fr.close()