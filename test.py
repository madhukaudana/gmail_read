from __future__ import print_function

import mail_request
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

def search_email(mail_request):

def main():
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle','rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:

        try:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
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


    try:
        service = build('gmail', 'v1', credentials=creds)

        results = service.users().messages().list(userId='me', q="is:unread after:"+mail_request.after_date + " before:" + mail_request.before_date).execute()
        messages = results.get('messages',[])

        if not messages:
            print('no messages found.')
        else:
            message_count = 0
            # for message in messages:
            #     msg = service.users().messages().get(userId='me', id=message['id']).execute()
            #     message_count += 1
            print("you have " + str(message_count) + " unread messages")

            message_count = int(input("how many messages do you want to read"))

            print('messages:')
            for message in messages[:message_count]:
                msg = service.users().messages().get(userId='me', id=message['id'],  format="full").execute()
                # message = service.users().messages().get(userId='me', id=message['id'], format="full").execute()

                print(msg['snippet'])
                print('\n')
                time.sleep(2)
                # ans = gmail_request.parse_msg(message)
                # soup = gmail_request(ans, features="html.parser")
                #
                # # kill all script and style elements
                # for script in soup(["script", "style"]):
                #     script.extract()  # rip it out
                # # get text
                # text = soup.get_text()
                # # break into lines and remove leading and trailing space on each
                # lines = (line.strip() for line in text.splitlines())
                # # break multi-headlines into a line each
                # chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                # # drop blank lines
                # mail_text = '\n'.join(chunk for chunk in chunks if chunk)
                # print('4', mail_text)
                # return str(mail_text)

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.'
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()