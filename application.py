import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

# Lines 11 - 26 credit CS50
# Configure application
app = Flask(__name__)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///corona.db")

@app.route("/")
def home():
    numTotalCasesDict = {"AFG": db.execute("SELECT numTotalCases FROM 'corona' WHERE id='1'")[0]['numTotalCases']}
    print(db.execute("SELECT numTotalCases FROM 'corona' WHERE id='1'"))
    return render_template("home.html", numCasesDict = numTotalCasesDict)