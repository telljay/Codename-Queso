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
        




def main():
    conn = None
    try:
        conn = sqlite3.connect("../Queso Database.db")
        conn.row_factory = sqlite3.Row
        checkBox = input ("""Would you like to search for:
                          1. Cheese
                          2. Vendor
                          3. Supplier
                          4. Distributor
                          5. Cheese Maker
                          6. Affineur
                          """)
        userInput = input(f"Please enter the name of what you would search: \n")
        checkBox= int(checkBox)-1
        cheeseSearch(conn,checkBox,userInput)

    except Error as e:
        print(f"Error opening the database {e}")
    finally:
        if conn:
            conn.close()

main()