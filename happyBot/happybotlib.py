import os 
import sqlite3
import pandas
import random
import datetime
import tqdm
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import bs4
import time


class DataBase:
    def __init__(self, db_name=False):
        self.db_name = db_name
        if db_name != False and db_name in [i.replace(".db","") for i in os.listdir("../data")]:
            self.conn = sqlite3.connect(f"../data/{db_name}.db")    
        else:
            self.conn = None
    
    def __repr__(self):
        return "create_new_db -> db_name\nconnect_to_db -> db_name\ntables -> self\nbuild_table -> table_name, columns\nread_table -> table_name\nsend_table -> table_name, dataframe\nclose_connection -> self"

    def create_new_db(self, new_db_name):
        if new_db_name in [i.replace(".db","") for i in os.listdir("../data")]:
            return "db already exists"
        new_db_name = new_db_name.replace(".db","")
        conn = sqlite3.connect(f'../data/{new_db_name}.db')
        self.conn = conn
    
    def connect_to_db(self, connect_db_name):
        db_list = [ db for db in os.listdir("../data") if ".db" in db]
        if connect_db_name in db_list:
            conn = sqlite3.connect(f'../data/{connect_db_name}.db')
            self.db_name = connect_db_name
            self.conn = conn
        else:
            return "db_name does not exit"
    
    def tables(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return cursor.fetchall()

    def build_table(self, table_name, columns):
        pandas.DataFrame({
            column:[] for column in columns
        }).to_sql(table_name, if_exists= "fail", con = self.conn, index=False)
    
    def read_table(self, table_name):
        return pandas.read_sql(f"select * from {table_name}", con=self.conn)
    
    def send_table(self, table_name, dataframe, overwrite=False):
        if overwrite == False:
            dataframe.astype(str).to_sql(table_name, if_exists="append", index = False, con = self.conn)
        elif overwrite == True:
            dataframe.astype(str).to_sql(table_name, if_exists="replace", index = False, con = self.conn)

    
    def update_tables():
        pass
    
    def close_connection(self):
        self.conn.close()

class WebScraper:
    def __init__(self, headless=True, opts= Options()):
        opts.headless = headless
        opts.add_argument('--disable-browser-side-navigation')
        self.driver = webdriver.Firefox(options=opts)
        self.action = ActionChains(self.driver)
        print("started ws")
    def visit(self, url):
        self.driver.get(url)
        return self.driver.content
    
    def goodmorning_gif(self):
        print("scraping...")
        self.driver.get("https://giphy.com/explore/good-morning")
        count = random.randint(1,50)
        for i in range(count):
            self.driver.find_element_by_xpath("/html").send_keys(Keys.ARROW_DOWN)
        time.sleep(3)
        lst = [item.get("src") for item in bs4.BeautifulSoup(self.driver.page_source, "html.parser").find_all("img") if ".gif" in item.get("src")]
        print("scraping complete...")
        print("downloading morning gifs...")
        for i,img in enumerate(tqdm.tqdm(lst)):
            with open(f"../data/Gifs/Goodmorning_{i}.gif","wb") as gif_file:
                gif_file.write(requests.get(img).content)

        print("Gifs saved to data/Gifs")
    
    def celebration_gif(self):
        print("scraping...")
        self.driver.get("https://giphy.com/explore/celebrate")
        count = random.randint(1,50)
        for i in range(count):
            self.driver.find_element_by_xpath("/html").send_keys(Keys.ARROW_DOWN)
        time.sleep(3)
        lst = [item.get("src") for item in bs4.BeautifulSoup(self.driver.page_source, "html.parser").find_all("img") if ".gif" in item.get("src")]
        print("scraping complete...")
        print("downloading images...")
        for i,img in enumerate(tqdm.tqdm(lst)):
            with open(f"../data/Gifs/Celebrate_{i}.gif","wb") as gif_file:
                gif_file.write(requests.get(img).content)

        print("Gifs saved to data/Gifs")
    
    def quit(self):
        self.driver.quit()

class User:
    def __init__(self, username, guild, hashed_password, email):
        self.username = username
        self.user_id
        self.guild = guild
        self.password = hashed_password
        self.email = email

class FirstSetUp:
    def __init__(self, client):
        self.client = client
    async def setup(self):
        guild_dict = {guild:0 for guild in self.client.guilds}
        for guild in guild_dict:
            for channel in guild.channels:
                if "general" in channel.name:
                    guild_dict[guild] += channel.id
                    break

        for guild in guild_dict:
            new_happy_bot_guild_users(guild)
            user_of_the_week_new_table()
            await client.get_channel(guild_dict[guild]).send(f"HappyBot Conneted to {guild.name} Guild")



#collect general chat room for all guilds
def collect_general_chat_all_guilds(client):
    guild_dict = {guild:0 for guild in client.guilds}
    for guild in guild_dict:
        for channel in guild.channels:
            if "general" in channel.name:
                guild_dict[guild] += channel.id
    return guild_dict

#Builds a sqlite3 database for the new guild along with a table for users
def new_happy_bot_guild_users(guild):
    db = DataBase()
    db.create_new_db(input("dbname:\n"))
    table = input("db_users_table:\n")
    db.build_table(table, ["member_id","username", "guild", "hashed_password","email"])
    db.send_table(table, pandas.DataFrame({
        "member_id":[member.id for member in guild.members ],
        "username":[member for member in guild.members ],
        "guild":[guild.name for member in guild.members ],
        "hashed_password":["NaN" for member in guild.members],
        "email": ["NaN" for member in guild.members]
        }))
    df = db.read_table(table)
    print(db.tables())
    db.close_connection()

#Builds a sqlite3 user of the week table given an existing database
def user_of_the_week_new_table():
    db_list = [i for i in os.listdir("../data") if ".db" in i]
    for db in db_list:
        print(i)
    response = input("db_name:\n")
    if response not in db_list:
        print("invalid: database does not exist:\n")
        return             
    db = DataBase(response)
    table = "users_of_the_week"
    db.build_table(table, ["date","username", "member_id"])
    df = db.read_table(input("users table:\n"))
    print(df)
    user = random.choice(df.username.tolist())
    user_id = df.loc[df.username == user, "member_id"].item()
    df =  pandas.DataFrame({
        "date":[datetime.datetime.now()],
        "username":[user],
        "member_id":[user_id]
    })
    db.send_table(table, df)
    print(db.tables())
    print(df)
    db.close_connection()

#randomly selects a user of the week given a db and the users table 
def pick_user_of_the_week(db_name, user_table):
    table = "users_of_the_week"
    db = DataBase(db_name)
    df_users = db.read_table(user_table)
    df_of_week = db.read_table(table)
    last_date = df_of_week.tail(1)["date"].item()
    user, user_id = random.choice(list(zip(df_users.username.tolist(),df_users.member_id.tolist())))
    db.send_table(table, pandas.DataFrame({
        "date":[datetime.datetime.now().date()],
        "username":[user],
        "member_id":[user_id]
    }))
    db.close_connection()
    return user.split("#")[0]

#pick a random goodmorning gif
def pick_random_goodmorning_gif():
    gm_gif = random.choice([gif for gif in os.listdir("../data/Gifs") if "Goodmorning" in gif])
    return f"../data/Gifs/{gm_gif}"

#pick a random celebration gif
def pick_random_celebration_gif():
    gm_gif = random.choice([gif for gif in os.listdir("../data/Gifs") if "Celebrate" in gif])
    return f"../data/Gifs/{gm_gif}"
