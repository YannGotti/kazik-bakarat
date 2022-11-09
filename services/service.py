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
    session.query(Game).filter(Game.isBet == False).update({'isBet': True})
    session.commit()

def getChatsId():
    return session.scalars(session.query(User.chat_id).filter(User.bet != 0)).all()


def getMessageId(chat_id):
    return session.query(User.current_message_game_id).filter(User.chat_id == chat_id).first()[0]

def Closebet():
    session.query(Game).filter(Game.isBet == True).update({'isBet': False})
    session.query(User).update({'select_color': "Нет"})
    session.query(User).update({'bet': 0})
    session.query(User).update({'current_message_game_id': 0})
    session.commit()

def setColorWin(color):
    session.query(Game).update({'win_color': color})

def getColorWin():
    return session.query(Game.win_color).first()[0]

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

def updateMoney(chat_id, bet):
    current_money = session.query(User.money).filter(User.chat_id == chat_id).first()[0]
    money = current_money + bet
    session.query(User).filter(User.chat_id == chat_id).update({'money': money})
    session.commit()

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

def allBetUser(chat_id):
    current_money = session.query(User.money).filter(User.chat_id == chat_id).first()[0]
    current_bet = session.query(User.bet).filter(User.chat_id == chat_id).first()[0]

    bet = current_money + current_bet
    session.query(User).filter(User.chat_id == chat_id).update({'money': 0})
    session.query(User).filter(User.chat_id == chat_id).update({'bet': bet})

    session.commit()

def startGameUser(chat_id, message_id):
    session.query(User).filter(User.chat_id == chat_id).update({'select_color': "Нет"})
    session.query(User).filter(User.chat_id == chat_id).update({'bet': 0})
    session.query(User).filter(User.chat_id == chat_id).update({'current_message_game_id': message_id})
    session.commit()

def setMessageIdUser(chat_id, message_id = 0):
    session.query(User).filter(User.chat_id == chat_id).update({'current_message_game_id': message_id})

def stopGameUser(chat_id):
    session.query(User).filter(User.chat_id == chat_id).update({'select_color': "Нет"})
    session.query(User).filter(User.chat_id == chat_id).update({'bet': 0})
    session.query(User).filter(User.chat_id == chat_id).update({'current_message_game_id': 0})
    session.commit()


