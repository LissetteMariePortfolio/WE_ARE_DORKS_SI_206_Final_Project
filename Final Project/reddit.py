

import praw
import sqlite3
import plotly.graph_objects as go
import csv



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
    sql_connection = sqlite3.connect('reddit.db')
    sql_cursor = sql_connection.cursor()
    return sql_connection, sql_cursor


def makeSubredditTable(sql_connection, sql_cursor):
    sql_cursor.execute("DROP TABLE IF EXISTS FirstSubreddit")
    sql_cursor.execute("DROP TABLE IF EXISTS SecondSubreddit")
    sql_cursor.execute(
        '''CREATE TABLE IF NOT EXISTS FirstSubreddit (id INTEGER PRIMARY KEY, content_type TEXT, Title TEXT, Upvotes INTEGER, Comments INTEGER)''')
    sql_cursor.execute(
        '''CREATE TABLE IF NOT EXISTS SecondSubreddit (id INTEGER PRIMARY KEY, content_type TEXT, Title TEXT, Upvotes INTEGER, Comments INTEGER)''')

    sql_connection.commit()
   

# I want to join subreddit tables.
# Make new function , use that to combine two categories
# How to take

def access_api(first_sub_reddit, second_sub_reddit, reddit):

    first_subreddit = reddit.subreddit(first_sub_reddit)
    second_subreddit = reddit.subreddit(second_sub_reddit)
    first_chosen_threads = first_subreddit.hot(limit=25)
    second_chosen_threads = second_subreddit.hot(limit=25)

    return first_chosen_threads, second_chosen_threads


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


def fill_table(sql_connection, sql_cursor, first_data_dict, second_data_dict, first_sub_reddit, second_sub_reddit):
    counter = 0

    id_numbs = 320

    for entry in range(0, len(first_data_dict["Titles"]) - 1):
        sql_cursor.execute("INSERT INTO FirstSubreddit (id, content_type, Title, Upvotes, Comments) VALUES (?,?,?,?,?)", (id_numbs, "Reddit Post",
                                                                                                                          first_data_dict["Titles"][counter], first_data_dict["Upvote Totals"][counter], first_data_dict["Comment Totals"][counter]))
        sql_cursor.execute("INSERT INTO SecondSubreddit (id, content_type, Title, Upvotes, Comments) VALUES (?,?,?,?,?)", (id_numbs, "Reddit Post",
                                                                                                                           second_data_dict["Titles"][counter], second_data_dict["Upvote Totals"][counter], second_data_dict["Comment Totals"][counter]))

        sql_connection.commit()
        counter += 1
        id_numbs += 1
    
    sql_cursor.execute("SELECT Upvotes FROM FirstSubreddit")
    first_upvotes = sql_cursor.fetchall()
    sql_connection.commit()
    sql_cursor.execute("SELECT Upvotes FROM SecondSubreddit")
    second_upvotes = sql_cursor.fetchall()
    sql_connection.commit()
    sql_cursor.execute("SELECT Comments FROM FirstSubreddit")
    first_comments = sql_cursor.fetchall()
    sql_connection.commit()
    sql_cursor.execute("SELECT Comments FROM SecondSubreddit")
    second_comments = sql_cursor.fetchall()
    sql_connection.commit()
    first_total_upvotes = 0
    first_total_comments = 0
    second_total_upvotes = 0
    second_total_comments = 0
    first_avg_upvotes = 0
    first_avg_comments = 0
    second_avg_upvotes = 0
    second_avg_comments = 0
    for row in first_upvotes:
        first_total_upvotes += row[0]
    for row in first_comments:
        first_total_comments += row[0]  
    for row in second_upvotes:
        second_total_upvotes += row[0] 
    for row in second_comments:
        second_total_comments += row[0] 
    first_avg_upvotes = first_total_upvotes / counter
    first_avg_comments = first_total_comments / counter
    second_avg_upvotes = second_total_upvotes = second_total_upvotes / counter
    second_avg_comments = second_total_comments / counter
    first_upvote_line = "The average number of upvotes of the top 25 posts in " +  first_sub_reddit + " is " + str(int(first_avg_upvotes))
    first_comment_line = "The average number of comments of the top 25 posts in " +  first_sub_reddit + " is " + str(int(first_avg_comments))
    second_upvote_line = "The average number of upvotes of the top 25 posts in " +  second_sub_reddit + " is " + str(int(second_avg_upvotes))
    second_comment_line = "The average number of comments of the top 25 posts in " +  second_sub_reddit + " is " + str(int(second_avg_comments))

    file_line_list = [first_upvote_line,first_comment_line,second_upvote_line,second_comment_line]
    
    
    with open('reddit.csv', 'w') as reddit_csv:
        for statement in file_line_list:
            reddit_csv.write(statement)
            reddit_csv.write("\n")




def make_plotly_graphic(sql_connection, sql_cursor):
    sql_cursor.execute("SELECT Upvotes FROM FirstSubreddit")
    first_subreddit_upvotes = sql_cursor.fetchall()
    sql_connection.commit()
    sql_cursor.execute("SELECT Upvotes FROM SecondSubreddit")
    second_subreddit_upvotes = sql_cursor.fetchall()
    sql_connection.commit()
    sql_cursor.execute("SELECT Comments FROM FirstSubreddit")
    first_subreddit_comments = sql_cursor.fetchall()
    sql_connection.commit()
    sql_cursor.execute("SELECT Comments FROM SecondSubreddit")
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
    plot.update_yaxes(range=[0,600])
    plot.update_traces(marker=dict(color='red'))
    plot.show()
    

# Tentative Deadline December 5th for code


def main():
    api_prep = api_setup()
    sql_connection, sql_cursor = set_up_database()
    makeSubredditTable(sql_connection, sql_cursor)

    first_subreddit, second_subreddit = access_api("uofm", "anime", api_prep)
    first_dictionary = make_data_dic(first_subreddit)
    second_dictionary = make_data_dic(second_subreddit)

    fill_table(sql_connection, sql_cursor, first_dictionary, second_dictionary, "/r/uofm", "/r/anime")
    
    
    
    make_plotly_graphic(sql_connection, sql_cursor)


if __name__ == "__main__":
    main()

'''
Notes:
Need a commin column (medium?) in each table stating whether this is a game, song, or movie
'''
