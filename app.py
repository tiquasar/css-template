from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file, session, make_response
import pandas as pd
import os
import json

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Required for flash messages and session management

# Route for the login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Example: Add authentication logic here
        session['logged_in'] = True  # Set session to indicate user is logged in
        return redirect(url_for('dashboard'))  # Redirect to the dashboard page
    
    # Prevent caching of the login page
    response = make_response(render_template('login.html'))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

# Route for the dashboard
@app.route('/dashboard')
def dashboard():
    # If the user is not logged in, redirect to login page
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    # Prevent caching of the dashboard page
    response = make_response(render_template('dashboard.html'))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

# API Route to process the uploaded XLSX file
@app.route('/process-file', methods=['POST'])
def process_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    # Check if the file is an XLSX file
    if file.filename.endswith('.xlsx'):
        # Process the file (convert to dataframe, simulate some processing)
        df = pd.read_excel(file)
        output_data = df.to_dict(orient='records')

        # Save the output as JSON (temporary)
        with open('output.json', 'w') as f:
            json.dump(output_data, f)

        return jsonify({'output': output_data})

    return jsonify({'error': 'Invalid file format. Only XLSX files are accepted.'}), 400

# Route to download the output as CSV
@app.route('/download-csv')
def download_csv():
    with open('output.json', 'r') as f:
        data = json.load(f)

    df = pd.DataFrame(data)
    df.to_csv('output.csv', index=False)

    return send_file('output.csv', as_attachment=True)

# Route for logging out
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)  # Clear the session
    return redirect(url_for('login'))  # Redirect to login page

# Running the app
if __name__ == '__main__':
    app.run(debug=True)
