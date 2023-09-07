#This is part of a group project, this reddit code was made entirely by me, Lissette Ramos

import praw # Python Reddit API Wrapper
import sqlite3 # SQL usage within Python
import plotly.graph_objects as go # Let's me make charts via Python
import csv


# Set up the API, user account credentials are needed for any program run in case you want to make changes on the reddit site 
def api_setup():
    reddit = praw.Reddit(
        client_id="wtbjFJwLxqFu2-iC9JOqIg",
        client_secret="kKtX_A560IxAEGUVpe1woVJxaEn9TA",
        username="",#Put in a valid Reddit username
        password="",#Put in a valid Reddit password
        user_agent="omegadorks"
    )
    return reddit
# Setting up database and SQL objects

def set_up_database():
    sql_connection = sqlite3.connect('reddit.db')
    sql_cursor = sql_connection.cursor()
    return sql_connection, sql_cursor

# Making tables during first run through 

def makeSubredditTable(sql_connection, sql_cursor):
    
    sql_cursor.execute(
        '''CREATE TABLE IF NOT EXISTS SubredditHot (id INTEGER PRIMARY KEY, content_type TEXT, Title TEXT, Upvotes INTEGER, Comments INTEGER)''')
    sql_cursor.execute(
        '''CREATE TABLE IF NOT EXISTS SubredditNew (id INTEGER PRIMARY KEY, content_type TEXT, Title TEXT, Upvotes INTEGER, Comments INTEGER)''')

    sql_connection.commit()
   

# There are four subreddit groups entered into the function, the hot and new threads of two subreddits. Each of the four groups will have the top 25 threads currently
# in that category into the database ait the id number incremented and appended accordingly
def access_api(sql_cursor,sql_connection,first_sub_reddit, second_sub_reddit,third_sub_reddit,fourth_sub_reddit, reddit):
    sql_cursor.execute("SELECT * FROM SubredditHot")
    numb_of_entries = len(sql_cursor.fetchall())
    sql_connection.commit()
    subreddit_name = ""
    id_number= 1
    if numb_of_entries == 0:
        subreddit_name = first_sub_reddit
        current_subreddit = reddit.subreddit(first_sub_reddit)
        id_number = 1
    if numb_of_entries == 25:
        subreddit_name = second_sub_reddit
        current_subreddit = reddit.subreddit(second_sub_reddit) 
        id_number = 26
    if numb_of_entries == 50:
        subreddit_name = third_sub_reddit
        current_subreddit = reddit.subreddit(third_sub_reddit)   
        id_number = 51
    if numb_of_entries == 75:
        subreddit_name = fourth_sub_reddit
        current_subreddit = reddit.subreddit(fourth_sub_reddit) 
        id_number = 76
        #zip file for github?
        
        
    hot_threads = current_subreddit.hot(limit=26)
    new_threads = current_subreddit.new(limit=26)
    
    return hot_threads, new_threads,subreddit_name, id_number

# Data dictionaries are made, filled with the number of upvote and number of comments to put in the SQL database tables 
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

# Dictionaries used to fill tables
def fill_table(sql_connection, sql_cursor, first_data_dict, second_data_dict, subreddit_name, id_number):
    counter = 0

    

    for entry in range(0, len(first_data_dict["Titles"]) - 1):
        sql_cursor.execute("INSERT INTO SubredditHot (id, content_type, Title, Upvotes, Comments) VALUES (?,?,?,?,?)", (id_number, "Reddit Post",
                                                                                                                          first_data_dict["Titles"][counter], first_data_dict["Upvote Totals"][counter], first_data_dict["Comment Totals"][counter]))
        sql_cursor.execute("INSERT INTO SubredditNew (id, content_type, Title, Upvotes, Comments) VALUES (?,?,?,?,?)", (id_number, "Reddit Post",
                                                                                                                           second_data_dict["Titles"][counter], second_data_dict["Upvote Totals"][counter], second_data_dict["Comment Totals"][counter]))

        sql_connection.commit()
        counter += 1
        id_number += 1
    
    sql_cursor.execute("SELECT * FROM SubredditHot")
    table_view = sql_cursor.fetchall()
    entry_numb = len(table_view)
    if entry_numb == 100:
        sql_cursor.execute("SELECT SubredditHot.Upvotes, SubredditNew.Upvotes FROM SubredditHot INNER JOIN SubredditNew ON SubredditHot.id = SubredditNew.id ")
        all_upvotes = sql_cursor.fetchall()
        sql_connection.commit()
        sql_cursor.execute("SELECT SubredditHot.Comments, SubredditNew.Comments FROM SubredditHot INNER JOIN SubredditNew ON SubredditHot.id = SubredditNew.id ")
        all_comments = sql_cursor.fetchall()
        sql_connection.commit()
       # Average of number of comments and upvotes of different threads taken and entered into a file
        total_upvotes = 0
        total_comments = 0
        for row in all_upvotes:
            total_upvotes += row[0]
        for row in all_comments:
            total_comments += row[0]  
    
        avg_upvotes = total_upvotes / 100
        avg_comments = total_comments / 100
    
        upvote_line = "The average number of upvotes per post amongst all four subreddits is " + str(int(avg_upvotes))
        comment_line = "The average number of comments per post amongst all four subreddits is " + str(int(avg_comments))
        file_line_list = [upvote_line,comment_line]
    
       
        with open('reddit.csv', 'w') as reddit_csv:
            for statement in file_line_list:
                reddit_csv.write(statement)
                reddit_csv.write("\n")


# Graphs made to observe the relation of number of upvotes and number of comments in a post

def make_plotly_graphic(sql_connection, sql_cursor):
    sql_cursor.execute("SELECT Upvotes FROM SubredditHot")
    first_subreddit_upvotes = sql_cursor.fetchall()
    sql_connection.commit()
    sql_cursor.execute("SELECT Upvotes FROM SubredditNew")
    second_subreddit_upvotes = sql_cursor.fetchall()
    sql_connection.commit()
    sql_cursor.execute("SELECT Comments FROM SubredditHot")
    first_subreddit_comments = sql_cursor.fetchall()
    sql_connection.commit()
    sql_cursor.execute("SELECT Comments FROM SubredditNew")
    second_subreddit_comments = sql_cursor.fetchall()
    sql_connection.commit()
    all_upvotes = first_subreddit_upvotes + second_subreddit_upvotes
    all_comments = first_subreddit_comments + second_subreddit_comments
    upvote_numbers = []
    comment_totals = []
    for numb in range(0, len(all_comments) - 1):
        upvote_numbers.append(all_upvotes[numb][0])
        comment_totals.append(all_comments[numb][0])
    plot = go.Figure(data=[go.Scatter(
    x = upvote_numbers,
    y = comment_totals,
    mode = "markers",) 
    
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
    plot.update_yaxes(range=[0,600])
    plot.update_traces(marker=dict(color='red'))
    plot.show()
    

# Driver

def main():
    api_prep = api_setup()
    sql_connection, sql_cursor = set_up_database()
    makeSubredditTable(sql_connection, sql_cursor)
    hot_subreddit, new_subreddit,subreddit_name, id_number = access_api(sql_cursor,sql_connection,"movies", "badMovies","Music", "kpop", api_prep)
    first_dictionary = make_data_dic(hot_subreddit)
    second_dictionary = make_data_dic(new_subreddit)
    fill_table(sql_connection, sql_cursor, first_dictionary, second_dictionary,subreddit_name, id_number)
    
    
    
    make_plotly_graphic(sql_connection, sql_cursor)


if __name__ == "__main__":
    main()


