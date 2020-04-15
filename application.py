import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import requests
import pandas as pd
import pycountry as pc


# Lines 11 - 26 credit CS50
# Configure application
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

db = SQL("sqlite:///corona.db")

# Configure session to use filesystem (instead of signed cookies)
@app.route("/", methods=["GET", "POST"])
def home():

    views = db.execute("SELECT * FROM corona")
    views = views[0]['views']
    views += 1
    db.execute("UPDATE corona SET views = :views", views = views)
    print(db.execute("SELECT * FROM corona"))


    if request.method == "GET":
        date='4/13/20'

        numTotalCasesDict = {}
        numDeathsDict = {}
        colorDict={}

        def getColor(country):
            numCases = numTotalCasesDict[country]
            numCases = int(numCases)
            if numCases >= 500000:
                return 'extreme'
            elif numCases >= 100000:
                return 'vhigh'
            elif numCases >= 50000:
                return 'high'
            elif numCases >= 10000:
                return 'medium'
            elif numCases >= 1000:
                return 'low'
            else:
                try:
                    int(numCases)
                    return 'vlow'
                except:
                    return 'nothing'


        tc = pd.read_csv('virusTable.csv')
        country_column = tc['Country/Region']
        print(country_column)
        province_column = tc['Province/State']
        cases_column = tc[date]
        row_count = 0
        chinaSum = 0
        UKSum = 0
        canadaSum = 0
        auSum = 0
        frSum = 0

        for i in range(0, 264):
            if country_column[i] == 'China':
                chinaSum += cases_column[i]
            elif country_column[i] == 'United Kingdom':
                UKSum += cases_column[i]
            elif country_column[i] == 'Canada':
                canadaSum += cases_column[i]
            elif country_column[i] == 'Australia':
                auSum += cases_column[i]
            elif country_column[i] == 'France' and province_column[i] != 'French Guiana':
                frSum += cases_column[i]


        # FIX UP SOME COUNTRIES
        # COLOR SCHEME
        # BEGIN OTHER PHASES.


        for i in range(0, 264):
            if country_column[i] == 'China':
                numTotalCasesDict['CHN'] = chinaSum
            elif country_column[i] == 'United Kingdom':
                numTotalCasesDict['GBR'] = UKSum
            elif country_column[i] == 'Canada':
                numTotalCasesDict['CAN'] = canadaSum
            elif country_column[i] == 'Australia':
                numTotalCasesDict['AUS'] = auSum
            elif country_column[i] == 'France':
                numTotalCasesDict['FRA'] = frSum
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
            elif country_column[i] == 'Bolivia':
                numTotalCasesDict['BOL'] = cases_column[i]
            elif country_column[i] == 'Tanzania':
                numTotalCasesDict['TZA'] = cases_column[i]
            elif country_column[i] == 'Syria':
                numTotalCasesDict['SYR'] = cases_column[i]
            elif country_column[i] == 'Burma':
                numTotalCasesDict['MMR'] = cases_column[i]
            elif country_column[i] == 'Laos':
                numTotalCasesDict['LAO'] = cases_column[i]
            elif country_column[i] == 'Vietnam':
                numTotalCasesDict['VNM'] = cases_column[i]
            elif country_column[i] == 'Moldova':
                numTotalCasesDict['MDA'] = cases_column[i]
            elif country_column[i] == 'Brunei':
                numTotalCasesDict['BRN'] = cases_column[i]
            elif country_column[i] == 'Congo (Kinshasa)':
                numTotalCasesDict['COD'] = cases_column[i]
            elif country_column[i] == 'Congo (Brazzaville)':
                numTotalCasesDict['COG'] = cases_column[i]
            elif country_column[i] == 'Yemen':
                numTotalCasesDict['YEM'] = cases_column[i]
            elif country_column[i] == 'Denmark' and province_column[i] == 'Greenland':
                numTotalCasesDict['GRL'] = cases_column[i]
            elif country_column[i] == 'France' and province_column[i] == 'French Guiana':
                numTotalCasesDict['GUF'] = cases_column[i]
            else:
                try:
                    country = pc.countries.get(name = country_column[i])
                    numTotalCasesDict[country.alpha_3] = cases_column[i]
                except:
                    continue


        dc = pd.read_csv('deathTable.csv')
        D_country_column = dc['Country/Region']
        D_province_column = dc['Province/State']
        D_cases_column = dc[date]
        row_count = 0
        chinaDeathSum = 0
        UKDeathSum = 0
        canadaDeathSum = 0
        auDeathSum = 0
        frDeathSum = 0


        for i in range(0, 264):
            if D_country_column[i] == 'China':
                chinaDeathSum += D_cases_column[i]
            elif D_country_column[i] == 'United Kingdom':
                UKDeathSum += D_cases_column[i]
            elif D_country_column[i] == 'Canada':
                canadaDeathSum += D_cases_column[i]
            elif D_country_column[i] == 'Australia':
                auDeathSum += D_cases_column[i]
            elif D_country_column[i] == 'France' and D_province_column[i] != 'French Guiana':
                frDeathSum += D_cases_column[i]



        for i in range(0,264):
            if D_country_column[i] == 'China':
                numDeathsDict['CHN'] = chinaDeathSum
            elif D_country_column[i] == 'United Kingdom':
                numDeathsDict['GBR'] = UKDeathSum
            elif D_country_column[i] == 'US':
                numDeathsDict['USA'] = D_cases_column[i]
            elif D_country_column[i] == 'Canada':
                numDeathsDict['CAN'] = canadaDeathSum
            elif D_country_column[i] == 'Australia':
                numDeathsDict['AUS'] = auDeathSum
            elif D_country_column[i] == 'Venezuela':
                numDeathsDict['VEN'] = D_cases_column[i]
            elif D_country_column[i] == 'Iran':
                numDeathsDict['IRN'] = D_cases_column[i]
            elif D_country_column[i] == 'Korea, South':
                numDeathsDict['KOR'] = D_cases_column[i]
            elif D_country_column[i] == 'Russia':
                numDeathsDict['RUS'] = D_cases_column[i]
            elif D_country_column[i] == 'Bolivia':
                numDeathsDict['BOL'] = D_cases_column[i]
            elif D_country_column[i] == 'Tanzania':
                numDeathsDict['TZA'] = D_cases_column[i]
            elif D_country_column[i] == 'Congo (Kinshasa)':
                numDeathsDict['COD'] = D_cases_column[i]
            elif D_country_column[i] == 'Congo (Brazzaville)':
                numDeathsDict['COG'] = D_cases_column[i]
            elif D_country_column[i] == 'Syria':
                numDeathsDict['SYR'] = D_cases_column[i]
            elif D_country_column[i] == 'Burma':
                numDeathsDict['MMR'] = D_cases_column[i]
            elif D_country_column[i] == 'Laos':
                numDeathsDict['LAO'] = D_cases_column[i]
            elif D_country_column[i] == 'Vietnam':
                numDeathsDict['VNM'] = D_cases_column[i]
            elif D_country_column[i] == 'Moldova':
                numDeathsDict['MDA'] = D_cases_column[i]
            elif D_country_column[i] == 'Brunei':
                numDeathsDict['BRN'] = D_cases_column[i]
            elif D_country_column[i] == 'Yemen':
                numDeathsDict['YEM'] = D_cases_column[i]
            elif D_country_column[i] == 'Denmark' and D_province_column[i] == 'Greenland':
                numDeathsDict['GRL'] = D_cases_column[i]
            elif D_country_column[i] == 'France' and D_province_column[i] == 'French Guiana':
                numDeathsDict['GUF'] = D_cases_column[i]
            else:
                try:
                    country = pc.countries.get(name = D_country_column[i])
                    numDeathsDict[country.alpha_3] = D_cases_column[i]
                except:
                    continue


        for c in numTotalCasesDict:
            colorDict[c] = getColor(c)

        return render_template("home.html", theDict = numTotalCasesDict, deathDict = numDeathsDict, colorDict = colorDict, pageViews = views)

    else:
        age = request.form.get("age")
        print(age)
        gender = request.form.get("gender")
        print(gender)
        diseases = request.form.getlist("diseases")
        print(diseases)


        def calcPercent(age, gender, diseases):
            prob = 1.0

            if age=="80+":
                prob *= 0.142
            elif age=="70-79":
                prob *= .8
            elif age=="60-69":
                prob *= .36
            elif age=="50-59":
                prob *= .13
            elif age=="40-49":
                prob *= .04
            else:
                prob *= .02

            if gender == "m":
                prob *= 1.2
            else:
                prob *= .8

            for d in diseases:
                if d == "cardio":
                    prob += .1028
                elif d == "diabetes":
                    prob += .073
                elif d == "resp":
                    prob += .063
                elif d == "hypertension":
                    prob += .06
                elif d == "cancer":
                    prob += .056
                else:
                    prob += .009

            if prob >= .4:
                prob *= .75

            prob *= 100
            prob = round(prob, 2)
            return prob

        chances = calcPercent(age, gender, diseases)
        chances = 100 - chances

        def getColor(prob):
            if prob >= 95:
                return "#58cf46"
            elif prob > 90:
                return "#66b518"
            elif prob > 80:
                return "#8eb518"
            elif prob > 70:
                return "#8eb518"
            else:
                return "#b54718"

        return render_template("blank.html", prob = chances, color = getColor(chances), pageViews = views)
