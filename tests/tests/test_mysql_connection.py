import mysql.connector  # Import the MySQL connector library to interact with MySQL database

# Define a dictionary with configuration details for connecting to the MySQL database
config = {
    'user': 'root',  # Username to authenticate with MySQL
    'password': '',  # Password for the MySQL user, replace with your MySQL password
    'host': 'localhost',  # Hostname where the MySQL server is running, usually localhost for local server
    'database': 'syncmaster_db'  # Name of the database to connect to
}

try:
    # Attempt to establish a connection to the database using the provided config
    db = mysql.connector.connect(**config)
    cursor = db.cursor()  # Create a cursor object to execute SQL queries
    cursor.execute("SELECT DATABASE();")  # Execute a SQL query to select the current database
    database_name = cursor.fetchone()  # Fetch the first row of the query result
    print(f"Connected to database: {database_name[0]}")  # Print the name of the connected database
    cursor.close()  # Close the cursor to free database resources
    db.close()  # Close the database connection
except mysql.connector.Error as err:
    print(f"Error: {err}")  # Print an error message if an exception occurs during the database connection process
