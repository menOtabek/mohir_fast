from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, Table
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType

order_products = Table(
    'order_products',
    Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.id'), primary_key=True),
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True)
    email = Column(String(50), unique=True)
    password = Column(Text, unique=True)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    orders = relationship("Order", backref="users")

    def __repr__(self):
        return self.username


class Order(Base):
    ORDER_STATUS_CHOICES = (
        (1, 'Pending'),
        (2, 'In Progress'),
        (3, 'Delivered'),
    )
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    status = Column(ChoiceType(choices=ORDER_STATUS_CHOICES), default=1)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='orders')
    products = relationship('Product', secondary=order_products, back_populates='orders')

    def __repr__(self):
        return '<Order %r>' % self.id


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    price = Column(Integer)
    orders = relationship('Order', secondary=order_products, back_populates='products')

    def __repr__(self):
        return '<Product %r>' % self.id
