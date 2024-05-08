import sqlite3
from sqlite3 import Error

import sys

from flask import Flask
from flask import request
from flask import current_app
from flask import abort
app = Flask(__name__)

@app.route("/")
def displayWelcomeMessage():
    return f"Welcome. Welcome to Cheese."

@app.route("/search")
def searchLoad():
    return current_app.send_static_file('searchPage.html')

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
        results = []
        
        if buttonChoice.startswith('a'):
            sql = f"""
            SELECT last, first
            FROM {buttonChoice}
            WHERE last LIKE ? COLLATE NOCASE
            ORDER BY last, first
            """
            cursor = conn.cursor()
            cursor.execute(sql,("%"+searchInput+"%",))
            rows = cursor.fetchall() 
            for row in rows:
                # TODO consider if this is how we want this
                result = {"Name": row[0], "firstName": row[1], "Id": row[2]}
                results.append(result)
                print(result, file=sys.stderr)
        
        else:
            # TODO Update different tables to have general "id" PK
            sql = f"""
            SELECT Name, CheeseID
            FROM {buttonChoice}
            WHERE Name LIKE ? COLLATE NOCASE
            ORDER BY Name
            """
            cursor = conn.cursor()
            cursor.execute(sql,("%"+searchInput+"%",))
            rows = cursor.fetchall()
            for row in rows:
                result = {"Name": row[0], "Id": row[1]}
                results.append(result)
                print(result,file=sys.stderr)

    except Error as e:
        print(f"Error opening the database {e}")
    finally:
        if conn:
            conn.close()
    return {"results": results}



@app.route("/search/<entityType>/<entityId>")
# def loadPage()
#     return current_app.send_static_file('individualPage.html')

def getEntity(entityType, entityId):
    conn = None
    try:
        print("Got into individual route", file=sys.stderr)
        entity = []
        conn = sqlite3.connect("./Queso Database.db")
        conn.row_factory = sqlite3.Row
        if entityType == "cheese":
            query = """
            SELECT Name
            FROM Cheese
            WHERE CheeseID = ?;
            """
            
            cursor = conn.cursor()
            cursor.execute(query, entityId)
            row = cursor.fetchone()
            # TODO ADD OTHER QUALITIES
            entity = {"Name": row[0]}
            print(entity, file=sys.stderr)
                
        #TODO ADD OTHER IFS
        

    except Error as e:
        print(f"Error opening the database {e}")
    finally:
        if conn:
            conn.close()
    if not entity:
        print("Got into abort", file=sys.stderr)
        abort(404)
    return {"entity": entity}