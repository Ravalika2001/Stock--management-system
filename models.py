from sqlalchemy import Column, ForeignKey, Integer, Float, String, Date, Numeric, create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
engine = create_engine("postgresql://postgres:Password0#@database1.cuetvdodk2bh.us-east-1.rds.amazonaws.com:5432/final ")
Base.metadata.bind = engine


class Supplier(Base):
    __tablename__ = 'suppliers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    contact_number = Column(String)
    orders = relationship("SupplierOrder", back_populates="supplier", cascade="all, delete", single_parent=True)
    


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    name = Column(String)
    unit_price = Column(Numeric(10, 2))
    description = Column(String)

    category = relationship("Category", foreign_keys=[category_id], cascade="all, delete", single_parent=True)
    supplier_order_items = relationship("SupplierOrderItem", back_populates="product", cascade="all, delete", single_parent=True)
    consumer_order_items = relationship("ConsumerOrderItem", back_populates="product", cascade="all, delete", single_parent=True)


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id', ondelete="CASCADE"))
    category_name = Column(String)


class SupplierOrder(Base):
    __tablename__ = 'supplier_orders'

    id = Column(Integer, primary_key=True)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'))
    order_date = Column(Date)
    total_amount = Column(Float)

    supplier = relationship("Supplier", back_populates="orders")
    items = relationship("SupplierOrderItem", back_populates="order", cascade="all, delete", single_parent=True)


class SupplierOrderItem(Base):
    __tablename__ = 'supplier_order_items'

    id = Column(Integer, primary_key=True)
    supplier_order_id = Column(Integer, ForeignKey('supplier_orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    item_name = Column(String)
    quantity = Column(Integer)
    unit_price = Column(Float)
    total_price = Column(Float)

    product = relationship("Product", back_populates="supplier_order_items")
    order = relationship("SupplierOrder", back_populates="items")

    def calculate_total_price(self):
            if self.quantity is not None and self.product and self.product.unit_price is not None:
                self.total_price = self.quantity * self.product.unit_price
            else:
                self.total_price = 0 # Set a default value if any of the required fields are None


class ConsumerOrder(Base):
    __tablename__ = 'consumer_orders'

    id = Column(Integer, primary_key=True)
    consumer_id = Column(Integer, ForeignKey('consumers.id'))
    order_date = Column(Date)
    total_amount = Column(Float)

    consumer = relationship("Consumer", back_populates="orders")
    items = relationship("ConsumerOrderItem", back_populates="order", cascade="all, delete", single_parent=True)


class ConsumerOrderItem(Base):
    __tablename__ = 'consumer_order_items'

    id = Column(Integer, primary_key=True)
    consumer_order_id = Column(Integer, ForeignKey('consumer_orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    item_name = Column(String)
    quantity = Column(Integer)
    unit_price = Column(Float)
    total_price = Column(Float)

    product = relationship("Product", back_populates="consumer_order_items")
    order = relationship("ConsumerOrder", back_populates="items")

    def calculate_total_price(self):
        if self.product:
            self.total_price = self.quantity * self.product.unit_price


class Consumer(Base):
    __tablename__ = 'consumers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    contact_number = Column(String)
    orders = relationship("ConsumerOrder", back_populates="consumer", cascade="all, delete", single_parent=True)

class ConsumerMembership(Base):
    __tablename__ = 'consumer_memberships'

    id = Column(Integer, primary_key=True)
    consumer_id = Column(Integer, ForeignKey('consumers.id'))
    start_date = Column(Date)
    end_date = Column(Date)

    consumer = relationship("Consumer", backref="memberships")



if __name__ == '__main__':
    Base.metadata.create_all(engine)
