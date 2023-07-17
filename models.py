from sqlalchemy import Column, Integer, String, Float, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship,backref
from datetime import timedelta
from database import db



class Supplier(db.Model):
    __tablename__ = 'suppliers'

    SupplierID = Column(Integer, primary_key=True)
    SupplierName = Column(String(100), nullable=False)
    ContactPerson = Column(String(100), nullable=True)
    ContactNumber = Column(String(20), nullable=True)
    Email = Column(String(100), nullable=True)
    Address = Column(String(200), nullable=True)
    CategoryID = Column(Integer, ForeignKey('categories.CategoryID'), nullable=False)

    category = relationship("Category", back_populates="suppliers")
    supplier_orders = relationship("SupplierOrder", back_populates="supplier")
    # inbound_bills = relationship("InboundBill", back_populates="supplier", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Supplier(SupplierID={self.SupplierID}, SupplierName='{self.SupplierName}', ContactPerson='{self.ContactPerson}', ContactNumber='{self.ContactNumber}', Email='{self.Email}', Address='{self.Address}')>"


class Category(db.Model):
    __tablename__ = 'categories'

    CategoryID = Column(Integer, primary_key=True)
    CategoryName = Column(String(100), nullable=False)

    suppliers = relationship("Supplier", back_populates="category")
    products = relationship("Product", back_populates="category")

    def __repr__(self):
        return f"<Category(CategoryID={self.CategoryID}, CategoryName='{self.CategoryName}')>"


class Product(db.Model):
    __tablename__ = 'products'

    ProductID = Column(Integer, primary_key=True)
    ProductName = Column(String(100), nullable=False)
    ProductDescription = Column(String(500), nullable=False)
    CategoryID = Column(Integer, ForeignKey('categories.CategoryID'), nullable=False)
    UnitPrice = Column(Float, nullable=False)
    UnitsInStock = Column(Integer, nullable=False)
    UnitsOnOrder = Column(Integer, nullable=False)
    ReorderLevel = Column(Integer, nullable=False)
    Discontinued = Column(Boolean, nullable=False)

    category = relationship("Category", back_populates="products")

    def __repr__(self):
        return f"<Product(ProductID={self.ProductID}, ProductName='{self.ProductName}', CategoryID={self.CategoryID}, UnitPrice={self.UnitPrice}, UnitsInStock={self.UnitsInStock}, UnitsOnOrder={self.UnitsOnOrder}, ReorderLevel={self.ReorderLevel}, Discontinued={self.Discontinued})>"


class Membership(db.Model):
    __tablename__ = 'membership'

    membership_id = Column(Integer, primary_key=True)
    membership_type = Column(String, nullable=False, default='classic')
    customer = relationship("Customer", back_populates="membership")

    def __repr__(self):
        return f"<Membership(membership_id={self.membership_id}, membership_type='{self.membership_type}')>"


class Customer(db.Model):
    __tablename__ = 'customers'

    CustomerID = Column(Integer, primary_key=True)
    CustomerName = Column(String(100), nullable=False)
    ContactPerson = Column(String(100), nullable=True)
    ContactNumber = Column(String(20), nullable=False)
    Email = Column(String(100), nullable=False)
    Address = Column(String(200), nullable=False)
    membership_id = Column(Integer, ForeignKey('membership.membership_id'), nullable=True)

    membership = relationship("Membership")
    customer_orders = relationship("CustomerOrder", back_populates="customer", cascade="all, delete-orphan")

    def __repr__(self):
         return f"<Customer(CustomerID={self.CustomerID}, CustomerName='{self.CustomerName}', ContactPerson='{self.ContactPerson}', ContactNumber='{self.ContactNumber}', Email='{self.Email}', Address='{self.Address}', membership_id='{self.membership_id}')>"



class SupplierOrder(db.Model):
    __tablename__ = 'supplier_orders'

    OrderID = Column(Integer, primary_key=True)
    SupplierID = Column(Integer, ForeignKey('suppliers.SupplierID', ondelete="CASCADE"), nullable=False)
    OrderDate = Column(Date, nullable=False)
    ExpectedDeliveryDate = Column(Date, nullable=False)
    TotalAmount = Column(Float, nullable=False)
    Quantity = Column(Integer, nullable=False)
    ProductID = Column(Integer, ForeignKey('products.ProductID'), nullable=False)

    supplier = relationship("Supplier", back_populates="supplier_orders", single_parent=True, cascade="all, delete")
    inbound_bills = relationship("InboundBill", back_populates="supplier_order")
    product = relationship("Product")

    def __repr__(self):
        return f"<SupplierOrder(OrderID={self.OrderID}, SupplierID={self.SupplierID}, OrderDate='{self.OrderDate}', ExpectedDeliveryDate='{self.ExpectedDeliveryDate}', TotalAmount={self.TotalAmount}, Quantity={self.Quantity})>"

# class SupplierOrderedItems(db.Model):
#     __tablename__ = 'supplier_ordered_items'

#     ItemID = Column(Integer, primary_key=True)
#     OrderID = Column(Integer, ForeignKey('supplier_orders.OrderID'), nullable=False)
#     ProductID = Column(Integer, ForeignKey('products.ProductID'), nullable=False)
#     Quantity = Column(Integer, nullable=False)

#     order = relationship("SupplierOrder", back_populates="ordered_items")
#     product = relationship("Product")

#     def __repr__(self):
#         return f"<SupplierOrderedItems(ItemID={self.ItemID}, OrderID={self.OrderID}, ProductID={self.ProductID}, Quantity={self.Quantity})>"
    

class CustomerOrder(db.Model):
    __tablename__ = 'customer_orders'

    OrderID = Column(Integer, primary_key=True)
    CustomerID = Column(Integer, ForeignKey('customers.CustomerID'), nullable=False)
    OrderDate = Column(Date, nullable=False)
    ShippingAddress = Column(String(200), nullable=False)
    Quantity = Column(Integer, nullable=False)
    TotalAmount = Column(Float, nullable=False)
    Discount = Column(Float, nullable=False, default=0.0)
    ProductID = Column(Integer, ForeignKey('products.ProductID'), nullable=False)

    customer = relationship("Customer", back_populates="customer_orders", cascade="all, delete-orphan", single_parent=True)
    outbound_bills = relationship("OutboundBill", back_populates="customer_order")
    product = relationship("Product")

    def calculate_discount(self):
        membership_type = self.customer.membership.membership_type
        if membership_type == 'premium':
            return self.TotalAmount * 0.25  # 25% discount for premium members
        elif membership_type == 'classic':
            return self.TotalAmount * 0.05  # 5% discount for classic members
        else:
            return self.TotalAmount

    def calculate_total_amount(self):
        discount = self.calculate_discount()
        self.Discount = discount
        self.TotalAmount -= discount

    def __repr__(self):
        return f"<CustomerOrder(OrderID={self.OrderID}, CustomerID={self.CustomerID}, OrderDate='{self.OrderDate}', ShippingAddress='{self.ShippingAddress}', Quantity={self.Quantity}, TotalAmount={self.TotalAmount}, Discount={self.Discount})>"

# class ConsumerOrderedItems(db.Model):
#     __tablename__ = 'consumer_ordered_items'

#     ItemID = Column(Integer, primary_key=True)
#     OrderID = Column(Integer, ForeignKey('customer_orders.OrderID'), nullable=False)
#     ProductID = Column(Integer, ForeignKey('products.ProductID'), nullable=False)
#     Quantity = Column(Integer, nullable=False)

#     order = relationship("CustomerOrder", back_populates="ordered_items")
#     product = relationship("Product")

#     def __repr__(self):
#         return f"<ConsumerOrderedItems(ItemID={self.ItemID}, OrderID={self.OrderID}, ProductID={self.ProductID}, Quantity={self.Quantity})>"

class InboundBill(db.Model):
    __tablename__ = 'inbound_bills'

    InboundBillID = Column(Integer, primary_key=True)
    SupplierOrderID = Column(Integer, ForeignKey('supplier_orders.OrderID'), nullable=False)
    BillDate = Column(Date, nullable=False)
    DueDate = Column(Date, nullable=False)
    AmountDue = Column(Float, nullable=False)
    AmountPaid = Column(Float, nullable=False)
    PaymentStatus = Column(String(20), nullable=False)

    supplier_order = relationship("SupplierOrder", back_populates="inbound_bills", cascade="all, delete-orphan", single_parent=True)

    def __init__(self, SupplierOrderID, BillDate, DueDate, AmountDue, AmountPaid, PaymentStatus):
        self.SupplierOrderID = SupplierOrderID
        self.BillDate = BillDate
        self.DueDate = DueDate
        self.AmountDue = AmountDue
        self.AmountPaid = AmountPaid
        self.PaymentStatus = PaymentStatus

    def calculate_amount_due(self):
        self.AmountDue = self.supplier_order.TotalAmount - self.AmountPaid

class OutboundBill(db.Model):
    __tablename__ = 'outbound_bills'

    OutboundBillID = Column(Integer, primary_key=True)
    CustomerOrderID = Column(Integer, ForeignKey('customer_orders.OrderID'), nullable=False)
    BillDate = Column(Date, nullable=False)
    DueDate = Column(Date, nullable=False)
    Discount = Column(Float, nullable=False)
    AmountPaid = Column(Float, nullable=False)
    PaymentStatus = Column(String(20), nullable=False)

    customer_order = relationship("CustomerOrder", back_populates="outbound_bills")

    def __init__(self, CustomerOrderID, BillDate, AmountPaid, PaymentStatus):
        self.CustomerOrderID = CustomerOrderID
        self.BillDate = BillDate
        self.DueDate = BillDate + timedelta(days=2)  # Example: Due date is set to 2 days from the bill date
        self.Discount = 0.0  # Default discount is initially set to 0.0
        self.AmountPaid = AmountPaid
        self.PaymentStatus = PaymentStatus

    def __repr__(self):
        return f"<OutboundBill(OutboundBillID={self.OutboundBillID}, CustomerOrderID={self.CustomerOrderID}, BillDate='{self.BillDate}', DueDate='{self.DueDate}', Discount={self.Discount}, AmountPaid={self.AmountPaid}, PaymentStatus='{self.PaymentStatus}')>"
