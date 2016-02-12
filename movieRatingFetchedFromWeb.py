#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
import json, unicodedata
import re, time,csv

# --------------------------------- step 1 ----------------------------------

#use a for loop to fetch webpages for top 1-50, 51-100, 101-150, 151-200 movie pages
for i in range (1,200,50):
	response = urllib2.urlopen('http://www.imdb.com/search/title?at=0&genres=sci_fi&sort=user_rating&start='+str(i)+'&title_type=feature')
	html_doc = response.read()
	soup = BeautifulSoup(html_doc, 'html.parser')

	outfile = open('step1_top_scifi_movies_'+str(i)+'_to_'+str(i+49)+'_output_liuxj.html', 'w')
	outfile.write(soup.prettify().encode('utf-8'))
	outfile.close()


# #--------------------------- step 2 -------------------------------

outfile_step2 = open('step2_top_200_scifi_movies.tsv', 'w')
outfile_step2.write('\t'.join(['Rank', 'IMDB ID', 'Title', 'Year', 'Rating']) + '\n')


#use a for loop to read data from each page and fetch useful data sets

imdbID_list = []
title_list = []
year_list = []
imdb_voting_list = []
for i in range (1,200,50):
	response = urllib2.urlopen('http://www.imdb.com/search/title?at=0&genres=sci_fi&sort=user_rating&start='+str(i)+'&title_type=feature')
	html_doc = response.read()
	soup = BeautifulSoup(html_doc, 'html.parser')
	data_table = soup.find_all('table')[0]
	
	lol = []
	for row in data_table.find_all('tr')[1:]:
			
		data = []
		imdb = []
		
		for col in row.find_all('td', class_ = "number"):
			data.append((col.string).rstrip('.'))
		for col in row.find_all('a'):
			imdb.append(col.get('href'))
			imdbID = re.findall(r'tt[0-9]+', imdb[0])
		for i in imdbID:
			data.append(i)
			imdbID_list.append(i)
		for col in row.find_all('a')[1]:
			data.append(col.string)
			title_list.append(col.string)
		for col in row.find_all('span', class_ = "year_type"):
			data.append((col.string)[1:-1])
			year_list.append((col.string[1:-1]))
		for col in row.find_all('span', class_ = 'value'):
			data.append(col.string)
			imdb_voting_list.append(col.string)

		lol.append(data)

		
	for item in lol:
		line = '\t'.join(item) + '\n'
		outfile_step2.write(unicode(line).encode('utf-8'))

outfile_step2.close()


# ------------------------- step 3 ---------------------------------




# tmdb_list =[]
# tmdb_pair = []
# for i in imdbID_list:
# 	tmdb_pair = []

# 	url ='http://api.themoviedb.org/3/find/' + str(i)+'?api_key=d28f8d670eaf80e9b9966631ea1c3cc2&external_source=imdb_id'
# 	time.sleep(5)

# 	response = urllib2.urlopen(url)
# 	json_str = response.read()
# 	j = json_str.decode('utf-8')
	


# 	tmdb_pair.append(i)
# 	tmdb_pair.append(j)
# 	tmdb_list.append(tmdb_pair)




# outfile_step3 = open('step3.txt', 'w')
# for movie in tmdb_list:
# 	line = '\t'.join(movie) + '\n'
# 	outfile_step3.write(unicode(line).encode('utf-8'))
# outfile_step3.close()



# -------------------------- step 4 ----------------------------------


fhand = open('step3.txt', 'rU')

rating_list = []

tmdb_voting_list = []
for line in fhand:
	t_str = re.findall(r'tt[0-9]+', line)
	j_str = re.findall(r'"vote_average":[0-9].[0-9]',line)
	voting = re.findall(r'[0-9].[0-9]', str(j_str))
	tmdb_voting_list.append(voting)

for i in range(len(imdbID_list)):
	rating_list.append([imdbID_list[i],title_list[i],year_list[i],imdb_voting_list[i], tmdb_voting_list[i]])


rating_list = [x for x in rating_list if len(x [4]) == 1]
rating_list = [x for x in rating_list if x[4][0]!='0.0']

for item in rating_list:
	item[4] = item[4][0]

outfile_step4 = open('step4.csv', 'wb')

with open('step4.csv','wb') as f:
	writer = csv.writer(f)
	writer.writerow(['IMDB ID', 'Title', 'Year', 'IMDB Rating', 'themoviedb Rating'])
	for item in rating_list:
		writer.writerow([item[0], unicode(item[1]).encode('utf-8'), item[2], item[3], item[4]])
		
outfile_step4.close()




