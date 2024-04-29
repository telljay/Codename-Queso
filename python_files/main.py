import sqlite3
from sqlite3 import Error
def basicSearch(conn):
    print(f"Please enter a search: \n")
    word = input()
    basicSearch_query = """
    SELECT Name
    FROM Cheese
    WHERE Name LIKE ? COLLATE NOCASE;
    """
    cursor = conn.cursor()
    cursor.execute(basicSearch_query,("%"+word+"%",))
    rows = cursor.fetchall()
    for row in rows:
        print(f"{row[0]}")

    
def main():
    conn = None
    try:
        conn = sqlite3.connect("C:/Users/toell/Desktop/Codename Queso/Queso Database.db")
        conn.row_factory = sqlite3.Row
        
        basicSearch(conn)

    except Error as e:
        print(f"Error opening the database {e}")
    finally:
        if conn:
            conn.close()

main()