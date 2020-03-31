import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import textract


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

    countries = [
     'Afghanistan',
     'Albania',
     'Algeria',
     'Andorra',
     'Angola',
     'Anguilla',
     'Argentina',
     'Armenia',
     'Aruba',
     'Australia',
     'Austria',
     'Azerbaijan',
     'Bahamas',
     'Bahrain',
     'Bangladesh',
     'Barbados',
     'Belarus',
     'Belgium',
     'Belize',
     'Benin',
     'Bermuda',
     'Bhutan',
     'Bolivia',
     'Bosnia And Herzegovina',
     'Botswana',
     'Brazil',
     'Bulgaria',
     'Burkina Faso',
     'Cambodia',
     'Cameroon',
     'Canada',
     'Cabo Verde',
     'Cayman Islands',
     'Central African Rep',
     'Chad',
     'Chile',
     'China',
     'Christmas Island',
     'Cocos Islands',
     'Colombia',
     'Comoros',
     'Congo',
     'Cook Islands',
     'Costa Rica',
     'Cote D`ivoire',
     'Croatia',
     'Cuba',
     'Cyprus',
     'Czech Republic',
     'Denmark',
     'Djibouti',
     'Dominica',
     'Dominican Republic',
     'East Timor',
     'Ecuador',
     'Egypt',
     'El Salvador',
     'Equatorial Guinea',
     'Eritrea',
     'Estonia',
     'Ethiopia',
     'Faroe Islands',
     'Fiji',
     'Finland',
     'France',
     'French Guiana',
     'French Polynesia',
     'Gabon',
     'Gambia',
     'Georgia',
     'Germany',
     'Ghana',
     'Gibraltar',
     'Greece',
     'Greenland',
     'Grenada',
     'Guadeloupe',
     'Guam',
     'Guatemala',
     'Guinea',
     'Guinea-Bissau',
     'Guyana',
     'Haiti',
     'Honduras',
     'Hong Kong',
     'Hungary',
     'Iceland',
     'India',
     'Indonesia',
     'Iran',
     'Iraq',
     'Ireland',
     'Israel',
     'Italy',
     'Jamaica',
     'Japan',
     'Jordan',
     'Kazakhstan',
     'Kenya',
     'Kiribati',
     'S. Korea',
     'Kuwait',
     'Kyrgyzstan',
     'Laos',
     'Latvia',
     'Lebanon',
     'Lesotho',
     'Liberia',
     'Libya',
     'Liechtenstein',
     'Lithuania',
     'Luxembourg',
     'Macau',
     'Macedonia',
     'Madagascar',
     'Malawi',
     'Malaysia',
     'Maldives',
     'Mali',
     'Malta',
     'Marshall Islands',
     'Martinique',
     'Mauritania',
     'Mauritius',
     'Mayotte',
     'Mexico',
     'Micronesia',
     'Moldova',
     'Monaco',
     'Mongolia',
     'Montserrat',
     'Morocco',
     'Mozambique',
     'Myanmar',
     'Namibia',
     'Nepal',
     'Netherlands',
     'New Caledonia',
     'New Zealand',
     'Nicaragua',
     'Niger',
     'Nigeria',
     'Norway',
     'Oman',
     'Pakistan',
     'Palau',
     'Panama',
     'Papua New Guinea',
     'Paraguay',
     'Peru',
     'Philippines',
     'Poland',
     'Portugal',
     'Puerto Rico',
     'Qatar',
     'Reunion',
     'Romania',
     'Russian Federation',
     'Rwanda',
     'Saint Kitts And Nevis',
     'Saint Lucia',
     'St Vincent/Grenadines',
     'Samoa',
     'San Marino',
     'Sao Tome',
     'Saudi Arabia',
     'Senegal',
     'Seychelles',
     'Sierra Leone',
     'Singapore',
     'Slovakia',
     'Slovenia',
     'Somalia',
     'South Africa',
     'Spain',
     'Sri Lanka',
     'Sudan',
     'Suriname',
     'Swaziland',
     'Sweden',
     'Switzerland',
     'Syria',
     'Taiwan',
     'Tanzania',
     'Thailand',
     'Togo',
     'Trinidad And Tobago',
     'Tunisia',
     'Turkey',
     'Uganda',
     'Ukraine',
     'UAE',
     'UK',
     'USA',
     'Uruguay',
     'Uzbekistan',
     'Vatican City',
     'Venezuela',
     'Vietnam',
     'Zambia',
     'Zimbabwe'
    ]


    numTotalCasesDict = {}
    print(numTotalCasesDict)


    text = textract.process("Country.docx")
    text = text.decode()
    text = text.replace('\n', '')
    print(text)
    print("––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––")

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


    print(numTotalCasesDict)

    return render_template("home.html")

    # return render_template("home.html", numCasesDict = numTotalCasesDict)