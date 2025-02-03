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


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    price = Column(Integer, nullable=False)
    order_items = relationship('OrderItem', back_populates='product')  # Relationship to order items

    def __repr__(self):
        return f'<Product {self.id}>'


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    status = Column(ChoiceType(ORDER_STATUS_CHOICES), default='pending')  # Use ChoiceType for status
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='orders')  # Relationship to user
    order_items = relationship('OrderItem', back_populates='order')  # Relationship to order items

    def __repr__(self):
        return f'<Order {self.id}>'


class OrderItem(Base):
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    product = relationship('Product', back_populates='order_items')  # Relationship to product
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    order = relationship('Order', back_populates='order_items')  # Relationship to order

    def __repr__(self):
        return f'{self.quantity} x {self.product.name if self.product else "Unknown Product"}'
