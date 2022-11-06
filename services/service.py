from datetime import date, timedelta

from sqlalchemy import exists
from sqlalchemy.orm import Session

from data.entities import *
from services.cache import cache

engine = create_engine(CONNECTION_STRING)

session = Session(bind=engine)

# Game #
def addGame():

    if session.query(Game.session).count() > 0:
        return

    session.add(Game(
        session=False
    ))

    session.commit()


def startSessionGame():
    session.query(Game).filter(User.session == False).update({'session': True})
    session.commit()



def stopSessionGame():
    session.query(Game).filter(User.session == True).update({'session': False})
    session.commit()

@cache(5)
def isGameStarted():
    return session.scalars(session.query(Game.session)).first()


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
    

def getMoneyUserInteger(chat_id):
    return session.query(User.money).filter(User.chat_id == chat_id).first()[0]

def getMoneyUserString(chat_id):
    money = session.query(User.money).filter(User.chat_id == chat_id).first()[0]
    return '$ {:,.2f}'.format(money).replace('$-', '-$')
