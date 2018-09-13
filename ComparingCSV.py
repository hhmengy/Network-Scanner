from IPy import IP
import sys
import socket
import csv
def dilly(a):
	a = int(a)
	c=a+5
	print (c)
def main():
	# fname = input("Enter input file Name: ")
	# with open(fname) as csvfile:
		# line= csvfile.readline()
		# readCSV = csv.reader(csvfile,delimiter=",")
		# portnums = []
		# operations = []
		# for row in readCSV:
			# portnum = row[0]
			# operation = row[1]
			
			# portnums.append(portnum)
			# operations.append(operation)
		
		pnums = ["135","136","137","138","135","136","137","138","134"]
		ops = ["open","filtered","open","closed","open","filtered","open","closed","open"]
		IPS = ['127.0.0.1','127.0.0.1','127.0.0.1','127.0.0.1','127.0.0.2','127.0.0.2','127.0.0.2','127.0.0.2','127.0.0.3']
		portnums = ["135","136","137","138","135","136","137","138","134"]
		operations = ["open","closed","open","closed","open","filtered","filtered","open","open"]
		IPAS = ['127.0.0.1','127.0.0.1','127.0.0.1','127.0.0.1','127.0.0.2','127.0.0.2','127.0.0.2','127.0.0.2','127.0.0.3']
		# whatportnum = input("what port num would you like to know the status of? ")
		# portnumdex = portnums.index(whatportnum)
		# thestatus = operations[portnumdex]
		# print('the status of ' + whatportnum +' is: '+ thestatus)
		
		
		
		i = 0
		for portnum in portnums:
			j = 0
			for pnum in pnums:
				if portnums[i] == pnums[j] and IPAS[i] == IPS[j]:
					if IPS[j] != IPS[j - 1]:
						DOIT = 1
					stat1 = operations[i]
					stat2 = ops[j]
					if stat1 != stat2:
						if DOIT == 1:
							print("\nOn IP: " + IPS[j])
							DOIT = 2
						print ("port number: "+portnums[i]+" has changed from: "+ operations[i] + " to: " + ops[j]) 
				j+=1
			i+=1	
	#checking if any ports changed from closed to open/filtered for large range of ports
		j=0
		for i in pnums:
			if i not in portnums:
				if ops[j] != "closed":
					print("port number: " + pnums[j] + " has changed from: closed to: " + ops[j])
			j+=1
		print("all other ports are unchanged")
		
		#checking if any old ports changed from open/filtered to closed for large range of ports
		i=0		
		for j in portnums:
			if j not in pnums:
				if operations[i] != "closed":
					print("port number: " + portnums[i] + " has changed from:c closed to:  " + operations[i])
			i+=1
		# i = 0
		# for portnum in portnums:
			# portnumdex = portnums.index("135")
			# stat1 = operations[portnumdex]
			
			# portnumdex2 = pnums.index("135")
			# stat2 = ops[portnumdex2]
		
			# if stat1 == stat2:
				# print(portnums[i]+" is unchanged")
			# else:
				# print (portnums[i]+" has changed") 
			# i += 1
	
	
if __name__ == "__main__":
	main()

