from sqlalchemy import select, delete
from enum import Enum

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
            return [res.id,res.name,res.price,res.quantity]
        else:
            res = session.execute(select('*').select_from(CartridgesTable))
            return res.fetchall()

def get_liquid(id: int = None,strength: bool| None = None, cold: bool| None = None):
    with session_factory() as session:
        if id:
            res = session.get(LiquidsTable,id)
            return [res.id, res.name, res.price, res.quantity]
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

def add_product_in_basket(user_id: int, product_name: str, product_price: float, product_quantity: str):
    with session_factory() as session:
        session.add(BasketTable(user_id=user_id, product_name=product_name, product_price=product_price,
                                 product_quantity=product_quantity))
        session.commit()
    
def get_basket(user_id: int, id: int = None):
    with session_factory() as session:
        if id:
            res = session.get(BasketTable,id)
            return [res.id, res.name, res.price, res.quantity]
        response = select('*').select_from(BasketTable).filter_by(user_id = user_id)
        res = session.execute(response)
        if res:
            return res.fetchall()
        return None

def delete_product_from_basket(id: int):
    with session_factory() as session:
        session.execute(delete(BasketTable).filter_by(id=id))
        session.commit()