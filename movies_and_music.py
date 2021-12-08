def set_up_database():
    sql_connection = sqlite3.connect('entertainment.db')
    sql_cursor = sql_connection.cursor()
    return sql_connection, sql_cursor
  
    def api_setup(term,url):
      #Lissette API
        reddit = praw.Reddit(
        client_id="wtbjFJwLxqFu2-iC9JOqIg",
        client_secret="kKtX_A560IxAEGUVpe1woVJxaEn9TA",
        username="StardustNyako",
        password="22ruM@yu5h!!D35u",
        user_agent="omegadorks"
    )
        
    #Will API    
    r = requests.get(term)
    content = r.json()
    
    #Kashaf's API
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    
    return reddit,  content, soup
  
 
def main():
    sql_connection, sql_cursor = set_up_database()
    api_prep = api_setup()
    makeSubredditTable(sql_connection, sql_cursor)
    hot_subreddit, new_subreddit,subreddit_name, id_number = access_api(sql_cursor,sql_connection,"movies", "badMovies","Music", "kpop", api_prep)
    first_dictionary = make_data_dic(hot_subreddit)
    second_dictionary = make_data_dic(new_subreddit)
    fill_table(sql_connection, sql_cursor, first_dictionary, second_dictionary,subreddit_name, id_number)
    
    
    
    make_plotly_graphic(sql_connection, sql_cursor)


if __name__ == "__main__":
    main()
