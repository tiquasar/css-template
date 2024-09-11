import requests
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, make_response, send_file
import json
import pandas as pd

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Required for flash messages and session management

# External API endpoint (replace this with the actual API endpoint)
EXTERNAL_API_URL = "https://external-api.example.com/upload"  # Example URL

# Route for the login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['logged_in'] = True  # Set session to indicate user is logged in
        return redirect(url_for('dashboard'))  # Redirect to the dashboard page

    response = make_response(render_template('login.html'))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

# Route for the dashboard
@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    response = make_response(render_template('dashboard.html'))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

# API Route to process the uploaded files and forward them to an external API
@app.route('/process-files', methods=['POST'])
def process_files():
    if 'jsonFile' not in request.files:
        return jsonify({'error': 'JSON file is required.'}), 400

    json_file = request.files['jsonFile']
    xlsx_file = request.files.get('xlsxFile')

    files_to_send = {
        'json-file': (json_file.filename, json_file, json_file.mimetype),
    }

    if xlsx_file and xlsx_file.filename.endswith('.xlsx'):
        files_to_send['xlsx-file'] = (xlsx_file.filename, xlsx_file, xlsx_file.mimetype)

    try:
        external_response = requests.post(EXTERNAL_API_URL, files=files_to_send)

        if external_response.status_code == 200:
            # Save the output to a CSV for download
            output_data = external_response.json()
            with open('output.json', 'w') as f:
                json.dump(output_data, f)

            return external_response.json()  # Return the response from the external API
        else:
            return jsonify({'error': 'Error from external API.', 'details': external_response.text}), external_response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Failed to connect to external API./n/n/n/n/n/n/n/n/n/',
                        'error2': 'Failed to connect to external API./n/n/n/n/n/n/n/n/n/',
                        'error3': 'Failed to connect to external API./n/n/n/n/n/n/n/n/n/',
                        'error4': 'Failed to connect to external API./n/n/n/n/n/n/n/n/n/',
                        'error5': 'Failed to connect to external API./n/n/n/n/n/n/n/n/n/',
                        'error6': 'Failed to connect to external API./n/n/n/n/n/n/n/n/n/',
                        'error7': 'Failed to connect to external API./n/n/n/n/n/n/n/n/n/'}), 500

# Route to download the output as CSV
@app.route('/download-csv')
def download_csv():
    # Load the saved JSON output
    with open('output.json', 'r') as f:
        data = json.load(f)

    # Convert the JSON to a Pandas DataFrame
    df = pd.DataFrame(data)

    # Save the CSV output
    df.to_csv('output.csv', index=False)

    # Send the CSV file for download
    return send_file('output.csv', as_attachment=True)

# Route for logging out
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)  # Clear the session
    return redirect(url_for('login'))  # Redirect to login page

# Running the app
if __name__ == '__main__':
    app.run(debug=True)
