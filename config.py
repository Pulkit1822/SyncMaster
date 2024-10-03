# This class defines configuration variables for the app
class Config:
    # SECRET_KEY is a secret key used by Flask and extensions to keep data secure.
    # For example, it is used to securely sign session cookies.
    # If the SECRET_KEY environment variable is set, use that.
    # Otherwise, use a default secret key of 'supersecretkey'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecretkey'

    # The following configuration variables are used to connect to the MySQL database
    # The host is the location of the MySQL server
    # The user is the username used to connect to the MySQL server
    # The password is the password used to connect to the MySQL server
    # The db is the name of the database to connect to
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = '' # Replace with your MySQL password
    MYSQL_DB = 'syncmaster_db'
