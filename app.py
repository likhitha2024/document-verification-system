from flask import Flask, render_template, request, redirect, session
import os
import hashlib
from datetime import datetime

app = Flask(__name__)
app.secret_key = "mysecretkey"

# Upload folder
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Function to log user actions
def log_action(user, action, filename):
    with open("logs.txt", "a") as log:
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"{time} | {user} | {action} | {filename}\n")


# Home Page
@app.route('/')
def home():
    return render_template("index.html")


# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        if username == "admin" and password == "1234":
            session['user'] = username
            return redirect('/upload')

        else:
            return "Invalid Username or Password"

    return render_template("login.html")


# Upload Page
@app.route('/upload', methods=['GET', 'POST'])
def upload():

    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':

        file = request.files['document']

        if file:

            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # Log upload activity
            log_action(session['user'], "upload", file.filename)

            # Generate hash
            with open(filepath, "rb") as f:
                file_data = f.read()
                file_hash = hashlib.sha256(file_data).hexdigest()

            return f"File uploaded successfully. Hash: {file_hash}"

    return render_template("upload.html")


# Verify Page
@app.route('/verify', methods=['GET', 'POST'])
def verify():

    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':

        file = request.files['document']

        if file:

            # Log verification activity
            log_action(session['user'], "verify", file.filename)

            # Hash of uploaded file
            file_data = file.read()
            uploaded_hash = hashlib.sha256(file_data).hexdigest()

            original_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

            if os.path.exists(original_path):

                with open(original_path, "rb") as f:
                    original_data = f.read()
                    original_hash = hashlib.sha256(original_data).hexdigest()

                if uploaded_hash == original_hash:
                    return "Document Verified ✔ (Not Modified)"
                else:
                    return "Document Modified ⚠"

            else:
                return "Original file not found in server"

    return render_template("verify.html")

@app.route('/logs')
def view_logs():

    if 'user' not in session:
        return redirect('/login')

    with open("logs.txt", "r") as log:
        logs = log.readlines()

    return render_template("logs.html", logs=logs)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)

