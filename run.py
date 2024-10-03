# This is the main entry point for the application.
# It imports the app object which is an instance of the Flask class.
# The app object is the WSGI application object that is used to
# communicate with the web server and handle requests and responses.
from app import app

# This is the main entry point for the application.
# It checks if this script is being run directly (i.e. not being imported
# as a module in another script) and if so, it runs the app with the
# debug flag set to True.
if __name__ == '__main__':
    # The debug flag is a boolean that determines whether the app runs
    # in debug mode or not. If it is set to True, the app will automatically
    # reload if any changes are made to the source code, and it will provide
    # more detailed error messages.
    app.run(debug=True)
