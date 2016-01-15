import csv
import math


countryList = list()
countryData = list()
countries = set()
countryDict = dict()
countryListReturned = list()
countryDictReturned = dict()


# -------------------------------step 1-------------------------------------

fhand = open('world_bank_indicators.tsv', 'rU')

#Clean data and store useful data in a list called countryList, containing each country's name, 
#and eleven years' total population, urban population, and life expectancy.
#Use a set called countries to store each country's name

for line in fhand:
	line = line.replace('\"', '').replace('\n', '').replace(',', '').split('\t')
	
	if line[0]!='Country Name' and line[9]!='' and line[10]!='':
		countryNames = line[0]
		totalPopulation = line[9].replace(",", "")
		urbanPopulation = line[10].replace(",", "")
		lifeExpectancy = line[14]
		countryData = [countryNames, totalPopulation, urbanPopulation, lifeExpectancy]
		countryList.append(countryData)
		countries.add(countryNames)

for country in countries:
	countryDict[country]=[]
	countryDictReturned[country] = []

for item in countryList:
	countryDict[item[0]].append(item)

for k in countryDict:
	countryNew = list()
	countryNew.append(k)
	totalP = 0
	urbanP = 0
	lifeExpectancy = 0
	n = len(countryDict[k])
	m = 0
	for item in countryDict[k]:
		totalP += int(item[1])
		urbanP += int(item[2])
		if item[3] !='':
			lifeExpectancy += float(item[3])
			m+=1
	
	totalPopulation = totalP
	urbanPopulation = urbanP
	averageTotalP = float(totalP / n)
	averageUrbanP = float(urbanP / n)
	averageUrbanRatio = averageUrbanP / averageTotalP
	averageLifeExpectancy = 0 if m == 0 else lifeExpectancy / m

	countryNew.append(averageUrbanRatio)
	countryNew.append(averageLifeExpectancy)
	countryNew.append(totalPopulation)
	countryNew.append(urbanPopulation)
	countryListReturned.append(countryNew)
	countryListReturnedSorted = sorted(countryListReturned, key=lambda country:country[0])
	header = ['country name', 'average urban population ratio', 'average life expectancy', 'sum of total population in all years', 'sum of urban population in all years']
	countryListReturnedSorted.insert(0, header)

# Delete lines without life expectancy data
indexList = list()
for item in countryListReturnedSorted:
	if item[2] == 0:
		indexOfInvalid = countryListReturnedSorted.index(item)
	 	del countryListReturnedSorted[indexOfInvalid]

indexList2 = list()
for item in countryListReturnedSorted:
	if item[2] == 0:
		indexOfInvalid2 = countryListReturnedSorted.index(item)
	 	del countryListReturnedSorted[indexOfInvalid2]


with open('si601_w16_hw1_step1_liuxj.csv', 'wb') as f:
 	writer = csv.writer(f)
 	writer.writerows(countryListReturnedSorted)

fhand.close()

# ------------step 2 for life expectancy----------------------
countryList2 = list()
countries2 = set()
countryDict2 = dict()
countryListReturned2 = list()
countryDictReturned2 = dict()


fhand = open('world_bank_indicators.tsv', 'rU')

for line in fhand:
	line = line.replace('\"', '').replace('\n', '').replace(',', '').split('\t')

	if line[0]!='Country Name' and line[14]!='':
		countryNames = line[0]
		totalPopulation = line[9].replace(",", "")
		urbanPopulation = line[10].replace(",", "")
		lifeExpectancy = line[14]
		countryData2 = [countryNames, totalPopulation, urbanPopulation, lifeExpectancy]
		countryList2.append(countryData2)
		countries2.add(countryNames)

for country in countries2:
	countryDict2[country]=[]


for item in countryList2:
	countryDict2[item[0]].append(item)

for k in countryDict2:
	countryNew2 = list()
	countryNew2.append(k)
	lifeExpectancy = 0
	n = len(countryDict2[k])
	for item in countryDict2[k]:
		lifeExpectancy += float(item[3])
	
	averageLifeExpectancy = lifeExpectancy / n
	countryNew2.append(averageLifeExpectancy)
	countryListReturned2.append(countryNew2)
	countryListReturnedSorted2 = sorted(countryListReturned2, key=lambda country:country[0])

fhand.close()

# ---------------------------step2 for urban ratio ----------------------------
countryList3 = list()
countries3 = set()
countryDict3 = dict()
countryListReturned3 = list()
countryDictReturned3 = dict()

fhand = open('world_bank_indicators.tsv', 'rU')

for line in fhand:
	line = line.replace('\"', '').replace('\n', '').replace(',', '').split('\t')

	if line[0]!='Country Name' and line[9] != '' and line[10]!='':
		countryNames = line[0]
		totalPopulation = line[9].replace(",", "")
		urbanPopulation = line[10].replace(",", "")
		countryData3 = [countryNames, totalPopulation, urbanPopulation]
		countryList3.append(countryData3)
		countries3.add(countryNames)

for country in countries3:
	countryDict3[country]=[]


for item in countryList3:
	countryDict3[item[0]].append(item)

for k in countryDict3:
	countryNew3 = list()
	countryNew3.append(k)
	totalP = 0
	urbanP = 0
	n = len(countryDict[k])
	for item in countryDict3[k]:
		totalP += int(item[1])
		urbanP += int(item[2])
	
	
	totalPopulation = totalP
	urbanPopulation = urbanP
	averageTotalP = float(totalP / n)
	averageUrbanP = float(urbanP / n)
	averageUrbanRatio = averageUrbanP / averageTotalP

	countryNew3.append(totalPopulation)
	countryNew3.append(urbanPopulation)
	countryListReturned3.append(countryNew)
	countryListReturnedSorted3 = sorted(countryListReturned, key=lambda country:country[0])
	header = ['country name', 'sum of total population in all years', 'sum of urban population in all years']
	countryListReturnedSorted3.insert(0, header) 
	
fhand.close()

fhand2 = open('world_bank_regions.tsv', 'rU')

countryRegionDict = dict()
countryRegionList = list()
regionDict = dict()
regionDict2 = dict()
regions = set()

for line in fhand2:
	line=line.replace('\"','').replace('\n','').replace(',','').split('\t')
	regionNames = line[0]
	countryNames = line[2]
	countryRegionDict[countryNames] = regionNames
	regions.add(regionNames)

for item in countryListReturnedSorted2:
	item.insert(0, countryRegionDict.get(item[0], 'no region'))

del	countryListReturnedSorted3[0]

for item in countryListReturnedSorted3:
	item.insert(0,countryRegionDict.get(item[0], 'no region'))

for region in regions:
	regionDict[region] = []
	regionDict2[region] = []

regionList = list()

for item in countryListReturnedSorted3:
	if item[0] != 'no region':
		regionDict2[item[0]].append(item)

for k in regionDict2:
	regionNew = list()
	regionNew.append(k)
	regionTotalP = 0
	regionUrbanP = 0
	n = len(regionDict2[k])

	for item in regionDict2[k]:
		regionTotalP += float(item[4])
		regionUrbanP += float(item[5])
	
	averageUrbanRatio = regionUrbanP / regionTotalP
	
	regionNew.append(averageUrbanRatio)
	regionList.append(regionNew)

	


for item in countryListReturnedSorted2:
	if item[0] != 'no region':	
		regionDict[item[0]].append(item)


for k in regionDict:
	
	regionLifeExpectancy = 0
	n = len(regionDict[k])

	for item in regionDict[k]:
		regionLifeExpectancy += float(item[2])
	averageLifeExpectancy = regionLifeExpectancy / n

	for item in regionList:
		if item[0] == k:
			item.append(averageLifeExpectancy)

headerRegion = ['region', 'average urban population ratio', 'average life expectancy']
regionListSorted = sorted(regionList, key = lambda region: region[2], reverse=True)
regionListSorted.insert(0, headerRegion)


with open('si601_w16_hw1_step2_liuxj.csv', 'wb') as f:
 	writer = csv.writer(f)
 	writer.writerows(regionListSorted)

fhand2.close()






