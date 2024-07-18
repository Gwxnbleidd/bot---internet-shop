from sqlalchemy import select, delete,update
from enum import Enum

from database.engine import engine,Base, session_factory
from database.models import UsersTable, BasketTable,ProductTypesTable, ProductTable

def create_tables():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with session_factory() as session:
        session.add(ProductTypesTable(name='Картриджи'))
        session.add(ProductTypesTable(name='Алкоголь'))
        session.commit()


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
            res = session.get(ProductTable, id)
            return [res.id,res.name,res.price,res.quantity]
        else:
            res = session.execute(select('*').select_from(ProductTable).filter_by(type_id=1))
            return res.fetchall()

def get_liquid(id: int = None,strength: bool| None = None, cold: bool| None = None):
    with session_factory() as session:
        if id:
            res = session.get(ProductTable,id)
            return [res.id, res.name, res.price, res.quantity]
        response = select('*').select_from(ProductTable).filter_by(type_id=2)
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

def add_product_in_basket(user_id: int,product_id:int,product_name: str, product_price: float, product_quantity: str):
    with session_factory() as session:
        session.add(BasketTable(user_id=user_id, product_id=product_id, product_name=product_name, 
                                product_price=product_price, product_quantity=product_quantity))
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

def check_products(user_id: int):
    with session_factory() as session:
        response = (select(BasketTable.product_name)
        .select_from(BasketTable)
        .join(ProductTable, ProductTable.id == BasketTable.product_id)
        .where(BasketTable.user_id == user_id)
        .where(ProductTable.quantity == 0))
        res = session.execute(response)
        if not res.fetchall():
            return True
        else:
            raise Exception()
    
def buy_products(user_id: int):
    with session_factory() as session:
        response = select(BasketTable.product_id).select_from(BasketTable).filter_by(user_id=user_id)
        product_ids = [row[0] for row in session.execute(response)]

        # Проверка наличия товаров
        if not product_ids:
            raise Exception(f"Ваша корзина пуста.")

        # Обновление количества товаров
        for product_id in product_ids:
            response = update(ProductTable).where(ProductTable.id == product_id)
            response = response.values(quantity=ProductTable.quantity - 1)
            session.execute(response)
        
        session.execute(delete(BasketTable).filter_by(user_id=user_id))

        session.commit()

