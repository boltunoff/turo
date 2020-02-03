
# https://developers.google.com/people/quickstart/python
# authorize w/o browser:
#  https://stackoverflow.com/questions/46457093/google-drive-api-with-python-from-serverbackend-without-browser-autentication

# Step1
# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import csv
import pytz
from dateutil import parser

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def convert_timezone(utc_time_str):
    """
    Converts dates from Google Calendar ApI in UTC to Central time to match iPass time zone
    :param utc_time_str:
    :return:
    """
    utc_time_date = parser.parse(utc_time_str)
    utc_time_date.replace(tzinfo=pytz.timezone("UTC"))
    central_datetime = utc_time_date.astimezone(pytz.timezone("US/Central"))
    central_datetime_str = central_datetime.strftime("%Y-%m-%d %H:%M:%S")
    return central_datetime_str

def create_raw_calendar_extract_csv():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # calendarId from Google calendar for Turo
    calendarId = "b1jdbj417klp53n1allp98qst99pie8d@import.calendar.google.com"
    # Call the Calendar API
    from dateutil.relativedelta import relativedelta
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    three_years_ago = (datetime.datetime.utcnow() - relativedelta(years=+3)).isoformat() + 'Z'
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId= calendarId,
                                          timeMin=three_years_ago,
                                          maxResults=3000,
                                          singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    # new list of dictionaries

    events_data = []
    for event in events:
        print(type(event))
        print('One event >>>\n', event)
        events_dict = {}

        utc_start = event['start'].get('dateTime', event['start'].get('date'))
        utc_end = event['end'].get('dateTime', event['end'].get('date'))
        cst_start = convert_timezone(utc_start)
        cst_end = convert_timezone(utc_end)

        events_dict['start'] = cst_start
        events_dict['end'] = cst_end
        events_dict['summary'] = event['summary']
        events_dict['description'] = event['description']
        events_dict['created'] = convert_timezone(event['created'])
        events_dict['updated'] = convert_timezone(event['updated'])
        events_data.append(events_dict)
        # print(start, end, summary, description, created, updated)
        #break
    # writing raw extract csv file
    with open('raw_calendar_extract.csv', 'w') as csvFile:
        fields = ['start', 'end', 'summary', 'description', 'created', 'updated' ]
        writer = csv.DictWriter(csvFile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(events_data)

    print("Raw Extract writing completed")

    csvFile.close()
    print("::: Raw calendar extract is done")

def read_raw_csv_parse_turo_reservation_details(raw_calendar_extract_csv):
    """
    read raw cal extract, get all reservations, scrap each reservation detail, write enriched.csv
    :param raw_calendar_extract_csv:
    :return: enriched.csv
    """
    pass

def create_excel_report():
    # creating excel file with multiple sheets
    import pandas as pd
    from pandas import ExcelWriter
    import openpyxl
    #events_df = pd.DataFrame(events_data, columns= fields)
    events_df = pd.read_csv('raw_calendar_extract.csv')

    print(events_df.head(3))

    # read all summary to the list from df to find uniq MakeModelYear from summary
    summary_list = events_df.summary.tolist()
    # create uniq list of summaries w/o renter's name.
    # "Federico reserved Dmitry's Toyota Camry 12"    Removing" <Federico reserved Dmitry's> from string to find MakeModelYear:
    # Toyota Camry 12
    summary_uniq_cars = set([ ' '.join(s.split(' ')[3:]) for s in summary_list])

    # iterate on uniq MakeModelYear names to create filtered dataframes with only that MakeModelYear data
    # create list of dataframe names
    dfs_for_excel_sheet = []
    dfs_dict = {}
    for car_name in summary_uniq_cars:
        print('Looking for car name ::::', car_name)
        # providing name to serries based on car_name
        df_name_ser = str('_'.join(car_name.split(' '))) + "_serries"
        print('Creating Serries with True/False for the car name:::: ',df_name_ser)
        df_name_ser = events_df.summary.str.contains(car_name)
        # providing name to filtered dataframe based on car_name
        df_name = str('_'.join(car_name.split(' '))) + "_DF"
        print('Creating Dataframe with data only for :::: ', df_name)
        # create dataframe only containing records from serries
        df_new = events_df[df_name_ser]
        # create dict of car names and dataframes
        dfs_dict[df_name] = df_new

    print('Created DFs for cars::::')
    print(dfs_dict.keys())
    #print(dfs_dict['Mazda6_09_DF'])

    #DFs TO EXCEL
    with pd.ExcelWriter('calendar_by_car_report.xlsx') as writer:
        for k, v in dfs_dict.items():
            sheet_name = k
            df_name = v
            df_name.to_excel(writer, sheet_name, index=False)
    writer.save()
    print("::: Excel report is done: calendar_by_car_report.xlsx")

if __name__ == '__main__':
    create_raw_calendar_extract_csv()
    #TODO: complete function read_raw_csv_parse_turo_reservation
    #read_raw_csv_parse_turo_reservation_details()
    #create_excel_report()


'''
# getting from all events:
  'created': '2019-02-18T17:18:03.000Z', 
  'updated': '2019-02-18T17:18:04.011Z', 
  'summary': "Reta reserved Dmitry's Toyota Camry 12", 
  'description': 'https://turo.com/reservation/4221162', 
  'start': {'dateTime': '2019-02-18T18:30:00Z'}, 
  'end': {'dateTime': '2019-02-24T18:30:00Z'}, 
'''