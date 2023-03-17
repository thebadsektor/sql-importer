import mysql.connector

# Set up a connection to the MySQL database
# cnx = mysql.connector.connect(user='your_username', password='your_password', host='your_host', database='your_database')

# Connect to the MySQL server
try:
    cnx = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="majayjay_dbs"
    )
    print("Database connection successful")
except mysql.connector.Error as error:
    print(f"Error connecting to database: {error}")
    exit()

# Create a cursor object to execute queries
cursor = cnx.cursor()

# Define the name of the table you want to check
table_name = 'permission_tbl'

# Define the query to check if the table exists
check_table_query = "SHOW TABLES LIKE %s"

# Execute the query with the table name as a parameter
cursor.execute(check_table_query, (table_name,))

# Check if the query returned any results
table_exists = cursor.fetchone() is not None

# Print the result
if table_exists:
    print(f"The table '{table_name}' exists.")
else:
    print(f"The table '{table_name}' does not exist.")

# Clean up the cursor and connection
cursor.close()
cnx.close()