from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def create_filter():
    """Create a filter.
    Returns: Draft object, including filter id.

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    # creds, _ = google.auth.default()

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:


        # create gmail api client
        service = build('gmail', 'v1', credentials=creds)

        label_name = 'IMPORTANT'
        filter_content = {
            'criteria': {
                'from': 'gsuder1@workspacesamples.dev'
            }
            # 'action': {
            #     'addLabelIds': [label_name],
            #     'removeLabelIds': ['INBOX']
            # }
        }

        # pylint: disable=E1101
        result = service.users().settings().filters().create(
            userId='me', body=filter_content).execute()
        print(F'Created filter with id: {result.get("id")}')

    except HttpError as error:
        print(F'An error occurred: {error}')
        result = None

    return result.get('id')


if __name__ == '__main__':
    create_filter()