import sqlite3
import plotly.graph_objects as go
import requests
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
from requests import api
from bs4 import BeautifulSoup
import pandas as pd
from matplotlib import cm

api_search1 = 'http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/ws/RSS/topalbums/limit=50/json'
api_search2 = 'http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/ws/RSS/topsongs/limit=50/json'
def db_setup():
    '''
    Sets up connection to the entertainment database
    '''
    connection = sqlite3.connect('entertainment.db')
    cursor = connection.cursor()
    return connection, cursor
def api_request(term):
    '''
    Requests data from passed API search term and returns data in json format
    '''
    r = requests.get(term)
    content = r.json()
    return content
def data_grab_song(dataset):
    '''
    Takes the information from the returned song content and finds the desired information.
    Once the information is found, it is added to the corresponding list, and returned.
    '''
    title_list = []
    artist_list = []
    date_list = []
    genre_list = []
    for item in dataset['feed']['entry']:
        title_list.append(item['im:name']['label'])
        artist_list.append(item['im:artist']['label'])
        date_list.append(item['im:price']['label'])
        genre_list.append(item['category']['attributes']['term'])
    return ('song', title_list, artist_list, date_list, genre_list)
def data_grab_album(dataset):
    '''
    Takes the information from the returned album content and finds the desired information.
    Once the information is found, it is added to the corresponding list, and returned.
    '''
    title_list = []
    artist_list = []
    date_list = []
    genre_list = []
    for item in dataset['feed']['entry']:
        title_list.append(item['im:name']['label'])
        artist_list.append(item['im:artist']['label'])
        date_list.append(item['im:price']['label'])
        genre_list.append(item['category']['attributes']['term'])
    return ('album', title_list, artist_list, date_list, genre_list)
def create_table():
    '''
    Creates the Music table in entertainment database
    '''
    conn, cur = db_setup()
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS Music(id, title TEXT, artist TEXT, price TEXT)''')
    conn.commit()
def db_count(database):
    '''
    returns a count for the amount of entries in the passed table
    '''
    conn, cur = db_setup()
    query = "SELECT * FROM " + database
    cur.execute(query)
    db_total = len(cur.fetchall())
    return db_total
def top_from_songs():
    '''
    Gets a list of genres and the corresponding numbers in the top 50 iTunes songs as long as the Music table
    has 100 entries in it.
    '''
    if db_count('Music') == 100:
        conn, cur = db_setup()
    
        query = '''
                SELECT COUNT(*), genre
                FROM EntertainmentLogistics
                WHERE media_type = 'song'
                GROUP BY genre
                '''
        data = cur.execute(query).fetchall()
        return data
    else:
        pass
def top_from_albums():
    '''
    Gets a list of genres and the corresponding numbers in the top 50 iTunes albums as long as the Music table
    has 100 entries in it.
    '''
    if db_count('Music') == 100:
        conn, cur = db_setup()
    
        query = '''
                SELECT COUNT(*), genre
                FROM EntertainmentLogistics
                WHERE media_type = 'album'
                GROUP BY genre
                '''
        data = cur.execute(query).fetchall()
        return data
    else:
        pass

def write_to_file():
    '''
    Checks to see if Music table has 100 entries. If True, gets list of genres and corresponding
    numbers as a list of tuples. Takes the tuples, formats and writes to a text file.
    '''
    if db_count('Music') == 100:   
        song_data = top_from_songs()
        album_data = top_from_albums()
        with open("calc.txt", "a") as file:
            file.write('Top 50 songs data:\n--------------------------------\n')
            for song in song_data:
                file.write(f'{song[0]*2}% {song[1]}\n--------------------------------\n')

            file.write('\n\nTop 50 albums data:\n')

            for album in album_data:
                file.write(f'{album[0]*2}% {album[1]}\n--------------------------------\n')
def visualize():
    '''
    Takes the tuples of album data and song data and breaks them into lists. Chooses a 
    distribution of colors from the Paired colorset from matplotlib colormaps, displays
    the pie chart, and adds a legend to the side.
    '''
    if db_count('Music') == 100:
        x_song = []
        y_song = []
        x_album = []
        y_album = []

        song_data = top_from_songs()
        album_data = top_from_albums()
        n = len(song_data)
        for item in song_data:
            y_song.append(item[0])
            x_song.append(item[1])
        for item in album_data:
            y_album.append(item[0])
            x_album.append(item[1])
        arr = np.array(y_song)
        cs=cm.Paired(np.arange(n)/n)
        f=plt.figure()
        plt.pie(arr,colors = cs, autopct='%1.0f%%', pctdistance=1.1, labeldistance=1.2)
        plt.tight_layout()
        plt.legend(x_song, bbox_to_anchor=(-0.25, .75), loc="center left")
        plt.title('Distribution of Genres in iTunes Top 50 songs')
        arr = np.array(y_album)
        cs=cm.Paired(np.arange(n)/n)
        f=plt.figure()
        plt.pie(arr,colors = cs, autopct='%1.0f%%', pctdistance=1.1, labeldistance=1.2)
        plt.tight_layout()
        plt.legend(x_album, bbox_to_anchor=(-0.25, .75), loc="center left")
        plt.title('Distribution of Genres in iTunes Top 50 albums')
        plt.show()


def db_fill_incremented():
    '''
    Checks to see the size of Music table from the database. Puts in portions of the dataset
    25 at a time depending on whether the table has 0, 25, 50, or 75 items in it, until the table
    has 100 entries. Also takes any genre with the word 'Christmas' and changes it to Holiday
    '''
    conn, cur = db_setup()
    query = "SELECT * FROM Music"
    cur.execute(query)
    db_total = len(cur.fetchall())
    if db_total == 0:
        current_id = db_count('EntertainmentLogistics')
        for i in range(0,25):
            
            current_id += 1
            sql = '''INSERT INTO EntertainmentLogistics(id, media_type, genre) VALUES(?,?,?)'''
            if ('Christmas' in data_grab_song(api_request(api_search2))[4][i]):
                cur.execute(sql, (current_id,data_grab_song(api_request(api_search2))[0], 'Holiday'))
                conn.commit() 
            else:    
                cur.execute(sql, (current_id,data_grab_song(api_request(api_search2))[0], data_grab_song(api_request(api_search2))[4][i]))
                conn.commit() 

            sql = '''INSERT INTO Music(id, title, artist, price) VALUES(?, ?, ?, ?)'''
       
            cur.execute(sql,(current_id, data_grab_song(api_request(api_search2))[1][i], data_grab_song(
                api_request(api_search2))[2][i], data_grab_song(api_request(api_search2))[3][i]))
            conn.commit()

    elif db_total == 25:
        current_id = db_count('EntertainmentLogistics')
        for i in range(25,50):
            current_id += 1
            sql = '''INSERT INTO EntertainmentLogistics(id, media_type, genre) VALUES(?,?,?)'''
            if ('Christmas' in data_grab_song(api_request(api_search2))[4][i]):
                cur.execute(sql, (current_id,data_grab_song(api_request(api_search2))[0], 'Holiday'))
                conn.commit() 
            else:    
                cur.execute(sql, (current_id,data_grab_song(api_request(api_search2))[0], data_grab_song(api_request(api_search2))[4][i]))
                conn.commit() 
            
            sql = '''INSERT INTO Music(id, title, artist, price) VALUES(?, ?, ?, ?)'''
       
            cur.execute(sql,(current_id, data_grab_song(api_request(api_search2))[1][i], data_grab_song(
                api_request(api_search2))[2][i], data_grab_song(api_request(api_search2))[3][i]))
            conn.commit()

    elif db_total == 50:
        current_id = db_count('EntertainmentLogistics')
        for i in range(0,25):
            current_id += 1
            sql = '''INSERT INTO EntertainmentLogistics(id, media_type, genre) VALUES(?,?,?)'''
            if ('Christmas' in data_grab_album(api_request(api_search1))[4][i]):
                cur.execute(sql, (current_id,data_grab_album(api_request(api_search1))[0], 'Holiday'))
                conn.commit()
            else:
                cur.execute(sql, (current_id,data_grab_album(api_request(api_search1))[0], data_grab_album(api_request(api_search1))[4][i]))
                conn.commit()

            sql = '''INSERT INTO Music(id, title, artist, price) VALUES(?, ?, ?, ?)'''
       
            cur.execute(sql,(current_id, data_grab_album(api_request(api_search1))[1][i], data_grab_album(
                api_request(api_search1))[2][i], data_grab_album(api_request(api_search1))[3][i]))
            conn.commit()

    elif db_total == 75:
        current_id = db_count('EntertainmentLogistics')
        for i in range(25,50):

            current_id += 1
            sql = '''INSERT INTO EntertainmentLogistics(id, media_type, genre) VALUES(?,?,?)'''
            if ('Christmas' in data_grab_album(api_request(api_search1))[4][i]):
                cur.execute(sql, (current_id,data_grab_album(api_request(api_search1))[0], 'Holiday'))
                conn.commit()
            else:
                cur.execute(sql, (current_id,data_grab_album(api_request(api_search1))[0], data_grab_album(api_request(api_search1))[4][i]))
                conn.commit()

            sql = '''INSERT INTO Music(id, title, artist, price) VALUES(?, ?, ?, ?)'''
       
            cur.execute(sql,(current_id, data_grab_album(api_request(api_search1))[1][i], data_grab_album(
                api_request(api_search1))[2][i], data_grab_album(api_request(api_search1))[3][i]))
            conn.commit()

def main():
    db_setup()
    create_table()
    db_fill_incremented()
    write_to_file()
    visualize()

if __name__ == "__main__":
    main()
