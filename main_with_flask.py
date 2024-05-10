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
    return current_app.send_static_file('homePage.html')

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
            SELECT last, first, ID
            FROM {buttonChoice}
            WHERE last LIKE ? COLLATE NOCASE
            ORDER BY last, first
            """
            cursor = conn.cursor()
            cursor.execute(sql,("%"+searchInput+"%",))
            rows = cursor.fetchall() 
            for row in rows:
                result = {"Name": row[1] + " " + row[0], "Id": row[2]}
                results.append(result)
                print(result, file=sys.stderr)
        
        else:
            sql = f"""
            SELECT Name, ID
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



@app.route("/search/<entityType>/<int:entityId>")
def loadPage(entityType, entityId):
    return current_app.send_static_file('individualPage.html')

@app.route("/search/<entityType>/<int:entityId>", methods = ["POST"])
def getEntity(entityType, entityId):
    conn = None
    try:
        print("Got into individual route", file=sys.stderr)
        conn = sqlite3.connect("./Queso Database.db")
        conn.row_factory = sqlite3.Row
        entityType.capitalize()
        entity = []
        
        if entityType == "cheese":
            sql = f"""
            SELECT Name, Sharpness, Age, Lactose, Description, CheeseFamily
            FROM Cheese
            WHERE ID = ?
            """
            cursor = conn.cursor()
            cursor.execute(sql, (entityId,))
            row = cursor.fetchone() 
            entity = {"Name": row[0], "Sharpness": row[1], "Age": row[2],
            "Lactose": row[3], "Description": row[4], "CheeseFamily": row[5], "Vendors": []}

            sql = f"""
            SELECT Vendor.Name, Vendor.ID
            FROM Cheese INNER JOIN CheeseHasSuppliers ON Cheese.ID = CheeseHasSuppliers.CheeseID 
            INNER JOIN SuppliersHaveDistributors ON CheeseHasSuppliers.SupplierID = SuppliersHaveDistributors.SupplierID 
            INNER JOIN DistributorsSupplyVendors ON SuppliersHaveDistributors.DistributorID = DistributorsSupplyVendors.DistributorID
            INNER JOIN Vendor ON DistributorsSupplyVendors.VendorID = Vendor.ID
            WHERE Cheese.ID = ?
            """
            cursor = conn.cursor()
            cursor.execute(sql, (entityId,))
            rows = cursor.fetchall() 
            for row in rows:
                vendor = {"Name": row[0], "Id": row[1]}
                entity['Vendors'].append(vendor)
                print(vendor['Name'] + " ", vendor['Id'], file=sys.stderr)

        elif entityType == "vendor":
            sql = f"""
            SELECT Name, AddressLine, City, State, Zip, Country, PhoneNum, OpenYear, Website
            FROM Vendor
            WHERE ID = ?
            """
            cursor = conn.cursor()
            cursor.execute(sql, (entityId,))
            row = cursor.fetchone() 
            entity = {"Name": row[0], "AddressLine": row[1], "City": row[2],
            "State": row[3], "Zip": row[4], "Country": row[5], "PhoneNum": row[6],
            "OpenYear": row[7], "Website": row[8], "Cheeses": []}

            sql = f"""
            SELECT Cheese.Name, Cheese.ID
            FROM Cheese INNER JOIN CheeseHasSuppliers ON Cheese.ID = CheeseHasSuppliers.CheeseID 
            INNER JOIN SuppliersHaveDistributors ON CheeseHasSuppliers.SupplierID = SuppliersHaveDistributors.SupplierID 
            INNER JOIN DistributorsSupplyVendors ON SuppliersHaveDistributors.DistributorID = DistributorsSupplyVendors.DistributorID
            INNER JOIN Vendor ON DistributorsSupplyVendors.VendorID = Vendor.ID
            WHERE Vendor.ID = ?
            """
            cursor = conn.cursor()
            cursor.execute(sql, (entityId,))
            rows = cursor.fetchall() 
            for row in rows:
                cheese = {"Name": row[0], "Id": row[1]}
                entity['Cheeses'].append(cheese)
                print(cheese['Name'] + " ", cheese['Id'], file=sys.stderr)

        elif entityType == "distributor":
            sql = f"""
            SELECT Name, AddressLine, City, State, PhoneNum, Website, Email
            FROM Distributor
            WHERE ID = ?
            """
            cursor = conn.cursor()
            cursor.execute(sql, (entityId,))
            row = cursor.fetchone() 
            entity = {"Name": row[0], "AddressLine": row[1], "City": row[2],
            "State": row[3], "PhoneNum": row[4], "Website": row[5], "Email": row[6]}

        elif entityType == "supplier":
            sql = f"""
            SELECT Name, AddressLine, City, State, Zip, PhoneNum, Website
            FROM Supplier
            WHERE ID = ?
            """
            cursor = conn.cursor()
            cursor.execute(sql, (entityId,))
            row = cursor.fetchone() 
            entity = {"Name": row[0], "AddressLine": row[1], "City": row[2],
            "State": row[3], "Zip": row[4], "PhoneNum": row[5], "Website": row[6]}

        elif entityType == "affineur":
            sql = f"""
            SELECT First, Last, AddressLine, City, State, Zip, Country, PhoneNum, Website, Email
            FROM Affineur
            WHERE ID = ?
            """
            cursor = conn.cursor()
            cursor.execute(sql, (entityId,))
            row = cursor.fetchone() 
            entity = {"Name": row[0] + " " + row[1], "AddressLine": row[2], 
            "City": row[2], "State": row[3], "Zip": row[4], "Country": row[5], 
            "PhoneNum": row[6], "Website": row[7], "Email": row[8]}
        
        elif entityType == "cheesemaker":
            sql = f"""
            SELECT Name, AddressLine, City, State, Zip, Country, PhoneNum, Website, Email
            FROM CheeseMaker
            WHERE ID = ?
            """
            cursor = conn.cursor()
            cursor.execute(sql, (entityId,))
            row = cursor.fetchone() 
            entity = {"Name": row[0], "AddressLine": row[1], "City": row[2],
            "State": row[3], "Zip": row[4], "Country": row[5], "PhoneNum": row[6],
            "Website": row[7], "Email": row[8]}

    except Error as e:
        print(f"Error opening the database {e}")
    finally:
        if conn:
            conn.close()
    if not entity:
        print("Got into abort", file=sys.stderr)
        abort(404)
    print(entity, file=sys.stderr)
    return {"entity": entity}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)