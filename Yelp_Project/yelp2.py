# import argparse
import json
import pprint
import sys
import urllib
import urllib2
import oauth2
import pandas
import sqlite3 as sqlite

fhand = open('pop.tsv', 'rU')
cityList = list()

for line in fhand:
    line = line.replace('\"', '').replace('\n', '').replace(',', '').split('\t')
    if line[1] != 'City ':
        cityNames = line[1]
        cityList.append(cityNames)

city = cityList[1] #change i in cityList[i] to produce each city's specific data
API_HOST = 'api.yelp.com'
SEARCH_LIMIT = 20
SEARCH_PATH = '/v2/search/'

#---To run the program, add actual consumer key etc, ---
#---and comment out the following lines---

# CONSUMER_KEY = ''
# CONSUMER_SECRET = ''
# TOKEN = ''
# TOKEN_SECRET = ''


def request(host, path, url_params=None):
    """Prepares OAuth authentication and sends the request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        urllib2.HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = 'https://{0}{1}?'.format(host, urllib.quote(path.encode('utf8')))

    consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    oauth_request = oauth2.Request(
        method="GET", url=url, parameters=url_params)

    oauth_request.update(
        {
            'oauth_nonce': oauth2.generate_nonce(),
            'oauth_timestamp': oauth2.generate_timestamp(),
            'oauth_token': TOKEN,
            'oauth_consumer_key': CONSUMER_KEY
        }
    )
    token = oauth2.Token(TOKEN, TOKEN_SECRET)
    oauth_request.sign_request(
        oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    signed_url = oauth_request.to_url()

    conn = urllib2.urlopen(signed_url, None)
    try:
        response = json.loads(conn.read())
    finally:
        conn.close()

    return response



def search_yelp(offset):
    
    url_params = {
        'term':'restaurants', 'location': city, 'category_filter': 'chinese', 
        'offset':offset, 'limit':SEARCH_LIMIT
    }

    # print urllib.urlencode(url_params)
    return request(API_HOST, SEARCH_PATH, url_params=url_params)




table_biz_tuple = ()
table_biz_list = []
def query_api():
    n_businesses = 1 
    df=pandas.DataFrame(data=None)
    offset = 0
    city = cityList[1] #change i in cityList[i] to produce each city's specific data
    while (n_businesses > 0): #run the cycle till the API gets results back.
        response = search_yelp(offset) 
            # print response
        offset = offset + 20 
        businesses = response.get('businesses')
        df2 = pandas.DataFrame(businesses)
        df = df.append(df2, ignore_index=True)
        n_businesses = len(businesses)
        # print n_businesses

        for i in range(len(businesses)):

            biz_id = businesses[i]['id']
            biz_name = (businesses[i]['name']).encode('utf8')
            biz_rating = businesses[i]['rating']
            review_count = businesses[i]['review_count']
            # snippet_text = businesses[i]['snippet_text']
            table_biz_tuple = (biz_name, biz_rating, review_count)
            table_biz_list.append(table_biz_tuple)
    #         # print table_biz_list
    #         # print table_biz_tuple

        total_ratings = 0
        total_biz = len(table_biz_list)
        
        for i in range(len(table_biz_list)):
            total_ratings += table_biz_list[i][1]
            
        average_rating = total_ratings / total_biz
    print 'Total Ratings: ', total_ratings, 'Total Restaurants: ', total_biz, 
    'City Average Rating: ', average_rating


   #Create a sql table to store fetched data
    with sqlite.connect('yelp_chinese_restaurants_sf.db') as con:
        cur = con.cursor()

        cur.execute("DROP TABLE IF EXISTS yelp_chinese_sf")
        cur.execute("CREATE TABLE yelp_chinese_sf(name TEXT, ratings REAL, review_count INT, snippet_text TEXT)")
        cur.executemany("INSERT INTO yelp_chinese_sf VALUES (?,?,?,?)", table_biz_list)
        con.commit()

        cur.execute("SELECT DISTINCT name, ratings FROM yelp_chinese_restaurants_sf ORDER BY ratings DESC LIMIT 20")
        rows = cur.fetchall()
        title = 'Top 20 res:' + '\n' + 'name, ratings'
        print title
        for row in rows:
            print ','.join([str(x) for x in row])
        print ''

        cur.execute("SELECT rating, ")
    
    return df



def main():
    try:
        query_api()
    except urllib2.HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0}. Abort program.'.format(error.code))


if __name__ == '__main__':
    main()