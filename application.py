import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import textract
from bs4 import BeautifulSoup
import requests
import pandas as pd
import pycountry as pc


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

    date='3/31/20'

    numTotalCasesDict = {}
    colorDict={}
    country3 = []

    df = pd.read_csv('virusTable.csv')
    country_column = df['Country/Region']
    cases_column = df[date]
    row_count = 0
    chinaSum = 0
    UKSum = 0

    for i in range(0, 256):
        print(country_column[i])
        if country_column[i] == 'China':
            chinaSum += cases_column[i]
        elif country_column[i] == 'United Kingdom':
            UKSum += cases_column[i]

    print(chinaSum)
    print('––––––––––––––––––')

    # FIX UP SOME COUNTRIES
    # COLOR SCHEME
    # BEGIN OTHER PHASES.


    for i in range(0, 256):
        if country_column[i] == 'China':
            numTotalCasesDict['CHN'] = chinaSum
        elif country_column[i] == 'United Kingdom':
            numTotalCasesDict['GBR'] = UKSum
        elif country_column[i] == 'US':
            numTotalCasesDict['USA'] = cases_column[i]
        elif country_column[i] == 'Venezuela':
            numTotalCasesDict['VEN'] = cases_column[i]
        elif country_column[i] == 'Iran':
            numTotalCasesDict['IRN'] = cases_column[i]
        elif country_column[i] == 'Korea, South':
            numTotalCasesDict['KOR'] = cases_column[i]
        elif country_column[i] == 'Russia':
            numTotalCasesDict['RUS'] = cases_column[i]
        else:
            try:
                country = pc.countries.get(name = country_column[i])
                numTotalCasesDict[country.alpha_3] = cases_column[i]
            except:
                continue

    print(numTotalCasesDict)

    """
    def assignColor(index):
        check = numTotalCasesDict[index]
        if len(check) == 6:
            return 'vhigh'
        elif len(check) == 5:
            return 'high'
        elif len(check) == 4:
            return 'med'
        elif len(check) == 3:
            return 'low'
        elif check is 'I don\'t know':
            return 'nothing'
        else:
            return 'vlow'

    for i in range(len(countries)):
        index = text.find(countries[i])
        if(countries[i] is 'USA' or countries[i] is 'Italy'):
            isOK = True
        else:
            isOK = False
        if index == -1:
            numTotalCasesDict[i] = 'I don\'t know'
            continue

        substr = text[index + len(countries[i]) : index + len(countries[i]) + 7]

        commaPresent = False

        for char in substr:
            if (not char.isdigit()) and (char is not ',') :
                substr = substr[0 : substr.find(char)]
            if char is ',':
                commaPresent = True

        if len(substr) == 7 and not isOK:
            if commaPresent:
                substr = substr[0 : 4]
            else:
                substr = substr[0 : 2]

        if (len(substr) == 6 or len(substr) == 5 or len(substr) == 4) and not commaPresent:
            substr = substr[0 : 2]

        if len(substr) >= 4 and (substr[len(substr) - 1] is ','):
            substr = substr[0 : 1]

        if len(substr) == 0:
            numTotalCasesDict[i] = 'I don\'t know'
            continue

        numTotalCasesDict[i] = substr

        colorDict[i] = assignColor(i)


    print(colorDict)
    print(numTotalCasesDict)

    print('––––––––––––––––––––––––––––––––––––')
    print(colorDict[0])



    website_url = requests.get('https://en.wikipedia.org/wiki/2019%E2%80%9320_coronavirus_pandemic_by_country_and_territory').text
    soup = BeautifulSoup(website_url)
    theTable = soup.find('table', {'class': 'wikitable plainrowheaders sortable'})
    print(theTable)
    links = theTable.findAll('a')
    print(links)
    countries = []
    for link in links:
        countries.append(link.get('title'))


    countries = [c for c in countries if c != None]

    countries = countries[3 : len(countries) - 1]

    print(countries)
    """

    return render_template("home.html", theDict = numTotalCasesDict)

    # return render_template("home.html", numCasesDict = numTotalCasesDict, colorDict = colorDict, countries3 = countries3)