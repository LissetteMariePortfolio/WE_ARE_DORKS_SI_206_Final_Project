import requests
from bs4 import BeautifulSoup
import sqlite3
import plotly.graph_objects as go
import pandas as pd

URLS = ["https://www.imdb.com/search/title/?year=2021&title_type=feature&","https://www.imdb.com/search/title/?title_type=feature&year=2021-01-01,2021-12-31&start=51&ref_=adv_nxt","https://www.imdb.com/search/title/?title_type=feature&year=2021-01-01,2021-12-31&start=51&ref_=adv_nxt"]
MAX_COUNT=100
LIMIT = 25

def set_conn():
    conn = sqlite3.connect('imdb.db') 
    cursor = conn.cursor()
    return conn, cursor
def create_table():
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

def access_api():
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
    

def make_plotly_graphic():
    genre=calc_top_from_category()
    fig = go.Figure(go.Bar(
                y=list(genre.values()),
                x=list(genre.keys()),
                orientation='v'))
    fig.update_layout(
    title="Comparison of Number of Upvotes Compared To Number Of Comments",
    xaxis_title="Number of views",
    yaxis_title="Movie Genre",
    font=dict(
            family="Courier New, monospace",
            size=18,
            color="#7f7f7f"
    )
)

    fig.show()

def write_to_file():
    data=calc_top_from_category()
    with open("file.txt","w") as file:
        for movie in data.items():
            file.write(f"{movie[0]} {movie[1]}\n")


def main():
    create_table()
    access_api()
    make_plotly_graphic()
    write_to_file()
if __name__ == "__main__":
    print(f"Database count is: {get_db_count()}") #This prints the number of records in the database
    main()
