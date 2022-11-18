from __future__ import print_function
import email
import sys
import os.path
import base64
import filter_functions


from bs4 import BeautifulSoup
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def readGmail():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    # cred_path= os.path.abspath('./resources/libraries/read_gmail_using_api/creds.json')
    cred_path = os.path.abspath('D:/netClean/test-automation/NTest/resources/libraries/read_gmail_using_api/creds.json')

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        try:
                creds and creds.expired and creds.refresh_token
                creds.refresh(Request())
        except:
            if os.path.exists("token.json"):
                        os.remove("token.json")
                        flow = InstalledAppFlow.from_client_secrets_file(
                            cred_path, SCOPES)
                        creds = flow.run_local_server(port=0)

            # if creds and creds.expired and creds.refresh_token:
            #     creds.refresh(Request())

            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    cred_path, SCOPES)
                creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        query = filter_functions.build_search_criteria(filter_functions.search_criteria(filter_functions.to_mail))
        print(filter_functions)
        print(query)
        messages = filter_functions.get_mail_list(service,filter_functions.MAIL_COUNTS, query)
        print(messages)

        for message in messages:
            message = service.users().messages().get(userId='me', id=message['id'], format="full").execute()
            ans = filter_functions.parse_msg(message)
            soup = BeautifulSoup(ans, features="html.parser")

            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()    # rip it out
            # get text
            text = soup.get_text()
            # break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # drop blank lines
            mail_text = '\n'.join(chunk for chunk in chunks if chunk)
            print('4', mail_text)
            return str(mail_text)
                                          
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.'
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    readGmail()
