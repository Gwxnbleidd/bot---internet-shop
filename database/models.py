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

# class CartridgesTable(Base):
#     __tablename__ = 'cartridges'

#     id: Mapped[int] =  mapped_column(primary_key= True)
#     name: Mapped[str]
#     price: Mapped[float]
#     quantity: Mapped[int]

# class LiquidsTable(Base):
#     __tablename__ = 'liquids'

#     id: Mapped[int] =  mapped_column(primary_key= True)
#     name: Mapped[str]
#     strength: Mapped[bool]
#     cold: Mapped[bool]
#     price: Mapped[float]
#     quantity: Mapped[int]

class ProductTypesTable(Base):
    __tablename__ = 'product_types'

    id: Mapped[int] =  mapped_column(primary_key= True)
    name: Mapped[str]

class BasketTable(Base):
    __tablename__ = 'basket'

    id: Mapped[int] =  mapped_column(primary_key= True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    product_name: Mapped[str]
    product_price: Mapped[float]
    product_quantity: Mapped[int]

class ProductTable(Base):
    __tablename__ = 'products'

    id: Mapped[int] =  mapped_column(primary_key= True)
    type_id: Mapped[int] = mapped_column(ForeignKey('product_types.id', ondelete='CASCADE'))
    name: Mapped[str]
    price: Mapped[float]
    quantity: Mapped[int]
    strength: Mapped[bool] = mapped_column(nullable=True) 
    cold: Mapped[bool] = mapped_column(nullable=True)