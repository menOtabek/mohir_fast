from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType

ORDER_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('in_progress', 'In Progress'),
    ('delivered', 'Delivered'),
]

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(Text, nullable=False)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    orders = relationship("Order", back_populates="user")  # Relationship to orders

    def __repr__(self):
        return self.username


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    status = Column(ChoiceType(ORDER_STATUS_CHOICES, impl=String(11)), default='pending')  # Use ChoiceType for status
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='orders')  # Relationship to user
    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship('Product', back_populates='orders')

    def __repr__(self):
        return f'<Order {self.id}>'


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    price = Column(Integer, nullable=False)
    orders = relationship("Order", back_populates="product")

    def __repr__(self):
        return f'<Product {self.id}>'
