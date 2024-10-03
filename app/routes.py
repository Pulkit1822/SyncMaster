# This file defines the routes for the Flask web application.

# The root route displays all the data in the MySQL database.
@app.route('/', methods=['GET'])
def index():
    # Execute a SQL query to select all the data from the MySQL database.
    cursor = db.cursor()
    cursor.execute("SELECT * FROM data")

    # Fetch all the rows from the query.
    rows = cursor.fetchall()

    # Render the index.html template with the fetched data.
    return render_template('index.html', rows=rows)

# The add route is used to add new data to the MySQL database.
@app.route('/add', methods=['POST'])
def add_data():
    # Get the name and value from the form data.
    name = request.form['name']
    value = request.form['value']

    # Execute a SQL query to insert the new data into the MySQL database.
    cursor = db.cursor()
    cursor.execute("INSERT INTO data (name, value) VALUES (%s, %s)", (name, value))

    # Commit the changes to the database.
    db.commit()

    # Update the Google Sheets document with the new data.
    update_google_sheet(SHEET_ID)

    # Redirect the user to the root route.
    return redirect(url_for('index'))

# The update_entry route is used to update existing data in the MySQL database.
@app.route('/update_entry', methods=['POST'])
def update_entry():
    # Get the old name and value from the form data.
    old_name = request.form['old_name']
    old_value = request.form['old_value']

    # Get the new name and value from the form data.
    new_name = request.form['new_name']
    new_value = request.form['new_value']

    # Execute a SQL query to update the existing data in the MySQL database.
    cursor = db.cursor()
    cursor.execute("UPDATE data SET name = %s, value = %s WHERE name = %s AND value = %s", (new_name, new_value, old_name, old_value))

    # Commit the changes to the database.
    db.commit()

    # Update the Google Sheets document with the updated data.
    update_google_sheet(SHEET_ID)

    # Redirect the user to the root route.
    return redirect(url_for('index'))

# The delete_entry route is used to delete existing data from the MySQL database.
@app.route('/delete_entry', methods=['POST'])
def delete_entry():
    # Get the name and value from the form data.
    name = request.form['name']
    value = request.form['value']

    # Execute a SQL query to delete the existing data from the MySQL database.
    cursor = db.cursor()
    cursor.execute("DELETE FROM data WHERE name = %s AND value = %s", (name, value))

    # Commit the changes to the database.
    db.commit()

    # Update the Google Sheets document with the deleted data.
    update_google_sheet(SHEET_ID)

    # Redirect the user to the root route.
    return redirect(url_for('index'))

# The sync route is used to sync the data from the Google Sheets document to the MySQL database.
@app.route('/sync', methods=['POST'])
def sync_data():
    # Sync the data from the Google Sheets document to the MySQL database.
    sync_with_google_sheet(SHEET_ID)

    # Redirect the user to the root route.
    return redirect(url_for('index'))

# The webhook route is used to receive updates from the Google Sheets document.
@app.route('/webhook', methods=['POST'])
def webhook():
    # Get the webhook payload from the request.
    data = request.get_json()

    # Check if the payload is valid.
    if data:
        # Extract the data from the payload.
        sheet_id = data.get('spreadsheetId')
        range = data.get('range')
        values = data.get('values')

        # Update the MySQL database with the extracted data.
        cursor = db.cursor()
        for row in values:
            name, value = row[0], row[1]
            cursor.execute("SELECT COUNT(*) FROM data WHERE name = %s AND value = %s", (name, value))
            count = cursor.fetchone()[0]
            if count == 0:
                cursor.execute("INSERT INTO data (name, value) VALUES (%s, %s)", (name, value))
        db.commit()

        # Return a success response.
        return jsonify({'status': 'success'}), 200
    else:
        # Return an error response.
        return jsonify({'status': 'error'}), 400
