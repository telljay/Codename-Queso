import sqlite3
from sqlite3 import Error

import sys

from flask import Flask
from flask import request
from flask import current_app
app = Flask(__name__)

@app.route("/")
def displayWelcomeMessage():
    return f"Welcome. Welcome to Cheese."

@app.route("/search")
def searchLoad():
    return current_app.send_static_file('index.html')

@app.route("/search", methods = ["POST"])   
def simpleSearch():
    conn = None
    try:
        jsonPostData = request.get_json()
        searchInput = jsonPostData["userInput"]
        buttonChoice = jsonPostData["userButton"]
        
        print(buttonChoice, file=sys.stderr)
        print(searchInput, file=sys.stderr)

        conn = sqlite3.connect("../Queso Database.db")
        conn.row_factory = sqlite3.Row
        basicSearch_query = """
        SELECT Name
        FROM Cheese
        WHERE Name LIKE ? COLLATE NOCASE;
        """
        
        results = []
        cursor = conn.cursor()
        cursor.execute(basicSearch_query,("%"+searchInput+"%",))
        rows = cursor.fetchall()
        for row in rows :
            row_dict = {"Name": row[0]}
            results.append(row_dict)
        print(results, file=sys.stderr)

    except Error as e:
        print(f"Error opening the database {e}")
    finally:
        if conn:
            conn.close()
    return {"results": results}