from pprint import pprint
import requests
import sqlite3
import json
import matplotlib.pyplot as plt
import numpy as np
from requests import api

api_search = 'https://rss.applemarketingtools.com/api/v2/us/music/most-played/100/songs.json'
api_search1 = 'http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/ws/RSS/topalbums/limit=50/json'
api_search2 = 'http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/ws/RSS/topsongs/limit=50/json'
def db_setup():
        #Access API / Set up access
        #Set up database 
        #Make cur object
        #Make con object
        #Set up soup
    connection = sqlite3.connect('music.db')
    cursor = connection.cursor()
    return connection, cursor

def api_request(term):
    r = requests.get(term)
    content = r.json()
    return content

def data_grab_song(dataset):

    title_list = []
    artist_list = []
    date_list = []
    genre_list = []

    print (type(dataset))

    for item in dataset['feed']['entry']:
        print(item['im:name']['label'])
        title_list.append(item['im:name']['label'])
        print(item['im:artist']['label'])
        artist_list.append(item['im:artist']['label'])
        print(item['im:releaseDate']['attributes']['label'])
        date_list.append(item['im:releaseDate']['attributes']['label'])
        print(item['category']['attributes']['term'])
        genre_list.append(item['category']['attributes']['term'])
    
    return ('song', title_list, artist_list, date_list, genre_list)

def data_grab_album(dataset):

    title_list = []
    artist_list = []
    date_list = []
    genre_list = []

    print (type(dataset))

    for item in dataset['feed']['entry']:
        print(item['im:name']['label'])
        title_list.append(item['im:name']['label'])
        print(item['im:artist']['label'])
        artist_list.append(item['im:artist']['label'])
        print(item['im:releaseDate']['label'])
        date_list.append(item['im:releaseDate']['label'])
        print(item['category']['attributes']['term'])
        genre_list.append(item['category']['attributes']['term'])
    
    return ('album', title_list, artist_list, date_list, genre_list)
        

def create_table():
    conn, cur = db_setup()
    cur.execute('''DROP TABLE IF EXISTS Songs''')
    cur.execute('''CREATE TABLE Songs(id, title TEXT, artist TEXT, releaseDate TEXT, genre TEXT)''')
    conn.commit()
    conn.close()


def db_fill(id, titles, artists, dates, genres):
    #Access API with connection
    ##Store 100 items in the database from your API 
    #Each time you execute the code you must only store 25 or fewer items, 
    # run the code multiple times to get 100 items total processed
    
    conn, cur = db_setup()
    
    rows = []

    for i in range(len(titles)):
        rows.append((id, titles[i], artists[i], dates[i], genres[i]))
    
    sql = '''INSERT INTO Songs(id, title, artist, releaseDate, genre) VALUES(?, ?, ?, ?, ?)'''

    for row in rows:
        cur.execute(sql, row)
    
    conn.commit()
    conn.close()

def calc_top_from_category():
    conn, cur = db_setup()
    query = '''SELECT COUNT(*)
            FROM Songs
            GROUP BY genre
            '''

    data = cur.execute(query).fetchall()
    return data

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
    db_fill(data_grab_song(api_request(api_search2))[0], data_grab_song(api_request(api_search2))[1], data_grab_song(api_request(api_search2))[2], data_grab_song(api_request(api_search2))[3], data_grab_song(api_request(api_search2))[4],)
    db_fill(data_grab_album(api_request(api_search1))[0], data_grab_album(api_request(api_search1))[1], data_grab_album(api_request(api_search1))[2], data_grab_album(api_request(api_search1))[3], data_grab_album(api_request(api_search1))[4])



if __name__ == "__main__":
    main()
