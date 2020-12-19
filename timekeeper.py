# import the required libraries

import pickle
import os.path
import base64
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import email
from bs4 import BeautifulSoup
import re


from datetime import datetime, timedelta

# Define the SCOPES. If modifying it, delete the token.pickle file.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly','https://www.googleapis.com/auth/calendar']

def courses(course):
    res = re.findall(r'\w+', course)
    for i in res:
        print(i)
        if (i=="ESD" or i=="CN" or i=="ME"):
            return i
    return "No"
def time_search(time):
    for element in range(0, len(time)):
         if (time[element]=='1' or time[element]=='2'):
             return time[element]
    return "No"
def keyword_search(keyword):
    res = re.findall(r'\w+', keyword)
    for i in res:
        print(i)
        if (i=="Quiz" or i=="Exam" or i=="Assignment"):
            return i
    return "No"



def searchin_mail(subject ,sender ,body):
    print("\n")
    print("Sender of the mail:")
    print("Search begins\n")
    #lets search for the course or time or keyword in subject sender body
    course1=course(subject)
    course2=course(body)

    time1=time_search(subject)
    time2=time_search(body)

    Event=keyword_search(body)


    print(course1, " ", course2, " ", time1, " ", time2, " ", Event, "\n")
    print("Search Ends !!!!!!!!!!\n")
    if(course1=='No' and course2=='No'):
        return
    if(course1=='ESD' or course1=='CN' or course=='ME'):
        course3=course1
    else:
        course3=course2

    if(time1=='No'):
        time3=time1
    else:
        time3=time2

    print("\n")
    print("Eureka")
    print("You have", Event ,"of", course3 , "on ", time3)
    print("\n")

    #UPDATE in Google Calender







def getEmails():

    # Variable creds will store the user access token.
    # If no valid token found, we will create one.
    creds = None

    # The file token.pickle contains the user access token.
    # Check if it exists
    if os.path.exists('token.pickle'):

        # Read the token from the file and store it in the variable creds
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If credentials are not available or are invalid, ask the user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the access token in token.pickle file for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Connect to the Gmail API
    service = build('gmail', 'v1', credentials=creds)

    # request a list of all the messages
    result = service.users().messages().list(userId='me').execute()

    # We can also pass maxResults to get any number of emails. Like this:
    # result = service.users().messages().list(maxResults=200, userId='me').execute()
    messages = result.get('messages')

    # messages is a list of dictionaries where each dictionary contains a message id.

    # iterate through all the messages
    for msg in messages:
        # Get the message from its id
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()

        # Use try-except to avoid any Errors
        try:
            # Get value of 'payload' from dictionary 'txt'
            payload = txt['payload']
            headers = payload['headers']

            # Look for Subject and Sender Email in the headers
            for d in headers:
                if d['name'] == 'Subject':
                    subject = d['value']
                if d['name'] == 'From':
                    sender = d['value']

            # The Body of the message is in Encrypted format. So, we have to decode it.
            # Get the data and decode it with base 64 decoder.
            parts = payload.get('parts')[0]
            data = parts['body']['data']
            data = data.replace("-","+").replace("_","/")
            decoded_data = base64.b64decode(data)

            # Now, the data obtained is in lxml. So, we will parse
            # it with BeautifulSoup library
            soup = BeautifulSoup(decoded_data , "lxml")
            body = soup.body()
            # Printing the subject, sender's email and message
            print("*************Mail***********")
            print("Subject: ", subject)
            print("From: ", sender)
            print("Message: ", body)
            searchin_mail(subject, sender, body)
            print("Search completed\n")
            print('\n')
        except:
            pass


getEmails()




def calendarz():
    creds = None

    # The file token.pickle contains the user access token.
    # Check if it exists
    if os.path.exists('token.pickle'):

        # Read the token from the file and store it in the variable creds
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If credentials are not available or are invalid, ask the user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the access token in token.pickle file for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build("calendar", "v3", credentials=creds)
    start_time = datetime(2020, 12, 23, 19, 30, 0)
    end_time = start_time + timedelta(hours=1)
    event = {
            'summary': 'hiya',
            'location': '',
            'description': '',
            'start': {
                'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': 'Asia/Kolkata',
            },
            'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'Asia/Kolkata',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }
    service.events().insert(calendarId='primary', body=event).execute()

calendarz()