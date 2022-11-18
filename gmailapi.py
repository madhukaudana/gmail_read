from __future__ import print_function
import test
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

def read_gmail():
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle','rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:

        try:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                start = time.time()
                flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', SCOPES)
                print(flow)

                creds = flow.run_local_server(port=0)

                print(creds)
            # Save the credentials for the next run
                with open('token.pickle', 'wb') as token:
                    # token.write(creds.to_json())
                    pickle.dump(creds, token)

        except:
            exit()

    service = build('gmail', 'v1', credentials=creds)


    results = service.users().messages().list(userId='me', q="is:unread after:"+test.after_date + " before:" + test.before_date).execute()
    messages = results.get('messages',[])

    if not messages:
        print('no messages found.')
    else:
        message_count = 0
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            message_count += 1
        print("you have " + str(message_count) + " unread messages")



        message_count = int(input("how many messages do you want to read"))
        if not messages:
            print('no messages found.')
        else:
            print('messages:')
            for message in messages[:message_count]:
                msg = service.users().messages().get(userId='me', id=message['id']).execute()
                print(msg['snippet'])
                print('\n')
                time.sleep(2)

if __name__ == '__main__':
    read_gmail()
