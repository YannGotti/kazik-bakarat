from datetime import date, timedelta

from sqlalchemy import exists
from sqlalchemy.orm import Session

from data.entities import *
from services.cache import cache

engine = create_engine(CONNECTION_STRING)

session = Session(bind=engine)

# Game #
def addGame():

    if session.query(Game.isBet).count() > 0:
        return

    session.add(Game(
        isBet=False
    ))

    session.commit()


def OpenBet():
    session.query(Game).filter(User.isBet == False).update({'isBet': True})
    session.commit()



def Closebet():
    session.query(Game).filter(User.isBet == True).update({'isBet': False})
    session.commit()

@cache(1)
def isBetStarted():
    return session.scalars(session.query(Game.isBet)).first()


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

@cache(1)
def getColorBetUser(chat_id):
    return session.query(User.select_color).filter(User.chat_id == chat_id).first()[0]

def setColorBetUser(chat_id, color):
    session.query(User).filter(User.chat_id == chat_id).update({'select_color': color})

def getBetUser(chat_id):
    return session.query(User.bet).filter(User.chat_id == chat_id).first()[0]

def updateBetUser(chat_id, bet):
    current_money = session.query(User.money).filter(User.chat_id == chat_id).first()[0]
    
    current_bet = getBetUser(chat_id)

    money = current_money - bet
    new_bet = int(current_bet) +  bet

    session.query(User).filter(User.chat_id == chat_id).update({'money': money})
    session.query(User).filter(User.chat_id == chat_id).update({'bet': new_bet})

    session.commit()

def startGameUser(chat_id):
    session.query(User).filter(User.chat_id == chat_id).update({'select_color': "Нет"})
    session.query(User).filter(User.chat_id == chat_id).update({'bet': 0})