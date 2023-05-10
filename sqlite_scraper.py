import os
import sqlite3
import string
import sys
sys.path.append('./src')
from src.importer import input_file
from src.image_handler import handle_photo
from src.decoder import decode
from src.logger import scraper_log

#Import extracted SQLite db
filename = input_file()
while filename == "":
    print("No file entered.\nPress ctrl+c to exit.")
    filename = input_file()

tablename = input("Enter name of table to parse (defaults to 'object_data if nothing is entered): ")

conn = sqlite3.connect(filename)
cur = conn.cursor()

#Navigate to appropriate table and row
try:
    if tablename == "":
        res = cur.execute("SELECT name FROM sqlite_master WHERE name='object_data'")
        res.fetchall()

    else:
        res = cur.execute("SELECT name FROM sqlite_master WHERE name=tablename")

    #Set character validity for decoding
    valid_chars = string.printable

    #Decode and remove extraneous hex data, leaving only ascii characters
    decode(cur)

except sqlite3.Error as error:
    print("Failed to read data from sqlite table: Error:", error)
    error_text = "Failed to read data from sqlite table: Error:".format(str(error)) 
    log_error = 1
    scraper_log(error_text, log_error)

finally:
    if conn:
        conn.close()
        print("\nSQLite Connection Closed. \nLog saved in 'run.log'\n")



    
#Future Feature - handles photos using 'image_handler.py'
#images = handle_photo(cur)


