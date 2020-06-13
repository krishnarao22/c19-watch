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

age=None
gender=None
diseases=None

@app.route("/", methods=["GET", "POST"])
def home():

    views = db.execute("SELECT * FROM corona")
    views = views[0]['views']
    views += 1
    db.execute("UPDATE corona SET views = :views", views = views)


    if request.method == "GET":

        numTotalCasesDict = {}
        numDeathsDict = {}
        colorDict={}

        def getColor(country):
            numCases = numTotalCasesDict[country]
            numCases = int(numCases)
            if numCases >= 1000000:
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


        tc = pd.read_csv('countries.csv')
        country_column = tc['location']
        cases_column = tc['confirmed']



        # FIX UP SOME COUNTRIES
        # COLOR SCHEME
        # BEGIN OTHER PHASES.


        for i in range(0, 223):
            if country_column[i] == 'United States':
                numTotalCasesDict['USA'] = cases_column[i]
            elif country_column[i] == 'Venezuela':
                numTotalCasesDict['VEN'] = cases_column[i]
            elif country_column[i] == 'Iran':
                numTotalCasesDict['IRN'] = cases_column[i]
            elif country_column[i] == 'South Korea':
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
            elif country_column[i] == 'DR Congo':
                numTotalCasesDict['COD'] = cases_column[i]
            elif country_column[i] == 'Republic of the Congo':
                numTotalCasesDict['COG'] = cases_column[i]
            elif country_column[i] == 'Yemen':
                numTotalCasesDict['YEM'] = cases_column[i]
            elif country_column[i] == 'United Kingdom':
                numTotalCasesDict['GBR'] = cases_column[i]
            elif country_column[i] == 'Czech Republic':
                numTotalCasesDict['CZE'] = cases_column[i]
            elif country_column[i] == 'Ivory Coast':
                numTotalCasesDict['CIV'] = cases_column[i]
            else:
                try:
                    country = pc.countries.get(name = country_column[i])
                    numTotalCasesDict[country.alpha_3] = cases_column[i]
                except:
                    continue


        D_cases_column = tc['dead']
        row_count = 0

        for i in range(0,223):
            if country_column[i] == 'Venezuela':
                numDeathsDict['VEN'] = D_cases_column[i]
            elif country_column[i] == 'Iran':
                numDeathsDict['IRN'] = D_cases_column[i]
            elif country_column[i] == 'South Korea':
                numDeathsDict['KOR'] = D_cases_column[i]
            elif country_column[i] == 'Russia':
                numDeathsDict['RUS'] = D_cases_column[i]
            elif country_column[i] == 'Bolivia':
                numDeathsDict['BOL'] = D_cases_column[i]
            elif country_column[i] == 'Tanzania':
                numDeathsDict['TZA'] = D_cases_column[i]
            elif country_column[i] == 'DR Congo':
                numDeathsDict['COD'] = D_cases_column[i]
            elif country_column[i] == 'Republic of the Congo':
                numDeathsDict['COG'] = D_cases_column[i]
            elif country_column[i] == 'Syria':
                numDeathsDict['SYR'] = D_cases_column[i]
            elif country_column[i] == 'Burma':
                numDeathsDict['MMR'] = D_cases_column[i]
            elif country_column[i] == 'Laos':
                numDeathsDict['LAO'] = D_cases_column[i]
            elif country_column[i] == 'Vietnam':
                numDeathsDict['VNM'] = D_cases_column[i]
            elif country_column[i] == 'Moldova':
                numDeathsDict['MDA'] = D_cases_column[i]
            elif country_column[i] == 'Brunei':
                numDeathsDict['BRN'] = D_cases_column[i]
            elif country_column[i] == 'Yemen':
                numDeathsDict['YEM'] = D_cases_column[i]
            elif country_column[i] == 'United Kingdom':
                numDeathsDict['GBR'] = D_cases_column[i]
            elif country_column[i] == 'Czech Republic':
                numDeathsDict['CZE'] = D_cases_column[i]
            elif country_column[i] == 'Ivory Coast':
                numDeathsDict['CIV'] = D_cases_column[i]
            else:
                try:
                    country = pc.countries.get(name = country_column[i])
                    numDeathsDict[country.alpha_3] = D_cases_column[i]
                except:
                    continue


        for c in numTotalCasesDict:
            colorDict[c] = getColor(c)


        deathCount = 0
        for deaths in D_cases_column:
            deathCount += deaths
        totalCases = 0
        for cases in cases_column:
            totalCases += cases
        recoveredCol = tc['recovered']
        recoveredCount = 0
        for rv in recoveredCol:
            recoveredCount += rv
        totalCases -= (recoveredCount + deathCount)

        return render_template("home.html", theDict = numTotalCasesDict, deathDict = numDeathsDict, colorDict = colorDict, pageViews = views, total = totalCases, deaths = deathCount, recovered = recoveredCount)

    else:
        global age
        global gender
        global diseases
        age = request.form.get("age")
        gender = request.form.get("gender")
        diseases = request.form.getlist("diseases")

        return redirect("/results")

@app.route("/results", methods=["GET"])
def results():

    views = db.execute("SELECT * FROM corona")
    views = views[0]['views']
    views += 1
    db.execute("UPDATE corona SET views = :views", views = views)

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
        if prob >= 90:
            return "#02b552"
        elif prob > 80:
            return "#759c00"
        elif prob > 70:
            return "#979c00"
        else:
            return "#c22400"

    def classChance(prob):
        if prob >= 90:
            return 'high'
        elif prob >= 80:
            return  'medium'
        elif prob >= 70:
            return 'low'
        else:
            return 'vlow'

    return render_template("blank.html", prob = chances, color = getColor(chances), pageViews = views, chanceType = classChance(chances))
