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

# Initialize a counter for total deleted records
total_deleted = 0

# Loop over all tables in the database
print(f"With all six stones I can simply snap my fingers and it'll all cease to exist.")
print(f"-Thanos")
print(f"SNAP!!!")
for table in tables:
    # Count the number of records in the table
    mycursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = mycursor.fetchone()[0]

    # If the count exceeds 10, delete half of the records
    if count > 10:
        delete_count = count // 2
        mycursor.execute(f"DELETE FROM {table} LIMIT {delete_count}")
        mydb.commit()
        total_deleted += delete_count
        print(f"Deleted {delete_count} records from table {table}")

# Output total deleted records
print(f"Total deleted records: {total_deleted}")
print("I will shred this universe down to its last atom and then, with the stones you've collected for me, create a new one teeming with life that knows not what it has lost but only what is has been given. A grateful universe.")
print("-Thanos")

# Close the database connection
mydb.close()