from sqlalchemy import select
from enum import Enum

import sys
import os
sys.path.append(os.pardir)
from database.engine import engine,Base, session_factory
from database.models import UsersTable, CartridgesTable, LiquidsTable, BasketTable

def create_tables():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def add_user_in_db(id: int, name: str, number: str, promocode: str):
    with session_factory() as session:
        # Проверяем есть ли такой пользователь
        res = session.execute(select('*').select_from(UsersTable).filter_by(number=number))
        if not res.fetchone():
            session.add(UsersTable(id=id, username=name, number=number, promocode=promocode, number_of_guests=0))
            session.commit()
        else:
            raise Exception('Пользователь с таким номером уже существует')

def get_user_from_db(id: int):
    with session_factory() as session:
        res = session.execute(select('*').select_from(UsersTable).filter_by(id=id))
        user = res.fetchone()
        if user:
            return user
        return None

def get_cartridges(id: int = None):
    with session_factory() as session:
        if id:
            res = session.get(CartridgesTable, id)
            return res
        else:
            res = session.execute(select('*').select_from(CartridgesTable))
            return res.fetchall()

def get_liquid(strength: bool| None = None, cold: bool| None = None):
    with session_factory() as session:
        response = select('*').select_from(LiquidsTable)
        if not (strength is None):
            if strength:
                response = response.filter_by(strength = True)
            else:
                response = response.filter_by(strength = False)
        if not (cold is None):
            if cold:
                response = response.filter_by(cold = True)
            else:
                response = response.filter_by(cold = False)
        res = session.execute(response)
        return res.fetchall()
#def add_product_in_basket()