import sqlite3
from sqlite3 import Error
def basicSearch(conn, userInput):
    basicSearch_query = """
    SELECT Name
    FROM Cheese
    WHERE Name LIKE ? COLLATE NOCASE;
    """
    cursor = conn.cursor()
    cursor.execute(basicSearch_query,("%"+userInput+"%",))
    rows = cursor.fetchall()
    for row in rows:
        print(f"{row[0]}")

    
def vendorSearch(conn):
    vendorSearch_query = """
    SELECT Name
    FROM Vendor
    WHERE Name = ?
    """


def main():
    conn = None
    try:
        conn = sqlite3.connect("../Queso Database.db")
        conn.row_factory = sqlite3.Row
        userInput = input(f"Please enter the name of what you would search")
        
        basicSearch(conn,userInput)

    except Error as e:
        print(f"Error opening the database {e}")
    finally:
        if conn:
            conn.close()

main()