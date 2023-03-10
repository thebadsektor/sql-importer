import os
import mysql.connector

# Connect to the MySQL server
try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="majayjay_dbs"
    )
    print("Database connection successful")
except mysql.connector.Error as error:
    print(f"Error connecting to database: {error}")
    exit()

# Close the database connection
mydb.close()