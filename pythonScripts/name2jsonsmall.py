import json
import csv

dict={};

f = open('newChat.csv', 'rb');

sourceGen = 0;

server = 1;

fileName = 'server' + str(server) + '.json'

output = {"nodes": [], "links": []};

#nodes = {'nodes': []};

#links = {'links': []};

fr = open(fileName, 'wb');

reader = csv.reader(f, delimiter=',')

for row in reader:
	if int(row[2]) != server:
		fr.write(json.dumps(output, indent=2, separators=(',', ': ')))
		fr.close()
		print 'Server ' + str(server) + ': ' + str(sourceGen);
		fileName = 'server' + str(server) + '.json'
		fr = open(fileName, 'wb')
		dict={}
		server = int(row[2])
		output = {"nodes": [], "links": []}
		sourceGen = 0;

	if sourceGen < 70:
		try: 
			dict[row[0]]
		except:
			dict[row[0]] = sourceGen;
			sourceGen += 1;
			output["nodes"].append({
				"group": int(row[2]),
				"name": row[0]
				});
		try:
			dict[row[1]]
		except:
			dict[row[1]] = sourceGen;
			sourceGen += 1;
			output["nodes"].append({
				"group": int(row[2]),
				"name": row[1]
				});
	else:
		try: 
			dict[row[0]]
			dict[row[1]]
		except:
			continue

	output["links"].append({
		"source": dict[row[0]],
		"target": dict[row[1]],
		"value": int(row[3])
		});
	#if sourceGen >= 70:
	#	break

fr.write(json.dumps(output, indent=2, separators=(',', ': ')))
fr.close()
print 'Server ' + str(server) + ': ' + str(sourceGen);
fileName = 'server' + str(server) + '.json'
fr = open(fileName, 'wb')
dict={}
server = int(row[2])
output = {"nodes": [], "links": []}
sourceGen = 0;

f.close();
fr.close();