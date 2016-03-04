import json
import sqlite3 as sqlite

fhand = open('movie_actors_data.txt', 'rU')


table_genre_tuple = ()
table_genre_list = []
table_movies_tuple = ()
table_movies_list = []
table_actor_tuple = ()
table_actor_list = []

for line in fhand:
	data = json.loads(line)
	
	imdb_id = data['imdb_id']
	genres = data['genres']
	title = data['title']
	year = data['year']
	rating = data['rating']
	actors = data['actors']

	# imdb_id_genres_list.append(imdb_id)
	# imdb_id_genres_list.append(genres)
	for i in range(len(genres)):
		table_genre_tuple = (imdb_id, genres[i])
		table_genre_list.append(table_genre_tuple)

	table_movies_tuple = (imdb_id, title, year, rating)
	table_movies_list.append(table_movies_tuple)

	for i in range(len(actors)):
		table_actor_tuple = (imdb_id, actors[i])
		table_actor_list.append(table_actor_tuple)
	
with sqlite.connect('si601_w16_hw4_part1_liuxj.db') as con:
	cur = con.cursor()

	cur.execute("DROP TABLE IF EXISTS movie_genre")
	cur.execute("CREATE TABLE movie_genre(imdb_id TEXT, genres TEXT)")
	cur.executemany("INSERT INTO movie_genre VALUES (?,?)", table_genre_list)
	con.commit()

	cur.execute("DROP TABLE IF EXISTS movies")
	cur.execute("CREATE TABLE movies(imdb_id TEXT, title TEXT, year INT, rating REAL)")
	cur.executemany("INSERT INTO movies VALUES (?,?,?,?)", table_movies_list)
	con.commit()

	cur.execute("DROP TABLE IF EXISTS movie_actor")
	cur.execute("CREATE TABLE movie_actor(imdb_id TEXT, actor TEXT)")
	cur.executemany("INSERT INTO movie_actor VALUES (?,?)", table_actor_list)
	con.commit()


	cur.execute("SELECT genres, Count(genres) FROM movie_genre GROUP BY genres ORDER BY Count(genres) DESC LIMIT 10")
	rows = cur.fetchall()
	title = 'Top 10 genres:' + '\n' + 'Genre, Movies'
	print title
	for row in rows:
		print ','.join([str(x) for x in row])
	print ''

	cur.execute("SELECT year, Count(year) FROM movies GROUP BY year ORDER BY year")
	rows = cur.fetchall()
	title = 'movies broken down by year:' +'\n' +'Year, Movies'
	print title
	for row in rows:
		print ', '.join([str(x) for x in row])
	print ''


	cur.execute("SELECT movies.title, movies.year, movies.rating FROM movies INNER JOIN movie_genre ON (movies.imdb_id = movie_genre.imdb_id) WHERE movie_genre.genres == 'Sci-Fi' ORDER BY movies.rating DESC, movies.year DESC")
	rows = cur.fetchall()
	title = 'Sci-Fi movies:'+'\n'+'Title, Year, Rating'
	print title
	for row in rows:
		print', '.join([str(unicode(x).encode('utf-8')) for x in row])
	print ''

	cur.execute("SELECT movie_actor.actor, Count(movie_actor.actor) FROM movie_actor INNER JOIN movies ON (movie_actor.imdb_id = movies.imdb_id) WHERE movies.year >= 2000 GROUP BY movie_actor.actor ORDER BY Count(movie_actor.actor) DESC LIMIT 10")
	rows = cur.fetchall()
	title = 'In and after year 2000, top 10 actors who played in most movies: '+'\n'+'Actor, Movies'
	print title
	for row in rows:
		print', '.join([str(unicode(x).encode('utf-8')) for x in row])
	print ''
 
	cur.execute("SELECT a.actor, b.actor, Count(*) AS occurrence FROM movie_actor a INNER JOIN movie_actor b ON a.imdb_id = b.imdb_id WHERE a.actor < b.actor GROUP BY b.actor, a.actor HAVING occurrence >= 3 ORDER BY occurrence DESC, a.actor ASC")
	rows = cur.fetchall()
	title = 'Pairs of actors who co-stared in 3 or more movies: ' + '\n' + 'Actor A, Actor B, Co-stared Movies'
	print title
	for row in rows:
		print ', '.join([str(unicode(x).encode('utf-8')) for x in row])


