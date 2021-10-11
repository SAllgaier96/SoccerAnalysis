#!/usr/bin/env python
# coding: utf-8

# Pandas, Plotly, and NumPy modules
import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd

# Google Sheets Modules
import gspread
from df2gspread import  df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials

# Misc. Modules
import json
import sys

# Shift Number DO NOT CHANGE
SHIFT_NUMBER = 4

# Shift Encryption
def encrypt(str, shift):
    encryptedString = ''
    for char in str:
        encryptedString += chr(ord(char) + shift)
    return encryptedString

# Shift Decryption
def decrypt(str, shift):
    decryptedString = ''
    for char in str:
        decryptedString += chr(ord(char) - shift)
    return decryptedString

# Encrypts the JSON file
def encryptJson(filename, shift):
    file = open(f"assets/{filename}", 'r+')
    data = json.load(file)
    for key in data:
        data[key] = encrypt(data[key], shift)
    file.seek(0)
    file.write(json.dumps(data))
    file.truncate()
    print(data)
    
# Decrypts the JSON file
def decryptJson(filename, shift):
    file = open(f"assets/{filename}", 'r+')
    data = json.load(file)
    for key in data:
        data[key] = decrypt(data[key], shift)
    file.seek(0)
    file.write(json.dumps(data))
    file.truncate()
    print(data)

# Decrypt the creds.json file at the before the data pull
decryptJson('creds2.json', SHIFT_NUMBER)
    
# Spreadsheet Connection
try:
    print('Starting Data Pull...')
    WORKSHEET_ID = '1-kUlYLeDEQyzw2PYnLn6quq7kFYJbduI_Zrk_bQ7_9A'
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    path = 'assets/creds2.json'
    google_key_file = path
    credentials = ServiceAccountCredentials.from_json_keyfile_name(google_key_file, scope)
    gc = gspread.authorize(credentials)
    # Opening the workbook
    workbook = gc.open_by_key(WORKSHEET_ID)

    # Opening separate worksheets
    AnalysisDashboard = workbook.worksheet('AnalysisDashboard')
    PlayerOllie = workbook.worksheet('PlayerOllie')
    TeamOllie = workbook.worksheet('TeamOllie')
    print('Data Pull SUCCESS')
except:
    print('Data Pull FAILED')
    
#Encrypt the creds.json file once finished with the data pull
encryptJson('creds2.json', SHIFT_NUMBER)

# Returns the layout of the Dash Plotly Dashboard
def dash_layout():
    return html.Div(className='body', children=[
                html.Div(className='title', children=[
                    html.H1(className='headers', children=[
                        '[Insert Player Name Here]'
                    ]),
                    html.H2(className='headers', children=[
                        'Player Report'
                    ])
                ]),
                html.Div(className='stats', children=[
                    html.Div(className='offense', children=[
                        html.H2(className='headers', children=[
                            'Offense'
                        ]),
                        html.Div(className='offense-stats', children=[
                            html.Ul(className='stats-list', children=[
                                html.Li('Goals: '),
                                html.Li('Shots: '),
                                html.Li('Shots on Goal: '),
                                html.Li('Assists: '),
                                html.Li('Passes: '),
                                html.Li('Success Rate with Ball: '),
                                html.Li('Turnovers: ')
                            ]),
                            html.Ul(className='stats-numbers', children=[
                                html.Li('1'),
                                html.Li('2'),
                                html.Li('3'),
                                html.Li('4'),
                                html.Li('5'),
                                html.Li('60%'),
                                html.Li('700')
                            ])
                        ])
                    ]),
                    html.Div(className='defense', children=[
                        html.H2(className='headers', children=[
                            'Defense'
                        ]),
                        html.Div(className='defense-stats', children=[
                            html.Ul(className='stats-list', children=[
                                html.Li('Fouls: '),
                                html.Li('Recoveries: '),
                                html.Li('Yellow Cards: '),
                                html.Li('Red Cards: ')
                            ]),
                            html.Ul(className='stats-numbers', children=[
                                html.Li('1'),
                                html.Li('2'),
                                html.Li('30%'),
                                html.Li('400')
                            ])
                        ])
                    ]),
                    html.Div(className='work', children=[
                        html.H2(className='headers', children=[
                            'Work'
                        ]),
                        html.Div(className='work-stats',children=[
                            html.Ul(className='stats-list', children=[
                                html.Li('Participation %: '),
                                html.Li('Passes Completed: '),
                                html.Li('Two Mile (seconds): ')
                            ]),
                            html.Ul(className='stats-numbers', children=[
                                html.Li('1'),
                                html.Li('20%'),
                                html.Li('300')
                            ])
                        ])
                    ])
                ]),
                html.Div(className='chart-container', children=[
                    html.Div(className='radial', children=[
                        html.Div(className='radial-chart', children=[
                            html.P('Insert Radial Here')
                        ]),
                        html.Div(className='radial-stats', children=[
                            html.P('Insert Radial Stats Here')
                        ])
                    ]),
                    html.Div(className='position', children=[
                        html.P('Insert Position Here')
                    ]),
                    html.Div(className='line-chart', children=[
                        html.P('Insert Line Here')
                    ])
                ])
            ])

app = dash.Dash(__name__)

app.layout = dash_layout()

if __name__ == '__main__':
    app.run_server(debug=False)
