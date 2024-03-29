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

# Define error log file
error_log = open("error.log", "w")

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

        try:
            cursor = mydb.cursor()

            # Check if statement is a table creation statement
            if statement.strip().startswith("CREATE TABLE"):
                # Extract the table name from the statement
                table_name = statement.split()[2]  # get table name from statement

                # Check if table already exists
                cursor.execute(f"SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '{table_name}'")
                result = cursor.fetchone()[0]

                # If table does not exist, execute statement
                if result == 0:
                    cursor.execute(statement)
                    print(f"Table '{table_name}' created from file '{filename}'")
                # If table exists, log error and move on to the next statement
                else:
                    error_log.write(f"Table '{table_name}' already exists. Skipping statement in file '{filename}'\n")
                    continue

            # Check if statement is a row insertion statement
            elif statement.strip().startswith("INSERT INTO"):
                cursor.execute(statement)
                print(f"Row inserted from file '{filename}'")
            else:
                continue

            cursor.close()

        # Log error if statement execution fails
        except mysql.connector.Error as error:
            error_log.write(f"Error executing SQL statement in file '{filename}': {error}\n")

    print(f"All statements executed in file '{filename}'")
    
# Close the error log file
error_log.close()

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