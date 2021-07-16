import os 
import sqlite3
import pandas
import random
from flask import Flask
import datetime
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
        self.driver = webdriver.Firefox(options=opts)
        self.action = ActionChains(self.driver)

    def visit(self, url):
        self.driver.get(url)
        return self.driver.content
    
    def goodmorning_gif(self):
        self.driver.get("https://giphy.com/explore/good-morning")
        count = random.randint(1,1000)
        for i in range(count):
            self.driver.find_element_by_xpath("/html").send_keys(Keys.ARROW_DOWN)
        time.sleep(3)
        lst = [item.get("src") for item in bs4.BeautifulSoup(self.driver.page_source, "html.parser").find_all("img") if ".gif" in item.get("src")]
        gif = random.choice(lst)
        return gif
    
    def quit(self):
        self.driver.quit()

class User:
    def __init__(self, username, guild, hashed_password, email):
        self.username = username
        self.user_id
        self.guild = guild
        self.password = hashed_password
        self.email = email




def new_happy_bot_guild_users(guild, GUILD_NAME):
    db = DataBase()
    db.create_new_db("PTCB")
    db.build_table("users_PTCB", ["member_id","username", "guild", "hashed_password","email"])
    db.send_table("users_PTCB", pandas.DataFrame({
        "member_id":[member.id for member in guild.members ],
        "username":[member for member in guild.members ],
        "guild":[GUILD_NAME for member in guild.members ],
        "hashed_password":["NaN" for member in guild.members],
        "email": ["NaN" for member in guild.members]
        }))
    df = db.read_table("users_PTCB")
    print(db.tables())
    db.conn.close()

def user_of_the_week_new_table(): 
    db = DataBase("PTCB")
    db.build_table("users_of_the_week_PTCB", ["date","username", "member_id"])
    df = db.read_table("users_PTCB")
    user = random.choice(df.username.tolist())
    user_id = df.loc[df.username == user, "member_id"].item()
    df =  pandas.DataFrame({
        "date":[datetime.datetime.now()],
        "username":[user],
        "member_id":[user_id]
    })
    db.send_table("users_of_the_week_PTCB", df)
    print(db.tables())
    print(df)
    db.conn.close()


