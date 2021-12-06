from bs4 import BeautifulSoup
from pprint import pprint
import requests
import sqlite3
import json

from requests import api

url = 'https://itunes.apple.com/us/rss/topsongs/limit=3/json'


def db_setup():
        #Access API / Set up access
        #Set up database 
        #Make cur object
        #Make con object
        #Set up soup
    connection = sqlite3.connect('music_db')
    cursor = connection.cursor()
    return connection, cursor

def api_request(url):
    r = requests.get(url)
    content = r.json()
    return content

def data_grab(dataset):

    title_list = []
    artist_list = []
    album_list = []
    genre_list = []
    print (type(dataset.items()))
    print (type(dataset['feed']))
    print(len(dataset['feed']['entry']))


    for item in dataset['feed']['entry']:
        print(type(dataset))
        title_list.append(item['im:name']['label'])
        artist_list.append(item['im:artist']['label'])
        album_list.append(item['im:collection']['im:name']['label'])
        genre_list.append(item['category']['attributes']['term'])
    
    return (title_list, artist_list, album_list, genre_list)
        

def create_table():
    conn, cur = db_setup()
    cur.execute('''DROP TABLE IF EXISTS Songs''')
    cur.execute('''CREATE TABLE Songs(id, title TEXT, artist TEXT, album TEXT, genre TEXT)''')
    conn.commit()
    conn.close()


def db_fill(titles, artists, albums, genres):
    #Access API with connection
    ##Store 100 items in the database from your API 
    #Each time you execute the code you must only store 25 or fewer items, 
    # run the code multiple times to get 100 items total processed
    
    conn, cur = db_setup()
    
    rows = []

    for i in range(len(titles)):
        rows.append(('Music', titles[i], artists[i], albums[i], genres[i]))
    
    sql = '''INSERT INTO Songs(id, title, artist, album, genre) VALUES(?, ?, ?, ?, ?)'''

    for row in rows:

        cur.execute(sql, row)
        

def calc_top_from_category():
    #Combine 2 tables in video game
    #With stored items, look at their genres
    # Make dictionary of genres and how many items fall into each
    # find the highest number, store in json, csv or text file

    pass

def make_plotly_graphic(genre = "None"):
    #Combine 2 tables in video game
    #Using Plotly make graph visuals
    #Try to make a different one, for now
    #iTunes doing percentage pie of the different genres
    #Steam: use scatter plot to find the average rating of a given genre
    #iMDB: bar graph where you put ratings on the x axis (0-5) and how many 
    #songs from a genre in your table have that info


    pass

#Tentative Deadline December 5th for code


'''
Notes:
Need a commin column (medium?) in each table stating whether this is a game, song, or movie
'''

def main():
    db_setup()
    create_table()
    print (type((data_grab(api_request(url)))))
    db_fill(data_grab(api_request(url))[0], data_grab(api_request(url))[1], data_grab(api_request(url))[2], data_grab(api_request(url))[3])



if __name__ == "__main__":
    main()
