#nmap scanner

import csv
from io import StringIO
import nmap

#ArgumentScan takes in file info, and nmap switches and runs a scan and ouputs that information 
#to the terminal and a file and returns the portnumbers,statuses, and IPs that were scanned			
def ArgumentScan(fout,portKey,scanKey,hostKey):
	
	#acquiring IP address
	allgood = 1
	while allgood == 1:
		IP = input("\nPlease enter an IP address, Target Specification switch or 'help' for a list of commands: ")
		if IP == "-iL":
			Fname = input(" Enter file name with targets in it: ")
			IP = IP + " " + Fname
			allgood =0
		elif IP == "-iR":
			hosts = input("Enter how many random hosts you would like to scan: ")
			IP = IP + " " + hosts
			allgood =0
		elif IP == "--exclude":
			allgood =0
		elif IP == "help":
			print("\nTarget Specification Commands: ")
			print("-iL\t-iR\t--exclude")
		else :
			IP = "'"+ IP + "'"
			allgood =0
		
	
	#if/else statements to determine which ports are scanned based on user switch input
	allgood = 0
	CheckForInt =1
	while allgood == 0:
		if portKey == "-F":
			upport = 100
			lowport = 1
			ports = " "
			print("\nNow Scanning the top 100 ports\n")
		elif portKey == "--top-ports":
			upport = input( "\nEnter the number of ports you wish to be scanned: ")
			lowport = 1
			portKey = portKey + " " + upport
			ports = " "
			print("\nNow Scanning the top " + upport + " ports\n")
		elif portKey == "-p-":
			lowport = 1
			upport = 65535
			ports= lowport + "-" + upport
			print("\nNow Scanning all ports\n")
		elif portKey == "-p-65535":
			lowport = 1
			upport=input("Enter the last port you wished to be scanned: ")
			ports= lowport + "-" + upport
			print("\nNow Scanning ports from:1 to:" + upport + "\n")
		elif portKey == " -p0-":
			lowport=input("\nEnter the first port you wish to be scanned: ")
			upport = 65535
			ports= lowport + "-" + upport
			print("\nNow Scanning ports from:"+ lowport + "to:65535\n")
		elif portKey == 'no':
			portKey = " "
			ports = " "
			print("\nNow Scanning...\n")
		else:
			cont = 1
			while cont == 1:
				service = input("\nWould you like to scan from a service name? ('yes' or 'no'): ") 
				if service == "yes" or service == "YES" or service == "Yes":
					ports = input("Enter service name: ")
					allgood = 1
					print("\n Now Scanning from service: " + ports)
					CheckForInt = 0
					break
				elif service == "no" or service == "NO" or service == "No":
					lowport=input("\nEnter the first port you wish to be scanned: ")
					upport=input("Enter the last port you wished to be scanned: ")
					ports= lowport + "-" + upport
					print("\nNow Scanning ports from:" + lowport + " to:"+ upport + "\n")
					break
				else:
					print ("Error: '" + service + "'not recognized'")
				
		if CheckForInt == 1:
			try:
				lowport = int(lowport)
				upport = int(upport)
			except:
				print("Error: Port values must be a number")
				continue
			#error checking for user input of ports
			if upport <= 65535 and upport > 0 and lowport <= 65535 and lowport > 0:
				allgood = 1
			elif portKey == " ":
				allgood = 1
			else:
				print("Error: port numbers must be greater than 0 and less than 65536")
	
	#if/else statements for host discovery switches with user input
	if hostKey == "-PS":	
		HOSTlowport = input("\nEnter the first port for the TCP SYN discovery:  ")
		HOSTupport = input("\nEnter the last port for the TCP SYN discovery:  ")
		HOSTports= HOSTlowport + "-" + HOSTupport
		hostKey = portKey + HOSTports
	elif hostKey == "-PA":
		HOSTlowport = input("\nEnter the first port for the TCP ACK discovery:  ")
		HOSTupport = input("\nEnter the last port for the TCP ACK discovery:  ")
		HOSTports= HOSTlowport + "-" + HOSTupport
		hostKey = portKey + HOSTports
	elif hostKey == "PU" :
		HOSTlowport = input("\nEnter the first port for the TCP SYN discovery:  ")
		HOSTupport = input("\nEnter the last port for the TCP SYN discovery:  ")
		HOSTports= HOSTlowport + "-" + HOSTupport
		hostKey = portKey + HOSTports
	elif hostKey == "no":
		hostKey = " "
		
	ports = "'" + ports + "'"	
	key = hostKey + " " + scanKey + " " +portKey + " " + ports
	fout.write("Port#,Status\n")#writing out to file
	
	#running the scan
	nmScan = nmap.PortScanner()	#creating PortScanner object
	lowport = str(lowport)
	nmScan.scan(IP, arguments = '%s' % key)#running the scan
	scaninfo = nmScan.csv()#acquiring info from scan in csv format
	scaninfo = scaninfo.split("\n",1)[1]#deleting first line of csv
	f = StringIO(scaninfo)
	reader = csv.reader(f,delimiter=';')#reading the values inbetween ';'
	
	#creating arrays to hold port numbers and the statuses
	portnums = []
	statuss = []
	protocols = []
	
	#putting the port numbers and statuses into arrays
	for row in reader:
		portnum = row[4]
		status = row[6]
		protocol = row[0]
		portnums.append(portnum)
		statuss.append(status)
		protocols.append(protocol)
	multiplier = len(set(protocols))
	
	index = 0
	#outputting the information to the console and to the file
	for portnum in portnums:
		if protocols[index] != protocols[index - 1]:
			print("\nOn IP: " + protocols[index])
		print("port number: " + portnums[index] + " is " + statuss[index])
		fout.write(portnums[index] + "," + statuss[index] + "," + protocols[index]+ "\n")
		index += 1
	
	print("\nAll unshown ports are closed")
			
	print("\nScan finished")
	fout.close()
	return portnums,statuss,protocols
#
#
#
#CompareScan is a function that takes in the port numbers, statuss, and IPs
#of the scan that was run and compares them to a file that has old scan 
#information and ouputs any differences
def CompareScan (pnums,ops,prots):
	allgood = 1
	while allgood == 1:
		try:	
			#opening file and acquiring CSV info
			fname = input("Enter input file Name: ")
			with open(fname) as csvfile:
				line= csvfile.readline()
				readCSV = csv.reader(csvfile,delimiter=",")#splitting at commas
				portnums = []
				operations = []
				protocols = []
				for row in readCSV:#putting portnumber and status into arrays
					portnum = row[0]
					operation = row[1]
					protocol = row[2]
					portnums.append(portnum)
					operations.append(operation)
					protocols.append(protocol)
			break
		except:
			print("Error: File Name: '" + fname +"' not Found or File not in comma separated format")
			
	#checking if there are any differences between scans		
	i = 0
	printingIP = 1
	for portnum in portnums:
		j = 0
		for pnum in pnums:
			if portnums[i] == pnums[j] and protocols[i] == prots [j]:
				if prots[j] != prots[j - 1]:
					printingIP = 1
				if operations [i] != ops[j]:
					if printingIP == 1:
						print("\nOn IP: " + prots[j])
						printingIP = 2
					print ("port number: "+portnums[i]+" has changed from: "+ operations[i] + " to: " + ops[j]) 
			j+=1
		i+=1
		
	#checking if any ports changed from closed to open/filtered for large range of ports
	j=0
	printingIP = 1
	for i in pnums:
		if i not in portnums:
			if prots[j] != prots[j - 1]:
				printingIP = 1
			if ops[j] != "closed":
				if printingIP == 1:	
					print("\nOn IP: " + prots[j])
					printingIP = 2
				print("port number: " + pnums[j] + " has changed from: closed to: " + ops[j])
		j+=1
	
	#checking if any old ports changed from open/filtered to closed for large range of ports
	i=0	
	printingIP = 1	
	for j in portnums:
		if j not in pnums:
			if prots[j] != prots[j - 1]:
				printingIP = 1
			if operations[i] != "closed":
				if printingIP == 1:
					print("\nOn IP: " + prots[j])
					printingIP = 2
				print("port number: " + portnums[i] + " has changed from:"+ operations[i]+"closed" )
		i+=1
			
#
#
#
#main acquires nmap keys and then runs the scan function with those keys
# and then compares the scan if the user wants to	
def main():
	print("Welcome to Nmap Scanner")
	
	#making sure user has nmap package
	try:
	   nm = nmap.PortScanner()         # instantiate nmap.PortScanner object
	except nmap.PortScannerError:
	   print('\nNmap not installed', sys.exc_info()[0])
	   sys.exit(0)
	except:
	   print("\nUnexpected error:", sys.exc_info()[0])
	   sys.exit(0)

	allOverAgain = "yes"
	while allOverAgain == "yes" or allOverAgain == "YES" or allOverAgain == "Yes":
	
		#acquiring file information
		fname = input("\nPlease enter file name you would like to have data outputted to: ")
		fout = open(fname,"w")
		
		#acquiring port specification switch from user
		allgood = 1
		while allgood == 1:
			portKey = input("\nPlease enter NMAP Port Specification switch you would like to use or 'help' for a list of commands\n or 'no' if you do not wish to enter a Port Specification switch: ")
			if portKey == "-p" or portKey == "-p-" or portKey == "-F" or portKey == "-F" or portKey == "--top-ports" 	or portKey == "-p65536" or portKey == "-p0-":
				allgood = 0
			elif portKey == "help":
				print("\nPort Specification commands:")
				print("-p\t-p-\t-F\n--top-ports\t-p-65535\n-p0-")
			elif portKey == "no":
				allgood = 0
			else:
				print("\nError: Switch: '" + portKey + "' not recognized. Switches are case sensitive, please try again")
			
		#acquiring scan type switch from user
		allgood = 1
		while allgood == 1:
			scanKey = input("\nPlease enter NMAP Scan Technique switch you would like to use or 'help' for a list of commands\n or 'no' if you do not wish to enter a Scan Technique switch:  ")
			if scanKey == "-sS" or scanKey == "-sT" or scanKey == "-sU" or scanKey == "-sA" or scanKey == "-sW" or scanKey == "-sM":
				allgood = 0
			elif scanKey == "help":
				print("\nScan Techniques commands:")
				print("-sS\t-sT\t-sU\n-sA\t-sW\t-sM")
			elif scanKey == "no":
				scanKey = " "
				allgood = 0
			else:
				print("\nError: Switch: '" + scanKey + "' not recognized. Switches are case sensitive, please try again")
		
		#acquiring Host Discovery switch from user
		allgood = 1
		while allgood == 1:
			hostKey = input("\nPlease enter NMAP Host Discovery switch you would like to use or 'help' for a list of commands\n or 'no' if you do not wish to enter a Host Discovery Switch: ")
			if hostKey == "-sL" or hostKey == "-sn" or hostKey == "-Pn" or hostKey == "-PS" or hostKey == "-PA" or hostKey == "-PU" or hostKey == "-PR" or hostKey == "-n":
				allgood = 0
			elif hostKey == "help":
				print("\nHost Discovery Commands: ")
				print("-sL\t-sn\t-Pn\n-PS\t-PA\t-PU\n-PR\t-n")
			elif hostKey == "no":
				allgood = 0
			else:
				print("\nError: Switch: '" + hostKey + "' not recognized. Switches are case sensitive, please try again")
				
		
		#running scan
		pnums,ops,prots = ArgumentScan(fout,portKey,scanKey,hostKey)
		
		#asking and checking if user would like to compare scan to a recent scan
		allGood = 1
		while allGood == 1:
			compareScan = input("\nWould you like to compare scan to a recent scan? ('yes' or 'no'): ")	
			#comparing differences between scans
			if compareScan == "yes" or compareScan == "YES" or compareScan == "Yes":
				 CompareScan(pnums,ops,prots)
				 break
			elif compareScan == "no" or compareScan == "NO" or compareScan == "No":	
				break
			else :
				print("Error: '"+ compareScan + "' Not recognized")
		
		#asking and checking if user wants to run another scan
		while allOverAgain == "yes" or allOverAgain == "Yes" or allOverAgain == "YES":
			allOverAgain = input("\nwould you like to run another scan? ('yes' or 'no'): ")	
			if allOverAgain == "no" or allOverAgain == "No" or allOverAgain == "NO" or allOverAgain == "yes" or allOverAgain == "Yes" or allOverAgain == "YES":
				break
			else:
				print("Error: '"+ allOverAgain + "' Not recognized")
				allOverAgain = "yes"
				
if __name__ == "__main__":
	main()
