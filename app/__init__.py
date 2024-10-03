# Create a Flask application
app = Flask(__name__)

# Load configuration from a separate file called config.py
# This file contains settings such as database connection details
app.config.from_object(Config)

# Connect to the MySQL database using the settings from the configuration file
db = mysql.connector.connect(
    # The hostname or IP address of the MySQL server
    host=app.config['MYSQL_HOST'],

    # The username to use when connecting to the MySQL server
    user=app.config['MYSQL_USER'],

    # The password to use when connecting to the MySQL server
    password=app.config['MYSQL_PASSWORD'],

    # The name of the database to connect to
    database=app.config['MYSQL_DB']
)

# Load the routes for the application
# This file contains the code for the different URLs that the application responds to
from app import routes
