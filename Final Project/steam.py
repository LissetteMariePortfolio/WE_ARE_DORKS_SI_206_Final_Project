
import requests
import praw
import sqlite3
import plotly.express as px
import pandas as panda
from IPython.display import display


def api_setup():
    reddit = praw.Reddit(
    client_id="wtbjFJwLxqFu2-iC9JOqIg",
    client_secret="kKtX_A560IxAEGUVpe1woVJxaEn9TA",
    username = "StardustNyako",
    password = "22ruM@yu5h!!D35u",
    user_agent="omegadorks"
    )
    return reddit

def set_up_database():
    sql_connection = sqlite3.connect('reddit.db') 
    sql_cursor = sql_connection.cursor()
    return sql_connection, sql_cursor

def makeSubredditTable(sql_connection, sql_cursor):
    sql_cursor.execute("DROP TABLE IF EXISTS FirstSubreddit")
    sql_cursor.execute("DROP TABLE IF EXISTS SecondSubreddit")
    sql_cursor.execute('''CREATE TABLE IF NOT EXISTS FirstSubreddit (id INTEGER PRIMARY KEY, content_type TEXT, Title TEXT, Upvotes INTEGER, Comments INTEGER)''')
    sql_cursor.execute('''CREATE TABLE IF NOT EXISTS SecondSubreddit (id INTEGER PRIMARY KEY, content_type TEXT, Title TEXT, Upvotes INTEGER, Comments INTEGER)''')

    sql_connection.commit()
    


#I want to join subreddit tables. 
#Make new function , use that to combine two categories
#How to take 

def access_api(sub_reddit,reddit, new = False, hot = False, rising = False, top = False):
    counter = 0
    for category in [new, hot, rising, top]:
        if category == True:
            counter += 1
    if counter != 2:
        print("Sorry, you must choose 2 categories!")
        return None
    subreddit = reddit.subreddit(sub_reddit)
    first = False
    
    if new == True:
        chosen_threads = subreddit.new(limit=25)
        first = True
    elif hot == True and first == False:
        chosen_threads = subreddit.hot(limit=25)
        first = True
    elif hot == True and first == True:
        second_chosen_threads = subreddit.hot(limit=25)
    elif rising == True and first == False:
        chosen_threads = subreddit.rising(limit=25)
    elif rising == True and first == True:
        second_chosen_threads = subreddit.rising(limit=25)    
    elif top == True:
        second_chosen_threads = subreddit.top(limit=25) 
    else:
        print("Sorry, you must choose 2 categories!")
        return None 
    return chosen_threads, second_chosen_threads 
    
    #put what you need in lists
   
    #Make function!!
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

    
def fill_table(sql_connection, sql_cursor, first_data_dict, second_data_dict):
    counter = 0
    first_id_numbs = 240
    second_id_numbs = 320
    
    for entry in range(0,len(first_data_dict["Titles"]) - 1):
        sql_cursor.execute("INSERT INTO FirstSubreddit (id, content_type, Title, Upvotes, Comments) VALUES (?,?,?,?,?)", (first_id_numbs, "Reddit Post", first_data_dict["Titles"][counter], first_data_dict["Upvote Totals"][counter], first_data_dict["Comment Totals"][counter]))
        sql_cursor.execute("INSERT INTO SecondSubreddit (id, content_type, Title, Upvotes, Comments) VALUES (?,?,?,?,?)", (second_id_numbs, "Reddit Post", second_data_dict["Titles"][counter], second_data_dict["Upvote Totals"][counter], second_data_dict["Comment Totals"][counter]))

        sql_connection.commit()
        counter += 1
        first_id_numbs += 1
        second_id_numbs += 1
    
#Make a list of subreddits, 
#Get the number of comments and upvotes,
#Find avg upvotes and avg comments for each of the subreddits
#Make plot based on these averages (make list of these totals)
   
def calc_top_from_category(sql_connection, sql_cursor):
    subreddit_list = ["movies", "MovieSuggestions", ]
    upnote_average = sql_cursor.execute("SELECT AVG(Upvotes) FROM FirstSubreddit")
    sql_connection.commit()
    comment_number_average = sql_cursor.execute("SELECT AVG(Comments) FROM FirstSubreddit")
    sql_connection.commit()
    

def make_plotly_graphic(data_dict):
  
    fig = px.scatter(x=data_dict["Upvote Totals"], y=data_dict["Comment Totals"])
    fig.show()

    

#Tentative Deadline December 5th for code


def main():
    api_prep = api_setup()
    sql_connection,sql_cursor = set_up_database()
    makeSubredditTable(sql_connection, sql_cursor)
    #2 booleans must be set as true!
    first_subreddit, second_subreddit = access_api("uofm",api_prep, False, True, False, True)
    first_dictionary = make_data_dic(first_subreddit)
    second_dictionary = make_data_dic(second_subreddit)
    first_data_dict = {}
    second_data_dict = {}
    fill_table(sql_connection, sql_cursor,first_data_dict, second_data_dict)


if __name__ == "__main__":
    main()

'''
Notes:
Need a commin column (medium?) in each table stating whether this is a game, song, or movie
'''
