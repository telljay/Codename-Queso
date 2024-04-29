#CURRENTLY BROKEN
#CURRENTLY BROKEN
#CURRENTLY BROKEN

import sqlite3
from sqlite3 import Error

from flask import Flask
from flask import request
app = Flask(__name__)

@app.route("/")
def displayWelcomeMessage():
    return f"Welcome. Welcome to Cheese."

@app.route("/search", methods = ["POST"])   
def simpleSearch():
    conn = None
    try:
        jsonPostData = request.get_json()
        searchInput = jsonPostData["userInput"]
        # conn = sqlite3.connect("C:/Users/toell/Desktop/Codename Queso/Queso Database.db")
        # conn.row_factory = sqlite3.Row
        
        print(f"Please enter a search: \n")
        word = searchInput
        # basicSearch_query = """
        # SELECT Name
        # FROM Cheese
        # WHERE Name LIKE ? COLLATE NOCASE;
        # """
        # cursor = conn.cursor()
        # cursor.execute(basicSearch_query,("%"+word+"%",))
        # rows = cursor.fetchall()
        # return rows
        return jsonPostData["userInput"]

    except Error as e:
        print(f"Error opening the database {e}")
    finally:
        if conn:
            conn.close()