
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





def set_conn():

    conn = sqlite3.connect('entertainment.db')

    cursor = conn.cursor()

    return conn, cursor





def make_table():

    conn, c = set_conn()

    c.execute('''CREATE TABLE IF NOT EXISTS movies(id INT PRIMARY KEY, title TEXT, genre TEXT,run_time TEXT, rating REAL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS EntertainmentLogistics(id INT PRIMARY KEY,media_type TEXT)''')

    conn.commit()

    conn.close()

    return True





def get_db_count():

    conn, c = set_conn()

    c.execute("SELECT COUNT(*) from movies")

    return c.fetchone()[0]





def add_to_database(title, genre, run_time, rating):

    conn, c = set_conn()

    

    st = """INSERT INTO movies(title,run_time,genre,rating) VALUES (?,?,?,?)"""

    data = (title, genre, run_time, rating)

    c.execute(st, data)

    conn.commit()

    conn.close()

    return True





def api_bs_setup(url):

    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")

    return soup





def reach_api():

    movies = []

    for url in URLS:

        soup = api_bs_setup(url)

        res = soup.find(class_="lister-list")

        for movie in res.find_all(class_="lister-item"):

            title = movie.find(

                class_="lister-item-content").find("a").text.strip()

            genre = movie.find(class_="genre").text.strip()

            r_t = movie.find(class_="runtime")

            r_time = r_t.text.strip() if r_t else "0"

            try:

                rating = movie.find(

                    class_="ratings-imdb-rating").find("strong").text.strip()

            except:

                rating = 0

            movies.append([title, genre, r_time, rating])

    count = get_db_count()

    end_count = count+LIMIT

    for i in movies[count:end_count]:

        add_to_database(*i)





def get_data():

    conn, c = set_conn()

    c.execute("SELECT * FROM movies")

    return c.fetchall()





def calc_top_from_category():

    data = get_data()

    genre = {}

    for movie in data:

        genres = movie[2]

        for gen in genres.split(", "):

            if gen in genre:

                genre[gen] += 1

            else:

                genre[gen] = 1

    return genre





def make_graphic():

    genre = calc_top_from_category()

    print(type(genre))

    pprint(genre)

    fig = go.Figure(go.Bar(

        y=list(genre.values()),

        x=list(genre.keys()),

        orientation='v'))



    fig.show()





def write_file():

    data = calc_top_from_category()

    with open("file.txt", "w") as file:

        for movie in data.items():

            file.write(f"{movie[0]} {movie[1]}\n")





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





def db_fill_incremented():

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

    sql_connection = sqlite3.connect('entertainment.db')

    sql_cursor = sql_connection.cursor()

    return sql_connection, sql_cursor





def makeSubredditTable(sql_connection, sql_cursor):



    sql_cursor.execute(

        '''CREATE TABLE IF NOT EXISTS SubredditHot (id INTEGER PRIMARY KEY,Title TEXT, Upvotes INTEGER, Comments INTEGER)''')

    



    sql_connection.commit()





# I want to join subreddit tables.

# Make new function , use that to combine two categories

# How to take



def access_api(sql_cursor, sql_connection, first_sub_reddit, second_sub_reddit, third_sub_reddit, fourth_sub_reddit, reddit):

    sql_cursor.execute("SELECT * FROM SubredditHot")

    numb_of_entries = len(sql_cursor.fetchall())

    sql_connection.commit()

    

    

    if numb_of_entries == 0:

        subreddit_name = first_sub_reddit

        current_subreddit = reddit.subreddit(first_sub_reddit)

        id_number = 320

    if numb_of_entries == 25:

        subreddit_name = second_sub_reddit

        current_subreddit = reddit.subreddit(second_sub_reddit)

        id_number = 346

    if numb_of_entries == 50:

        subreddit_name = third_sub_reddit

        current_subreddit = reddit.subreddit(third_sub_reddit)

        id_number = 372

    if numb_of_entries == 75:

        subreddit_name = fourth_sub_reddit

        current_subreddit = reddit.subreddit(fourth_sub_reddit)

        id_number = 397

        # zip file for github?



    hot_threads = current_subreddit.hot(limit=26)

    

    # Alright, so now our API is set up to populate properly!!

    return hot_threads, id_number





def make_data_dic(chosen_threads):

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

    counter = 0

   

    for entry in range(0, len(first_data_dict["Titles"]) - 1):

        sql_cursor.execute("INSERT INTO SubredditHot (id,Title, Upvotes, Comments) VALUES (?,?,?,?)", (id_number, first_data_dict["Titles"][counter], first_data_dict["Upvote Totals"][counter], first_data_dict["Comment Totals"][counter]))

        



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

    plot.update_traces(marker=dict(color='red'))

    plot.show()





def main():

    primary_id = 0

    

    make_table()

    reach_api()

    make_graphic()

    write_file()



    api_prep = api_setup()

    sql_connection, sql_cursor = set_up_database()

    makeSubredditTable(sql_connection, sql_cursor)

    hot_subreddit, id_number = access_api(sql_cursor, sql_connection, "movies", "badMovies", "Music", "kpop", api_prep)

    first_dictionary = make_data_dic(hot_subreddit)

    

    fill_table(sql_connection, sql_cursor, first_dictionary,id_number)



    make_plotly_graphic(sql_connection, sql_cursor)



    db_setup()

    create_table()

    db_fill_incremented()

    visualize(top_from_category())

    write_to_file()





if __name__ == "__main__":

    main()

