import os
import mysql.connector

# Connect to the MySQL server
try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="twistah"
    )
    print("Database connection successful")
except mysql.connector.Error as error:
    print(f"Error connecting to database: {error}")
    exit()

# Initialize counters
total_files = 0
successful_imports = 0
failed_imports = 0

# Loop through all SQL files in the directory
for filename in os.listdir('sql_files'):
    if filename.endswith('.sql'):
        # Increment the total files counter
        total_files += 1
        
        # Read the contents of the SQL file into a string variable
        with open(os.path.join('sql_files', filename), 'r', encoding='utf-8') as f:
            sql = f.read()

        # Execute the SQL code in the string variable
        try:
            cursor = mydb.cursor()
            cursor.execute(sql, multi=True)
            cursor.close()
            print(f"Table(s) imported from file '{filename}'")
            successful_imports += 1
        except mysql.connector.Error as error:
            print(f"Error executing SQL in file '{filename}': {error}")
            failed_imports += 1

# Print the final results
print(f"Total files: {total_files}")
print(f"Successful imports: {successful_imports}")
print(f"Failed imports: {failed_imports}")

# Test query to count the actual tables inside the database
try:
    cursor = mydb.cursor()
    cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'twistah'")
    result = cursor.fetchone()[0]
    print(f"Actual tables inside the database: {result}")
    cursor.close()
except mysql.connector.Error as error:
    print(f"Error executing query: {error}")

# Commit the changes to the database
try:
    mydb.commit()
except mysql.connector.Error as error:
    print(f"Error committing changes to database: {error}")

# Close the database connection
mydb.close()