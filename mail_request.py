
from __future__ import print_function

import base64
import re

from bs4 import BeautifulSoup
from googleapiclient.errors import HttpError

to_mail = "tnetclean@gmail.com"

    # after_date = input("enter after date")
    # before_date = input("enter before date")
after_date = "2022/11/01"
before_date = "2022/11/05"

def search_parameters(param):
    SEARCH_CRITERIA = {
    'from': "no-reply.ncloud@griffeye.com",
    'to': param,
    'subject': "New User Account Created"
    }
    return SEARCH_CRITERIA
BASE_DIR = 'mail_box'


def get_user_cred(content ):
    user_reg = re.findall(r"(?:Username\: ).+\b", content)
    password_reg = re.findall(r"(?:Password\: ).+\b", content)
    username = str(user_reg).join(user_reg)
    password = str(password_reg).join(password_reg)
    split_user =  username.split()[1]
    split_pass =  password.split()[1]
    auth_list = [split_user,split_pass]
    return auth_list

def parse_msg(msg):
    if msg.get("payload").get("body").get("data"):
        return base64.urlsafe_b64decode(msg.get("payload").get("body").get("data").encode("ASCII")).decode("utf-8")
    return msg.get("snippet")