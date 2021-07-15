import os 
import sqlite3
import pandas
from flask import Flask


class DataBase:
    def __init__(self, db_name=False):
        self.db_name = db_name
        if db_name != False:
            self.conn = sqlite3.connect(f"{db_name}.db")    
        else:
            self.conn = None
    
    def __repr__(self):
        return "create_new_db -> db_name\nconnect_to_db -> db_name\ntables -> self\nbuild_table -> table_name, columns\nread_table -> table_name\nsend_table -> table_name, dataframe\nclose_connection -> self"

    def create_new_db(self, new_db_name):
        os.chdir("../data")
        new_db_name = new_db_name.replace(".db","")
        conn = sqlite3.connect(f'{new_db_name}.db')
    
    def connect_to_db(self, connect_db_name):
        db_list = [ db for db in os.chdir("../data") if ".db" in db]
        if connect_db_name in db_list:
            conn = sqlite3.connect(f'{connect_db_name}.db')
            self.db_name = connect_db_name
            self.conn = conn
        else:
            return "db_name does not exit"
    
    def tables(self):
        cur = self.conn.cursor()
        cur.execute(".tables")
        return self.conn.fetchall()
    
    def build_table(self, table_name, columns):
        pandas.DataFrame({
            column:[] for column in columns
        }).to_sql(table_name, if_exists= "fail", con = self.conn, index=False)
    
    def read_table(self, table_name):
        return pandas.read_sql(f"select * from {table_name}", con=self.conn)
    
    def send_table(self, table_name, dataframe, overwrite=False):
        if overwrite == False:
            dataframe.to_sql(table_name, if_exists="append", index = False, con = self.conn)
        elif overwrite == True:
            dataframe.to_sql(table_name, if_exists="replace", index = False, con = self.conn)

    def close_connection(self):
        self.conn.close()
