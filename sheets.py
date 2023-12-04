# Reference: https://medium.com/@jb.ranchana/write-and-append-dataframes-to-google-sheets-in-python-f62479460cf0

import os
from dotenv import load_dotenv
from datetime import datetime
import gspread
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials
from pydrive.auth import GoogleAuth
import pandas as pd

from messages import messages
from constants import *
from sms import sendSMS

load_dotenv('/.env')

def get_df():
    sheet_url = os.environ['SHEET_URL']
    url_1 = sheet_url.replace("/edit#gid=", "/export?format=csv&gid=")

    df = pd.read_csv(url_1)
    print(df)
    return df

def get_sheet():
    scopes = ['https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive']

    credentials = Credentials.from_service_account_file('./service_account.json', scopes=scopes)

    gc = gspread.authorize(credentials)

    # open a google sheet
    gs = gc.open(os.environ['GSHEET_NAME'])
    # select a work sheet from its name
    worksheet1 = gs.worksheet(os.environ['WORKSHEET_NAME'])
    values_list = worksheet1.get_all_values
    print(values_list)
    return worksheet1


def df2sheet(df):
    # dataframe (create or import it)
    worksheet = get_sheet()
    # write to dataframe
    worksheet.clear()
    set_with_dataframe(worksheet=worksheet, dataframe=df, include_index=False,
    include_column_header=True, resize=True)

    return df


def get_timestamp():
    return datetime.today().strftime(DATE_FORMAT)


def get_day_diff(past):
    past = datetime.strptime(past, DATE_FORMAT)
    now = datetime.strptime(get_timestamp(), DATE_FORMAT)
    # return (now - past).days
    return (now - past).seconds / 60


def process(row, group, index, phone):
    groupkey = 'group' + str(group)
    try:
        message = messages[groupkey][index]
        print('Sending...\n  >>>  ', message, '\n')
        sendSMS(message, phone)
        row[INDEX] = index + 1
        row[DATE_SINCE] = get_timestamp()
    except:
        print('Update group number\n')
        ## 1. group number ++
        newgroup = group + 1
        newindex = 0
        newgroup_key = 'group' + str(newgroup)
        ## 2. handle group accordingly
        message = messages[newgroup_key][newindex]

        ## update columns
        row[GROUP] = newgroup
        row[INDEX] = newindex
        row[DATE_SINCE] = get_timestamp()


def update(row):
    ## 1. get the group number
    group = row[GROUP]
    index = row[INDEX]
    str_phone = str(row[PHONE])
    phone = '+1' + str_phone

    if str_phone == '91819132':
        phone = '+65' + str_phone

    if group == 1:
        ## 2a. if throws array index out of bounds exception, update group
        process(row, group, index, phone)

    ## 2b. if group 2, check if it's been 3 days. if group 3, check if it's been a week
    elif group == 2:
        diff = get_day_diff(row[DATE_SINCE])
        print('been', diff, 'mins')
        ## if day 3 since last message, send new message
        if 3 <= diff < 4:
            process(row, group, index, phone)
    
    elif group == 3:
        diff = get_day_diff(row[DATE_SINCE])
        print(diff, 'minute(s)\n')
        ## if day 7 since last message, send new message
        if 7 <= diff < 8:
            process(row, group, index, phone)

    else:
        print('Completed set of messages.')

    return row


def run():
    df = get_df()

    upd_df = df.apply(update, axis=1)
    upd_df = df2sheet(upd_df)
    print(upd_df)
