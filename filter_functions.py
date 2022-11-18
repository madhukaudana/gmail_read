from __future__ import print_function

import base64
import re

from bs4 import BeautifulSoup
from googleapiclient.errors import HttpError


MAIL_COUNTS = 1
to_mail = "tnetclean@gmail.com"

def search_criteria(param):
    SEARCH_CRITERIA = {
    'from': "no-reply.ncloud@griffeye.com",
    'to': param,
    'subject': "New User Account Created"
    }
    return SEARCH_CRITERIA
BASE_DIR = 'mail_box'

def build_search_criteria(query_dict):
    query_string = ''
    for key, value in query_dict.items():
        if value:
            query_string += key + ':' + value + ' '

    return query_string

def get_mail_list(service, limit, query):
        # Call the Gmail API
        try:
            results = service.users().messages().list(
                userId='me', maxResults=limit, q=query).execute()
        except HttpError as err:
             raise

        messages = results.get('messages', [])

        return messages
    
def parse_msg(msg):
    if msg.get("payload").get("body").get("data"):
        return base64.urlsafe_b64decode(msg.get("payload").get("body").get("data").encode("ASCII")).decode("utf-8")
    return msg.get("snippet")

def get_user_cred(content ):
    user_reg = re.findall(r"(?:Username\: ).+\b", content)
    password_reg = re.findall(r"(?:Password\: ).+\b", content)
    username = str(user_reg).join(user_reg)
    password = str(password_reg).join(password_reg)
    split_user =  username.split()[1]
    split_pass =  password.split()[1]
    auth_list = [split_user,split_pass]
    return auth_list

