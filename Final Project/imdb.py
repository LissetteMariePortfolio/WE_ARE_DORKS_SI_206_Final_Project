import requests
from bs4 import BeautifulSoup
import sqlite3
import plotly.graph_objects as go
import pandas as pd

URL = "https://www.imdb.com/search/title/?year=2021&title_type=feature&"
MAX_COUNT=100
LIMIT = 25

def set_conn():
    conn = sqlite3.connect('imdb.db') 
    cursor = conn.cursor()
    return conn, cursor

def create_table():
    conn,c = set_conn()
    c.execute('''CREATE TABLE IF NOT EXISTS movies(id INT PRIMARY KEY, title TEXT, run_time TEXT, genre TEXT,rating REAL)''')
    conn.commit()
    conn.close()
    return True

def get_db_count():
    conn,c = set_conn()
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

def api_bs_setup():
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup

def access_api():
    soup=api_bs_setup()
    res=soup.find(class_="lister-list")
    db_count=get_db_count()
    count=0

    for movie in res.find_all(class_="lister-item"):
        if db_count==MAX_COUNT:
            return
        if count==(db_count+LIMIT):
            break
        if count<=db_count and db_count!=0:
            count+=1
            continue
        
        count+=1
        title=movie.find(class_="lister-item-content").find("a")
        genre=movie.find(class_="genre")
        r_time=movie.find(class_="runtime")
        try:
            rating=movie.find(class_="ratings-imdb-rating").find("strong").text.strip()
        except:
            rating=0
        add_to_database(title.text.strip(),genre.text.strip(),r_time.text.strip(),rating)
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
    

def make_plotly_graphic():
    genre=calc_top_from_category()
    fig = go.Figure(go.Bar(
                y=list(genre.values()),
                x=list(genre.keys()),
                orientation='v'))

    fig.show()

if __name__ == "__main__":
  create_table()
  access_api()
  make_plotly_graphic()

'''
Notes:
Need a commin column (medium?) in each table stating whether this is a game, song, or movie
'''
