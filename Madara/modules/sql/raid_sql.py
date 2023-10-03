import threading

from sqlalchemy import Column, String

from Madara.modules.sql import BASE, SESSION


class RaidChats(BASE):
    __tablename__ = "raid_chats"
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = chat_id


RaidChats.__table__.create(checkfirst=True)
INSERTION_LOCK = threading.RLock()


def is_raid(chat_id):
    try:
        chat = SESSION.query(RaidChats).get(str(chat_id))
        return bool(chat)
    finally:
        SESSION.close()


def set_raid(chat_id):
    with INSERTION_LOCK:
        raidchat = SESSION.query(RaidChats).get(str(chat_id))
        if not raidchat:
            raidchat = RaidChats(str(chat_id))
        SESSION.add(raidchat)
        SESSION.commit()


def rem_raid(chat_id):
    with INSERTION_LOCK:
        raidchat = SESSION.query(RaidChats).get(str(chat_id))
        if raidchat:
            SESSION.delete(raidchat)
        SESSION.commit()


def get_all_raid_chats():
    try:
        return SESSION.query(RaidChats.chat_id).all()
    finally:
        SESSION.close()
