import os

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_session import Session
import sqlite3
import base64

app = Flask(__name__)

app.config["session_permanent"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def get_db_connection():
    db = sqlite3.connect('subsidies.db')
    db.row_factory = sqlite3.Row
    return db

@app.template_filter('b64encode')
def b64encode_filter(data):
    if data:
        return base64.b64encode(data).decode('utf-8')
    return ''

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/subsidies', methods=['GET'])
def subsidies():
    db = get_db_connection()
    subsidies = db.execute('SELECT * FROM subsidies').fetchall()
    db.close()
    return render_template('subsidies.html', subsidies=subsidies)

@app.errorhandler(404)
def pagenotfound(error):
    return render_template('404.html')

if __name__ == "__main__":
    app.run(debug=True)