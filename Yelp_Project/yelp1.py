import csv
import oauth2, urllib2, json

fhand = open('pop.tsv', 'rU')
cityList = list()
res_List = list()
city_res_list = list()
sorted_res_List = list()


for line in fhand:
	line = line.replace('\"', '').replace('\n', '').replace(',', '').split('\t')
	if line[1] != 'City ':
		cityNames = line[1]
		cityList.append(cityNames)
print cityList


for i in range(len(cityList)):
	city = cityList[i]

#---To run the program, add actual consumer key etc, ---
#---and comment out the following lines---

	# consumer_key = ''
	# consumer_secret = '‘
	# token = ''
	# token_secret = ''

	consumer = oauth2.Consumer(consumer_key, consumer_secret)

	#The url used to call yelp api
	url = 'http://api.yelp.com/v2/search?term=restaurants&category_filter=chinese&location=' + str(city)


	oauth_request = oauth2.Request('GET', url, {})
	oauth_request.update({'oauth_nonce': oauth2.generate_nonce(),
	                      'oauth_timestamp': oauth2.generate_timestamp(),
	                      'oauth_token': token,
	                      'oauth_consumer_key': consumer_key})

	token = oauth2.Token(token, token_secret)
	oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
	signed_url = oauth_request.to_url()


	conn = urllib2.urlopen(signed_url, None)
	json_response = conn.read()
	yelp_data = json.loads(json_response)

	total = yelp_data['total']
	res_List = [city, total]
	city_res_list.append(res_List)
	city_res_list_sorted = sorted(city_res_list, key = lambda c : c[1], reverse=True)
	header = ['city name', 'chinese restaurant counts']
	city_res_list_sorted.insert(0, header)

#Write returned results into a csv file
with open('city_res.csv', 'wb') as f:
	writer = csv.writer(f)
	writer.writerows(city_res_list_sorted)

fhand.close()



