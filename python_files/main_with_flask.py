import sqlite3
from sqlite3 import Error

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
        # Might alternatively use a request.form["searchInput"]

        conn = sqlite3.connect("../Queso Database.db")
        conn.row_factory = sqlite3.Row
        
        print(f"Please enter a search: \n")
        word = searchInput
        basicSearch_query = """
        SELECT Name
        FROM Cheese
        WHERE Name LIKE ? COLLATE NOCASE;
        """
        
        results = []
        cursor = conn.cursor()
        cursor.execute(basicSearch_query,("%"+word+"%",))
        rows = cursor.fetchall()
        for row in rows :
            row_dict = {"Name": row[0]}
            results.append(row_dict)
        return results

    except Error as e:
        print(f"Error opening the database {e}")
    finally:
        if conn:
            conn.close()