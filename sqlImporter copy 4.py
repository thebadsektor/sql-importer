import os
import mysql.connector

# Connect to the MySQL server
try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="majayjay_dbs",
        port=3306
    )
    print("Database connection successful")
except mysql.connector.Error as error:
    print(f"Error connecting to database: {error}")
    exit()

# Get the path of the SQL files directory
sql_dir = os.path.abspath("orig")

# Import all SQL files in the directory
for filename in os.listdir(sql_dir):
    if filename.endswith(".sql"):
        # Read the contents of the SQL file into a string variable
        with open(os.path.join(sql_dir, filename), "r", encoding="utf-8") as f:
            sql = f.read()

         # Split the SQL code into individual statements
    statements = sql.split(";")

    # Execute each statement separately
    for statement in statements:
        # Skip empty statements
        if statement.strip() == "":
            continue

        # Modify the SQL statement to use AUTO_INCREMENT for zero values
        statement = statement.replace("PRIMARY KEY", "PRIMARY KEY AUTO_INCREMENT")

        # Check if table exists
        try:
            cursor = mydb.cursor()
            table_name = statement.split()[2]  # get table name from statement
            cursor.execute(f"SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '{table_name}'")
            result = cursor.fetchone()[0]
            cursor.close()

            # If table does not exist, execute statement
            if result == 0:
                cursor = mydb.cursor()
                cursor.execute(statement)
                cursor.close()
                print(f"Table created from file '{filename}'")
            # If table exists, move on to the next file
            else:
                print(f"Table '{table_name}' already exists. Skipping file '{filename}'")
                break

        except mysql.connector.Error as error:
            print(f"Error executing SQL statement in file '{filename}': {error}")

    print(f"Table(s) imported from file '{filename}'")

# Test query to count the actual tables inside the database
try:
    cursor = mydb.cursor()
    cursor.execute("SELECT COUNT(*) FROM information_schema.tables")
    result = cursor.fetchone()[0]
    print(f"Actual tables inside the database: {result}")
    cursor.close()
except mysql.connector.Error as error:
    print(f"Error executing query: {error}")

# Close the database connection
mydb.close()