
1 of 17,372
new
Inbox

Lissette Ramos <liramos@umich.edu>
Attachments
5:10 PM (2 minutes ago)
to me


Attachments area
Compose:
Teammates are hard to be reach
MinimizePop-outClose
import praw
import sqlite3
import plotly.graph_objects as go
import csv
from pprint import pprint
import requests
import sqlite3
import json
import matplotlib.pyplot as plt
import numpy as np
from requests import api
from bs4 import BeautifulSoup
import pandas as pd
api_search1 = 'http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/ws/RSS/topalbums/limit=50/json'
api_search2 = 'http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/ws/RSS/topsongs/limit=50/json'
URLS = ["https://www.imdb.com/search/title/?year=2021&title_type=feature&", "https://www.imdb.com/search/title/?title_type=feature&year=2021-01-01,2021-12-31&start=51&ref_=adv_nxt",
        "https://www.imdb.com/search/title/?title_type=feature&year=2021-01-01,2021-12-31&start=51&ref_=adv_nxt"]
MAX_COUNT = 100
LIMIT = 25
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
    # Access API / Set up access
    # Set up database
    # Make cur object
    # Make con object
    # Set up soup
    connection = sqlite3.connect('entertainment.db')
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
    for item in dataset['feed']['entry']:
        title_list.append(item['im:name']['label'])
        artist_list.append(item['im:artist']['label'])
        date_list.append(item['im:price']['label'])
        genre_list.append(item['category']['attributes']['term'])
    return ('song', title_list, artist_list, date_list, genre_list)
def data_grab_album(dataset):
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
    conn, cur = db_setup()
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS Music(id, title TEXT, artist TEXT, price TEXT, genre TEXT)''')
    conn.commit()
def db_count():
    conn, cur = db_setup()
    query = "SELECT * FROM Music"
    cur.execute(query)
    db_total = len(cur.fetchall())
    return db_total
def top_from_category():
    conn, cur = db_setup()
    query = '''
            SELECT COUNT(*), genre
            FROM Music
            GROUP BY genre
            '''
    data = cur.execute(query).fetchall()
    return data
def write_to_file():
    data = top_from_category()
    with open("calc.txt", "w") as file:
        for item in data:
            file.write(f"{item[0]/100}% {item[1]}")
def visualize(data):
    x = []
    y = []
    for item in data:
        y.append(item[0])
        x.append(item[1])
    arr = np.array(y)
    plt.pie(arr, autopct='%1.0f%%', pctdistance=1.1, labeldistance=1.2)
    plt.tight_layout()
    plt.legend(x, bbox_to_anchor=(-0.25, .75), loc="center left")
    plt.title('Distribution of Genres in iTunes Top 100')
    plt.show()
def db_fill_incremented(id_number):
    conn, cur = db_setup()
    query = "SELECT * FROM Music"
    cur.execute(query)
    db_total = len(cur.fetchall())
    if db_total == 0:
        rows = []
        for i in range(0, 25):
            rows.append((data_grab_song(api_request(api_search2))[0], data_grab_song(api_request(api_search2))[1][i], data_grab_song(
                api_request(api_search2))[2][i], data_grab_song(api_request(api_search2))[3][i], data_grab_song(api_request(api_search2))[4][i]))
        sql = '''INSERT INTO Music(id, title, artist, price, genre) VALUES(?, ?, ?, ?, ?)'''
        for row in rows:
            cur.execute(sql, row)
            conn.commit()
    elif db_total == 25:
        rows = []
        for i in range(25, 50):
            rows.append((data_grab_song(api_request(api_search2))[0], data_grab_song(api_request(api_search2))[1][i], data_grab_song(
                api_request(api_search2))[2][i], data_grab_song(api_request(api_search2))[3][i], data_grab_song(api_request(api_search2))[4][i]))
        sql = '''INSERT INTO Music(id, title, artist, price, genre) VALUES(?, ?, ?, ?, ?)'''
        for row in rows:
            cur.execute(sql, row)
            conn.commit()
    elif db_total == 50:
        rows = []
        for i in range(0, 25):
            rows.append((data_grab_album(api_request(api_search1))[0], data_grab_album(api_request(api_search1))[1][i], data_grab_album(
                api_request(api_search1))[2][i], data_grab_album(api_request(api_search1))[3][i], data_grab_album(api_request(api_search1))[4][i]))
        sql = '''INSERT INTO Music(id, title, artist, price, genre) VALUES(?, ?, ?, ?, ?)'''
        for row in rows:
            cur.execute(sql, row)
            conn.commit()
    elif db_total == 75:
        rows = []
        for i in range(25, 50):
            rows.append((data_grab_album(api_request(api_search1))[0], data_grab_album(api_request(api_search1))[1][i], data_grab_album(
                api_request(api_search1))[2][i], data_grab_album(api_request(api_search1))[3][i], data_grab_album(api_request(api_search1))[4][i]))
        sql = '''INSERT INTO Music(id, title, artist, price, genre) VALUES(?, ?, ?, ?, ?)'''
        for row in rows:
            cur.execute(sql, row)
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
    sql_cursor.execute('''CREATE TABLE IF NOT EXISTS EntertainmentLogistics(id INT PRIMARY KEY,media_type TEXT)''')
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
    if numb_of_entries == 50:
        
        current_subreddit = reddit.subreddit(second_sub_reddit)
        id_number = 51
    if numb_of_entries == 100:
        #25 50 75 100 125 150 175 200
        
        current_subreddit = reddit.subreddit(third_sub_reddit)
        id_number = 101
    if numb_of_entries == 150:
        
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
def main():
    primary_id = 1
    api_prep = api_setup()
    sql_connection, sql_cursor = set_up_database()
    make_subreddit_table(sql_connection, sql_cursor)
    hot_subreddit, primary_id = access_api(sql_cursor, sql_connection, "movies", "badMovies", "Music", "kpop", api_prep)
    first_dictionary = make_data_dic(hot_subreddit)
    fill_table(sql_connection, sql_cursor, first_dictionary,primary_id)
    make_plotly_graphic(sql_connection, sql_cursor)
    db_setup()
    create_table()
    primary_id = db_fill_incremented(primary_id)
    visualize(top_from_category())
    write_to_file()
    make_a_join()
if __name__ == "__main__":
    main()
