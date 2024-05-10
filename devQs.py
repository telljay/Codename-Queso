import sqlite3
from sqlite3 import Error
def cheeseSearch(conn, boxResults,userInput):
    keyValuePairs = ["Cheese","Vendor","Supplier","Distributor","CheeseMaker","Affineur"]
    if(boxResults <= 4):
        sql = f"""
        SELECT Name
        FROM {keyValuePairs[boxResults]}
        WHERE Name LIKE ? COLLATE NOCASE
        ORDER BY Name
        """
        cursor = conn.cursor()
        cursor.execute(sql,("%"+userInput+"%",))
        rows = cursor.fetchall()
        for row in rows:
            results = row[0]
            
            print(results)
    else:
        sql = f"""
        SELECT last,first
        FROM {keyValuePairs[boxResults]}
        WHERE last LIKE ? COLLATE NOCASE
        ORDER BY last,first
        """
        cursor = conn.cursor()
        cursor.execute(sql,("%"+userInput+"%",))
        rows = cursor.fetchall() 
        for row in rows:
            results = f"{row[0]}, {row[1]}"  
            print(results)
        

def getEntity(entityType, entityId):
    conn = None
    try:
        print("Got into individual route")
        entity = []
        conn = sqlite3.connect("./Queso Database.db")
        conn.row_factory = sqlite3.Row
        if entityType == "cheese":
            query = """
            SELECT *
            FROM Cheese
            WHERE ID = ?;
            """
            
            cursor = conn.cursor()
            cursor.execute(query, entityId)
            rows = cursor.fetchone()
            # TODO ADD OTHER QUALITIES
            for row in rows:
                entity += {row}
            print(entity)
                
        #TODO ADD OTHER IFS
        

    except Error as e:
        print(f"Error opening the database {e}")
    finally:
        if conn:
            conn.close()
    if not entity:
        print("Got into abort")
        ##abort(404)
    return {"entity": entity}



def main():
    conn = None
    try:
        conn = sqlite3.connect("../Queso Database.db")
        conn.row_factory = sqlite3.Row
        checkBox = "cheese"
        userInput = input(f"Please enter the Id of what you would search: \n")
        ##checkBox= int(checkBox)-1
        getEntity(checkBox,userInput)

    except Error as e:
        print(f"Error opening the database {e}")
    finally:
        if conn:
            conn.close()

main()