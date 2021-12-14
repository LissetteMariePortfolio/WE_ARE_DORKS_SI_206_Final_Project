import praw
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
URLS = ["https://www.imdb.com/search/title/?year=2021&title_type=feature&", "https://www.imdb.com/search/title/?title_type=feature&year=2021-01-01,2021-12-31&start=51&ref_=adv_nxt",
        "https://www.imdb.com/search/title/?title_type=feature&year=2021-01-01,2021-12-31&start=51&ref_=adv_nxt"]
MAX_COUNT = 100
LIMIT = 25


def set_conn():
    conn = sqlite3.connect('entertainment.db') 
    cursor = conn.cursor()
    return conn, cursor
def kashaf_create_table():
    conn,c=set_conn()
    c.execute('''CREATE TABLE IF NOT EXISTS movies(id INT PRIMARY KEY, title TEXT, run_time TEXT, genre TEXT,rating REAL)''')
    conn.commit()
    conn.close()
    return True
def get_db_count():
    conn,c=set_conn()
    c.execute("SELECT COUNT(*) from movies")
    return c.fetchone()[0]
def add_to_database(title,genre,run_time,rating):
    conn,c=set_conn()
    st="""INSERT INTO movies(title,run_time,genre,rating) VALUES (?,?,?,?);"""
    data=(title,genre,run_time,rating)
    c.execute(st,data)
    conn.commit()
    conn.close()
    return True
def api_bs_setup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup

def kashaf_access_api():
    movies=[]
    for url in URLS:
        soup=api_bs_setup(url)
        res=soup.find(class_="lister-list")
        for movie in res.find_all(class_="lister-item"):
            title=movie.find(class_="lister-item-content").find("a").text.strip()
            genre=movie.find(class_="genre").text.strip()
            r_t=movie.find(class_="runtime")
            r_time= r_t.text.strip() if r_t else "0"
            try:
                rating=movie.find(class_="ratings-imdb-rating").find("strong").text.strip()
            except:
                rating=0
            movies.append([title,genre,r_time,rating])
    count=get_db_count()
    end_count=count+LIMIT
    for i in movies[count:end_count]:
        add_to_database(*i)
def get_data():
  conn,c=set_conn()
  c.execute("SELECT * FROM movies;")
  return c.fetchall()
def calc_top_from_category():
    data=get_data()
    genre={}
    for movie in data:
      genres=movie[2]
      for gen in genres.split(", "):
        if gen in genre:
          genre[gen]+=1
        else:
          genre[gen]=1
    return genre
    

def kashaf_make_plotly_graphic():
    if db_count("movies") == 100:
        genre=calc_top_from_category()
        fig = go.Figure(go.Bar(
                    y=list(genre.values()),
                    x=list(genre.keys()),
                    orientation='v'))
        fig.update_layout(
        title="The Breakdown of Genres of Movies in IMDb's Top 100 ",
        xaxis_title="Number of Movies",
        yaxis_title="Movie Genre",
        font=dict(
                family="Courier New, monospace",
                size=18,
                color="#7f7f7f"
        )
    )

        fig.show()



def set_up_database():
    sql_connection = sqlite3.connect('entertainment.db')
    sql_cursor = sql_connection.cursor()
    return sql_connection, sql_cursor
def api_bs_setup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup
def api_setup():
    # Lissette API
    reddit = praw.Reddit(
        client_id="wtbjFJwLxqFu2-iC9JOqIg",
        client_secret="kKtX_A560IxAEGUVpe1woVJxaEn9TA",
        username="StardustNyako",
        password="22ruM@yu5h!!D35u",
        user_agent="omegadorks"
    )
    return reddit

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

def api_setup():
    reddit = praw.Reddit(
        client_id="wtbjFJwLxqFu2-iC9JOqIg",
        client_secret="kKtX_A560IxAEGUVpe1woVJxaEn9TA",
        username="StardustNyako",
        password="22ruM@yu5h!!D35u",
        user_agent="omegadorks"
    )
    return reddit
def set_up_database():
    '''
     No input, just making my sqlite cursor and connection objects for the
     reddit API that then get used in the other reddit API functions

    '''
    sql_connection = sqlite3.connect('entertainment.db')
    sql_cursor = sql_connection.cursor()
    return sql_connection, sql_cursor
def make_subreddit_table(sql_connection, sql_cursor):
    '''
    This creates the SubredditHot table (Posts are collected from the hot 
    section of each subreddit accessed)
    '''
    sql_cursor.execute(
        '''CREATE TABLE IF NOT EXISTS SubredditHot (id INTEGER PRIMARY KEY,Title TEXT, Upvotes INTEGER, Comments INTEGER)''')
    sql_connection.commit()
    sql_cursor.execute('''CREATE TABLE IF NOT EXISTS EntertainmentLogistics(id INT PRIMARY KEY,media_type TEXT, genre TEXT)''')
    sql_connection.commit()
# I want to join subreddit tables.
# Make new function , use that to combine two categories
# How to take
def access_api(sql_cursor, sql_connection, first_sub_reddit, second_sub_reddit, third_sub_reddit, fourth_sub_reddit, reddit):
    '''
    It takes in the sqlite objects, the names of the four subreddits we want
    to get data from, and the reddit API object. What it does is it will count
    how many rows are in the SubredditHot table currently. Depending on how
    many entries there are, that determines which subreddit to draw 25 posts
    from. It then changes the id number to the first number in that
    corresponding range of numbers. The 25 posts and id number is returned
    '''
    
    sql_cursor.execute("SELECT * FROM SubredditHot")
    numb_of_entries = len(sql_cursor.fetchall())
    sql_connection.commit()
    id_number = 0
    
    current_subreddit = ""
    if numb_of_entries == 0:
       
        current_subreddit = reddit.subreddit(first_sub_reddit)
        id_number = 1
    if numb_of_entries == 25:
        
        current_subreddit = reddit.subreddit(second_sub_reddit)
        id_number = 51
    if numb_of_entries == 50:
        #25 50 75 100 125 150 175 200
        
        current_subreddit = reddit.subreddit(third_sub_reddit)
        id_number = 101
    if numb_of_entries == 75:
        
        current_subreddit = reddit.subreddit(fourth_sub_reddit)
        id_number = 151
        # zip file for github?
    hot_threads = current_subreddit.hot(limit=26)
    # Alright, so now our API is set up to populate properly!!
    return hot_threads, id_number
def make_data_dic(chosen_threads):
    '''
     This takes the set of 25 posts and  makes a dictionary with the   wanted 
     data by accessing each post object and returns that dictionary.

    '''
    title = []
    upvote_totals = []
    comment_totals = []
    for submission in chosen_threads:
        title.append(submission.title)
        upvote_totals.append(submission.ups)
        comment_totals.append(len(submission.comments.list()))
    data_dict = {}
    data_dict["Titles"] = title
    data_dict["Upvote Totals"] = upvote_totals
    data_dict["Comment Totals"] = comment_totals
    return data_dict
def fill_table(sql_connection, sql_cursor, first_data_dict, id_number):
    '''
    Given the sqlite objects so you can use the data from the dictionary to
    insert the needed data of each post into the database, ensuring the proper
    id number is used according to where the post lies in the dictionary
    (see make_data_dic). This then finds the average number of upvotes and
    number of comments each post in the database so far received and prints
    them out. 
    '''
    counter = 0
    for entry in range(0, len(first_data_dict["Titles"]) - 1):
        sql_cursor.execute("INSERT INTO SubredditHot (id,Title, Upvotes, Comments) VALUES (?,?,?,?)", (id_number, first_data_dict["Titles"][counter], first_data_dict["Upvote Totals"][counter], first_data_dict["Comment Totals"][counter]))
        sql_connection.commit() 
        sql_cursor.execute("INSERT INTO EntertainmentLogistics(id, media_type) VALUES (?,?)", (id_number, "Reddit Post"))
        sql_connection.commit()
        
        counter += 1
        id_number += 1
    sql_cursor.execute("SELECT Upvotes FROM SubredditHot")
    all_upvotes = sql_cursor.fetchall()
    sql_connection.commit()
    sql_cursor.execute("SELECT Comments FROM SubredditHot")   
    all_comments = sql_cursor.fetchall()
    sql_connection.commit()
    total_upvotes = 0
    total_comments = 0
    for row in all_upvotes:
        total_upvotes += row[0]
    for row in all_comments:
        total_comments += row[0]
    avg_upvotes = total_upvotes / 100
    avg_comments = total_comments / 100
    print("The average number of upvotes per post amongst all four subreddits is " + 
            str(int(avg_upvotes)))
    print("The average number of comments per post amongst all four subreddits is " + 
            str(int(avg_comments)))
def make_plotly_graphic(sql_connection, sql_cursor):
    '''
    Used the Reddit API SQL objects to make a graph to show the correlation
    between the number of upvotes and reddit comment
    '''
    if db_count("SubredditHot") == 100:
        sql_cursor.execute("SELECT Upvotes FROM SubredditHot")
        subreddit_upvotes = sql_cursor.fetchall()
        sql_connection.commit()
        sql_cursor.execute("SELECT Comments FROM SubredditHot")
        subreddit_comments = sql_cursor.fetchall()
        sql_connection.commit()
        upvote_numbers = []
        comment_totals = []
        for numb in range(0, len(subreddit_comments) - 1):
            upvote_numbers.append(subreddit_upvotes[numb][0])
            comment_totals.append(subreddit_comments[numb][0])
        plot = go.Figure(data=[go.Scatter(
            x=upvote_numbers,
            y=comment_totals,
            mode="markers",) 
        ])
        plot.update_layout(
            title="Comparison of Number of Upvotes Compared To Number Of Comments",
            xaxis_title="Number of Upvotes",
            yaxis_title="Number Of Comments",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="#7f7f7f"
            )
        )
        plot.update_yaxes(range=[0, 600])
        plot.update_xaxes(range=[0, 600])
        plot.update_traces(marker=dict(color='red'))
        plot.show()
def media_types(sql_connection, sql_cursor):
    sql_cursor.execute("SELECT SubredditHot.id,SubredditHot.Title, EntertainmentLogistics.media_type FROM SubredditHot INNER JOIN EntertainmentLogistics ON SubredditHot.id = EntertainmentLogistics.id")
    sql_connection.commit()
    reddit_pairings = sql_cursor.fetchall()
    sql_cursor.execute("SELECT Music.id, Music.title, EntertainmentLogistics.media_type, EntertainmentLogistics.genre FROM Music INNER JOIN EntertainmentLogistics ON music.id = EntertainmentLogistics.id")
    sql_connection.commit()
    music_pairings = sql_cursor.fetchall()
    # Uncomment below if you wish to see the results of the selection query
    '''
    for pairing in range(0,len(reddit_pairings) - 1):
        print(reddit_pairings[pairing])
        print(music_pairings[pairing])
    '''

def main():
    kashaf_create_table()
    kashaf_access_api()
    kashaf_make_plotly_graphic()
    
    primary_id = 1
    api_prep = api_setup()
    sql_connection, sql_cursor = set_up_database()
    make_subreddit_table(sql_connection, sql_cursor)
    hot_subreddit, primary_id = access_api(sql_cursor, sql_connection, "movies", "badMovies", "Music", "kpop", api_prep)
    first_dictionary = make_data_dic(hot_subreddit)
    fill_table(sql_connection, sql_cursor, first_dictionary,primary_id)
    make_plotly_graphic(sql_connection, sql_cursor)
    set_up_database()       
    db_setup()
    create_table()
    db_fill_incremented()
    write_to_file()
    visualize()
    media_types(sql_connection, sql_cursor)

if __name__ == "__main__":
    main()
