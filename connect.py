import sqlite3 
from sqlite3 import Error

def connect_db(db_path):
   connection = None
   
   try:
       connection = sqlite3.connect(db_path)
   except Error as e:
       print(f"An Error has occured: {e}")
   return connection


