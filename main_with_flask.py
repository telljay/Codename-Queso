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
    return current_app.send_static_file('searchPage.html')

# @app.route("/search/<entityType>/<entityId>")
# def getEntity(entityType, entityId):
#     conn = None
#     try:
#         entity = []
#         conn = sqlite3.connect("../Queso Database.db")
#         conn.row_factory = sqlite3.Row
#         if entityType == "Cheese":
#             query = """
#             SELECT Name
#             FROM Cheese
#             WHERE Id = ?;
#             """
            
#             cursor = conn.cursor()
#             cursor.execute(query, entityId)
#             row = cursor.fetchone()
#             # TODO ADD OTHER QUALITIES
#             results = {"Name": row[0], "OTHER QUALITIES": row[1]}
#             print(results, file=sys.stderr)
                
#         #TODO ADD OTHER IFS
        

#     except Error as e:
#         print(f"Error opening the database {e}")
#     finally:
#         if conn:
#             conn.close()
#     if not results:
        # abort(404)
#     return {"results": results}

@app.route("/search", methods = ["POST"])   
def simpleSearch():
    conn = None
    try:
        jsonPostData = request.get_json()
        searchInput = jsonPostData["userInput"]
        buttonChoice = jsonPostData["userButton"]
        buttonChoice.capitalize()

        print(buttonChoice, file=sys.stderr)
        print(searchInput, file=sys.stderr)
        conn = sqlite3.connect("./Queso Database.db")
        conn.row_factory = sqlite3.Row
        ##----        
        if buttonChoice.startswith('a'):
            sql = f"""
            SELECT last,first
            FROM {buttonChoice}
            WHERE last LIKE ? COLLATE NOCASE
            ORDER BY last,first
            """
            cursor = conn.cursor()
            cursor.execute(sql,("%"+searchInput+"%",))
            rows = cursor.fetchall() 
            for row in rows:
                results = f"{row[0]}, {row[1]}"
                print(results,file=sys.stderr)
        
        else:
            sql = f"""
            SELECT Name
            FROM {buttonChoice}
            WHERE Name LIKE ? COLLATE NOCASE
            ORDER BY Name
            """
            cursor = conn.cursor()
            cursor.execute(sql,("%"+searchInput+"%",))
            rows = cursor.fetchall()
            for row in rows:
                results = row[0]
                print(results,file=sys.stderr)


        ##----
    except Error as e:
        print(f"Error opening the database {e}")
    finally:
        if conn:
            conn.close()
    return {"results": results}