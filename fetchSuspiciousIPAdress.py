import re
import urlparse
import csv

fhand=open('access_log.txt','rU')
valid = list()
invalid = list()

def is_valid(line):
	# Find lines with HTTP verb as GET, POST, or HEAD; URL starts with http:// or https://;
	# and the status code is 2xx, 3xx, or 5xx
	if re.search(r'^.*"(GET|POST|HEAD)\s(http://|https://).*"\s(2..|3..|5..)',line, re.IGNORECASE): 
		#match1 is used as a group search to get URL
		match1 = re.search(r'(^.*)"(GET|POST|HEAD)\s(.*?)\s',line)
		if match1:
			url = match1.group(3)
			o = urlparse.urlparse(url)  #parse URL
			q = urlparse.parse_qs(o.query, True)
			i = 0 #Use i as an indicator to see if length of each field in the URL query string
			for k in q:
				field = str(q[k])
				if len(field) >= 80:
					i = 1
			if i == 1:
				return False
			else:
				return True

	#Find lines with HTTP verb as CONNECT, and status code of 2xx, 3xx, or 5xx
	if re.search(r'^.*"CONNECT\s(.*)"\s(2..|3..|5..)', line, re.IGNORECASE):
		return True

	else:
		return False
	

for line in fhand:
	if is_valid(line) == True:
		valid.append(line)
	if is_valid(line) == False:
		invalid.append(line)

fhand.close()

fileValid = open('valid_access_log_liuxj.txt', 'w')
fileValid.writelines(valid)
fileInvalid = open('invalid_access_log_liuxj.txt', 'w')
fileInvalid.writelines(invalid)


ipDict = dict()
def extract_ip(line):
	match = re.search(r'([0-9].*[0-9])\s\-\s\-', line,re.IGNORECASE)
	if match:
		ip = match.group(1)
	return ip

for line in invalid:
	ip = extract_ip(line)
	
	if ip not in ipDict.keys():
		ipDict[ip] = 1
	else:
		ipDict[ip] += 1

ipDictSorted = sorted(ipDict.items(), key = lambda x:x[1],reverse = True)

fileSuspicious = open('suspicious_ip_summary_liuxj.csv', 'wb')
csvFile = csv.writer(fileSuspicious)
csvFile.writerow(['IP Address', 'Attempts'])
for row in ipDictSorted:
	csvFile.writerow(row)

fileValid.close()
fileInvalid.close()
fileSuspicious.close()





