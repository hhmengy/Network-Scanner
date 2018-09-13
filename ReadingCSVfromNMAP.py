import csv
from io import StringIO
import nmap

n = nmap.PortScanner()
n.scan('127.0.0.1', '22-501')
p = n.csv()
print(p)



p = p.split("\n",1)[1]
f = StringIO(p)
reader = csv.reader(f,delimiter=';')
portnums = []
statuss = []
for row in reader:
	portnum = row[4]
	status = row[6]
	
	portnums.append(portnum)
	statuss.append(status)
index = 0
for portnum in portnums:
	print("port number: " + portnums[index] + " is " + statuss[index])
	index += 1
print("all other ports are closed")
# #print (p)
# #print("\n" + line)
