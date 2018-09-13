from IPy import IP
import socket
import csv
def dilly(a):
	a = int(a)
	c=a+5
	print (c)
def main():
	allgood = 0
	while allgood == 0:
		try:
			fname = input("Enter input file Name: ")
			with open(fname) as csvfile:
				line= csvfile.readline()
				readCSV = csv.reader(csvfile,delimiter=",")
				portnums = []
				operations = []
				for row in readCSV:
					portnum = row[0]
					operation = row[1]
					
					portnums.append(portnum)
					operations.append(operation)
				
				whatportnum = input("what port num would you like to know the status of? ")
				portnumdex = portnums.index(whatportnum)
				thestatus = operations[portnumdex]
				print('the status of ' + whatportnum +' is: '+ thestatus)
				allgood = 1
		except:
			print("you did bad")
	
	
	
if __name__ == "__main__":
	main()
