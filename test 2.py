from __future__ import print_function

import os.path
import pickle
import time

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    # if os.path.exists('token.json'):
    if os.path.exists('token.pickle'):
        with open('token.pickle','rb') as token:
            creds = pickle.load(token)
        # creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            # token.write(creds.to_json())
            pickle.dump(creds, token)
    # try:
        # Call the Gmail API
    service = build('gmail', 'v1', credentials=creds)

    # after_date = input("enter after date")
    after_date = "2022/11/01"
    # before_date = input("enter before date")
    before_date = "2022/11/15"
    results = service.users().messages().list(userId='me', q="is:unread after:"+after_date + " before:" + before_date).execute()
    # print(results)
    messages = results.get('messages',[])



    message_count = int(input("how many messages do you want to read"))
    if not messages:
        print('no messages found.')
    else:
        print('messages:')
        for message in messages[:message_count]:
            msg = service.users().messages().get(userId='me', id = message['id']).execute()
            print(msg['snippet'])
            print('\n')
            time.sleep(2)



if __name__ == '__main__':
    main()