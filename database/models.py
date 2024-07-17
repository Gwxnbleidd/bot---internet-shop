from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.schema import ForeignKey

from database.engine import Base

class UsersTable(Base):
    __tablename__ = 'users'

    id: Mapped[int] =  mapped_column(primary_key= True)
    username: Mapped[str]
    number: Mapped[str]
    promocode: Mapped[str]
    number_of_guests: Mapped[str]

class CartridgesTable(Base):
    __tablename__ = 'cartridges'

    id: Mapped[int] =  mapped_column(primary_key= True)
    name: Mapped[str]
    price: Mapped[float]
    quantity: Mapped[int]

class LiquidsTable(Base):
    __tablename__ = 'liquids'

    id: Mapped[int] =  mapped_column(primary_key= True)
    name: Mapped[str]
    strength: Mapped[bool]
    cold: Mapped[bool]
    price: Mapped[float]
    quantity: Mapped[int]

class BasketTable(Base):
    __tablename__ = 'basket'

    id: Mapped[int] =  mapped_column(primary_key= True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id',ondelete='CASCADE'))
    product_name: Mapped[str]
    product_price: Mapped[float]
    product_quantity: Mapped[int]