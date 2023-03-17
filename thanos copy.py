import mysql.connector

# Connect to the database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="majayjay_dbs",
  port=3306
)

# Get a cursor object to execute SQL queries
mycursor = mydb.cursor()

# Get a list of all the tables in the database
mycursor.execute("SHOW TABLES")
tables = [x[0] for x in mycursor.fetchall()]

# Loop over all tables in the database
for table in tables:
    # Count the number of records in the table
    mycursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = mycursor.fetchone()[0]

    # If the count exceeds 10, delete half of the records
    if count > 10:
        delete_count = count // 2
        mycursor.execute(f"DELETE FROM {table} LIMIT {delete_count}")
        mydb.commit()

# Close the database connection
mydb.close()