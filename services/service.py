import calendar
import json
import random
import shutil
from datetime import date, timedelta

from sqlalchemy import exists
from sqlalchemy.orm import Session

from data.entities import *
from services.cache import cache

engine = create_engine(CONNECTION_STRING)

session = Session(bind=engine)

# User #
def addUser(chat_id):
    session.add(User(
        chat_id=chat_id
    ))
    session.commit()


def userExists(chat_id):
    return session.query(exists().where(User.chat_id == chat_id)).scalar()


def getTwitchName(chat_id):
    return session.query(User.twitch_name).filter(User.chat_id == chat_id).first()[0]


def addTwitchName(chat_id, twitch_name):
    session.query(User).filter(User.chat_id == chat_id).update({'twitch_name': twitch_name})
    session.commit()