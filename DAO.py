from typing import Optional,List
from sqlalchemy.orm import joinedload
from models import *
import re
from datetime import date, timedelta

class SupplierDao:
    
    @staticmethod
    def create_supplier(name, address, contact, contact_number, email, category_id):
        supplier = Supplier(
            SupplierName=name,
            Address=address,
            ContactPerson=contact,
            ContactNumber=contact_number,
            Email=email,
            CategoryID=category_id
        )
        db.session.add(supplier)
        db.session.commit()
        return supplier
    
    @staticmethod
    def get_suppliers_by_name(supplier_name: str) -> List[Supplier]:
        suppliers = Supplier.query.filter_by(Supplier.SupplierName == supplier_name).all()
        return suppliers
    @staticmethod
    def get_supplier_by_id(supplier_id):
        supplier = Supplier.query.filter_by(SupplierID=supplier_id).first()
        if supplier:
            category = CategoryDao.get_category_by_id(supplier.category_id)
            if category:
                supplier.category_name = category.CategoryName
        return supplier

    @staticmethod
    def get_all_suppliers():
        suppliers = Supplier.query.all()
        for supplier in suppliers:
            category = CategoryDao.get_category_by_id(supplier.category_id)
            if category:
                supplier.category_name = category.CategoryName
        return suppliers

    @staticmethod
    def update_supplier(supplier_id, supplier_name, contact_person, contact_number, email, address):
        supplier = SupplierDao.get_supplier_by_id(supplier_id)
        supplier.SupplierName = supplier_name
        supplier.ContactPerson = contact_person
        supplier.ContactNumber = contact_number
        supplier.Email = email
        supplier.Address = address
        db.session.commit()
        return supplier

    @staticmethod
    def delete_supplier(supplier_id):
        supplier = SupplierDao.get_supplier_by_id(supplier_id)
        db.session.delete(supplier)
        db.session.commit()

    @staticmethod
    def is_valid_email(email):
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(email_regex, email)

    @staticmethod
    def is_valid_contact_number(contact_number):
        contact_number_regex = r"^\d{10}$"
        return re.match(contact_number_regex, contact_number)
    
class CategoryDao:
    @staticmethod
    def create_category(category_name):
        category = Category(CategoryName=category_name)
        db.session.add(category)
        db.session.commit()
        return category

    @staticmethod
    def get_category_by_id(category_id):
        category = Category.query.filter_by(CategoryID=category_id).first()
        return category

    @staticmethod
    def get_all_categories():
        categories = Category.query.all()
        return categories

    @staticmethod
    def update_category(category_id, category_name):
        category = CategoryDao.get_category_by_id(category_id)
        category.CategoryName = category_name
        db.session.commit()
        return category

    @staticmethod
    def delete_category(category_id):
        category = CategoryDao.get_category_by_id(category_id)
        db.session.delete(category)
        db.session.commit()

    @staticmethod
    def get_category_by_id(category_id: int) -> Optional[Category]:
        return Category.query.filter_by(CategoryID=category_id).first()

    @staticmethod
    def get_category_name_by_id(category_id: int) -> Optional[str]:
        category = CategoryDao.get_category_by_id(category_id)
        if category:
            return category.CategoryName 
        return None
    
    @staticmethod
    def get_products_and_suppliers_by_category(category_id: int):
        products_and_suppliers = db.session.query(Product, Supplier).\
            join(Supplier, Product.CategoryID == Supplier.CategoryID).\
            filter(Product.CategoryID == category_id).all()

        return products_and_suppliers



# ==============================================



class ProductDao:
    @staticmethod
    def create_product(
        name: str,
        description: str,
        category_id: int,
        unit_price: float,
        units_in_stock: int,
        units_on_order: int,
        reorder_level: int,
        discontinued: bool
    ) -> Product:
        try:
            product = Product(
                ProductName=name,
                ProductDescription=description,
                CategoryID=category_id,
                UnitPrice=unit_price,
                UnitsInStock=units_in_stock,
                UnitsOnOrder=units_on_order,
                ReorderLevel=reorder_level,
                Discontinued=discontinued
            )
            db.session.add(product)
            db.session.commit()
            return product
        except Exception as e:
            print("An error occurred while creating the product:", str(e))
            db.session.rollback()
            return None

    @staticmethod
    def get_product_by_id(product_id: int) -> Product:
        return Product.query.filter_by(ProductID=product_id).first()

    @staticmethod
    def get_all_products():
        return Product.query.all()

    @staticmethod
    def update_product(
        product_id: int,
        name: str = None,
        description: str = None,
        category_id: int = None,
        unit_price: float = None,
        units_in_stock: int = None,
        units_on_order: int = None,
        reorder_level: int = None,
        discontinued: bool = None
    ) -> Product:
        product = ProductDao.get_product_by_id(product_id)
        if not product:
            return None

        if name is not None:
            product.ProductName = name
        if description is not None:
            product.ProductDescription = description
        if category_id is not None:
            product.CategoryID = category_id
        if unit_price is not None:
            product.UnitPrice = unit_price
        if units_in_stock is not None:
            product.UnitsInStock = units_in_stock
        if units_on_order is not None:
            product.UnitsOnOrder = units_on_order
        if reorder_level is not None:
            product.ReorderLevel = reorder_level
        if discontinued is not None:
            product.Discontinued = discontinued

        db.session.commit()

        return product

    @staticmethod
    def delete_product(product_id: int) -> bool:
        product = ProductDao.get_product_by_id(product_id)
        if not product:
            return False

        db.session.delete(product)
        db.session.commit()

        return True

class MembershipDAO:
    @staticmethod
    def get_membership_by_id(membership_id):
        return Membership.query.get(membership_id)

    @staticmethod
    def get_all_memberships():
        return Membership.query.all()
    

class SupplierOrderDAO:

        @staticmethod
        def get_supplier_order(order_id):
            return SupplierOrder.query.get(order_id)

        @staticmethod
        def get_all_supplier_orders():
            return SupplierOrder.query.all()
        
        @staticmethod
        def get_supplier_order_by_id(order_id: int) -> Optional[SupplierOrder]:
            supplier_order = SupplierOrder.query.get(order_id)
            return supplier_order

        @staticmethod
        def get_supplier_name_by_order_id(order_id: int) -> Optional[str]:
            supplier_order = SupplierOrder.query.options(joinedload(SupplierOrder.supplier)).get(order_id)
            if supplier_order and supplier_order.supplier:
                return supplier_order.supplier.SupplierName
            return None

        @staticmethod
        def get_product_name_by_order_id(order_id: int) -> Optional[str]:
            supplier_order = SupplierOrder.query.options(joinedload(SupplierOrder.product)).get(order_id)
            if supplier_order and supplier_order.product:
                return supplier_order.product.ProductName
            return None

        @staticmethod
        def create_supplier_order(supplier_id, quantity, product_id):
            # Get today's date
            order_date = date.today()

            # Calculate the expected delivery date as order date plus 5 days
            expected_delivery_date = order_date + timedelta(days=5)

            # Create a new SupplierOrder object
            new_order = SupplierOrder(
                SupplierID=supplier_id,
                OrderDate=order_date,
                ExpectedDeliveryDate=expected_delivery_date,
                TotalAmount=0.0,  # TotalAmount will be calculated based on quantity and product unit price
                Quantity=quantity,
                ProductID=product_id
            )

            # Increment UnitsInStock for the product
            product = Product.query.get(product_id)
            product.UnitsInStock += quantity

            # Calculate the total amount based on quantity and product unit price
            new_order.TotalAmount = product.UnitPrice * quantity

            # Create the inbound bill for this order
            inbound_bill = InboundBill(
                SupplierOrderID=new_order.OrderID,
                BillDate=new_order.OrderDate,
                DueDate=new_order.ExpectedDeliveryDate + timedelta(days=5),  # Example: Due date is set to 5 days from the expected delivery date
                AmountDue=new_order.TotalAmount,
                AmountPaid=0.0,  # Initially set to 0.0, as no payment is made yet
                PaymentStatus="Pending"  # Initially set to "Pending"
            )

            # Set the relationship between the supplier order and inbound bill
            new_order.inbound_bills.append(inbound_bill)

            # Add the new order and inbound bill to the database session and commit the transaction
            db.session.add(new_order)
            db.session.commit()

            # Return the newly created supplier order object
            return new_order

            
        @staticmethod
        def update_supplier_order(order_id, quantity):
            order = SupplierOrder.query.get(order_id)
            order.Quantity = quantity

            # Update UnitsInStock for the product
            product = Product.query.get(order.ProductID)
            product.UnitsInStock -= order.Quantity  # Decrement previous quantity
            product.UnitsInStock += quantity  # Increment new quantity

            db.session.commit()

            return order

        @staticmethod
        def delete_supplier_order(order_id):
            order = SupplierOrder.query.get(order_id)
            product = Product.query.get(order.ProductID)

            # Decrement UnitsInStock for the product
            product.UnitsInStock -= order.Quantity

            db.session.delete(order)
            db.session.commit()

            return True
        
class InboundBillDAO:

    @staticmethod
    def get_inbound_bill(inbound_bill_id: int) -> Optional[InboundBill]:
        return InboundBill.query.get(inbound_bill_id)

    @staticmethod
    def get_all_inbound_bills() -> List[InboundBill]:
        return InboundBill.query.all()

    @staticmethod
    def update_inbound_bill_amount_paid(inbound_bill_id, amount_paid):
        # Retrieve the inbound bill from the database
        inbound_bill = InboundBill.query.get(inbound_bill_id)

        # Update the amount paid
        inbound_bill.AmountPaid = amount_paid

        # Decrement the amount due by the amount paid
        inbound_bill.AmountDue -= amount_paid

        # Check if the amount due is zero
        if inbound_bill.AmountDue == 0:
            # Set the payment status to "Success"
            inbound_bill.PaymentStatus = "Success"

        # Commit the changes to the database
        db.session.commit()

        # Return the updated inbound bill
        return inbound_bill
    
class CustomerDao:
    @staticmethod
    def create_customer(name, address, contact_person, contact_number, email, membership_id):
        customer = Customer(
            CustomerName=name,
            Address=address,
            ContactPerson=contact_person,
            ContactNumber=contact_number,
            Email=email,
            membership_id=membership_id
        )
        db.session.add(customer)
        db.session.commit()
        return customer

    @staticmethod
    def get_customers_by_name(customer_name: str) -> List[Customer]:
        customers = Customer.query.filter(Customer.CustomerName == customer_name).all()
        return customers

    @staticmethod
    def get_customer_by_id(customer_id):
        customer = Customer.query.filter_by(CustomerID=customer_id).first()
        if customer:
            membership = MembershipDAO.get_membership_by_id(customer.membership_id)
            if membership:
                customer.membership_type = membership.membership_type
        return customer
    
    @staticmethod
    def get_customers_by_email(email: str) -> List[Customer]:
        return db.session.query(Customer).filter(Customer.Email == email).all()

    @staticmethod
    def get_all_customers():
        customers = Customer.query.all()
        for customer in customers:
            membership = MembershipDAO.get_membership_by_id(customer.membership_id)
            if membership:
                customer.membership_type = membership.membership_type
        return customers

    @staticmethod
    def update_customer(customer_id, customer_name, contact_person, contact_number, email, address):
        customer = CustomerDao.get_customer_by_id(customer_id)
        customer.CustomerName = customer_name
        customer.ContactPerson = contact_person
        customer.ContactNumber = contact_number
        customer.Email = email
        customer.Address = address
        db.session.commit()
        return customer

    @staticmethod
    def delete_customer(customer_id):
        customer = CustomerDao.get_customer_by_id(customer_id)
        db.session.delete(customer)
        db.session.commit()

    @staticmethod
    def is_valid_email(email):
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(email_regex, email)

    @staticmethod
    def is_valid_contact_number(contact_number):
        contact_number_regex = r"^\d{10}$"
        return re.match(contact_number_regex, contact_number)

    
class CustomerOrderDAO:
    @staticmethod
    def create_customer_order(customer_id, quantity, product_id):
        # Get today's date
        order_date = date.today()

        # Calculate the total amount based on the quantity and product unit price
        product = Product.query.get(product_id)
        total_amount = quantity * product.UnitPrice

        # Create the customer order
        new_order = CustomerOrder(
            customer_id=customer_id,
            OrderDate=order_date,
            ShippingAddress='',
            Quantity=quantity,
            TotalAmount=total_amount,
            Discount=0.0,
            ProductID=product_id
        )

        # Add the new order to the database
        db.session.add(new_order)
        db.session.commit()

        return new_order

    @staticmethod
    def update_customer_order(order_id, customer_id, quantity, product_id):
        # Retrieve the existing customer order
        order = CustomerOrder.query.get(order_id)

        # Update the customer order with the new values
        order.customer_id = customer_id
        order.quantity = quantity
        order.product_id = product_id

        # Calculate the new total amount based on the updated quantity and product unit price
        product = Product.query.get(product_id)
        order.total_amount = quantity * product.UnitPrice

        # Commit the changes to the database
        db.session.commit()

        return order

    @staticmethod
    def delete_customer_order(order_id):
        # Retrieve the customer order to be deleted
        order = CustomerOrder.query.get(order_id)

        # Delete the customer order from the database
        db.session.delete(order)
        db.session.commit()

        return True

    @staticmethod
    def get_customer_order_by_id(order_id):
        return CustomerOrder.query.get(order_id)

    @staticmethod
    def update_customer_order(order_id, shipping_address, quantity):
        order = CustomerOrder.query.get(order_id)
        if order:
            # Update the order details
            order.ShippingAddress = shipping_address
            order.Quantity = quantity
            db.session.commit()
            return order
        return None

    @staticmethod
    def delete_customer_order(order_id):
        order = CustomerOrder.query.get(order_id)
        if order:
            # Delete the order
            db.session.delete(order)
            db.session.commit()
            return True
        return False

    @staticmethod
    def get_all_customer_orders():
        return CustomerOrder.query.all()
    

class OutboundBillDAO:
    @staticmethod
    def create_outbound_bill(customer_order_id, bill_date, amount_paid, payment_status):
        outbound_bill = OutboundBill(
            CustomerOrderID=customer_order_id,
            BillDate=bill_date,
            DueDate=bill_date + timedelta(days=2),
            Discount=0.0,
            AmountPaid=amount_paid,
            PaymentStatus=payment_status
        )

        db.session.add(outbound_bill)
        db.session.commit()

        return outbound_bill

    @staticmethod
    def get_outbound_bill_by_id(outbound_bill_id):
        return OutboundBill.query.get(outbound_bill_id)

    @staticmethod
    def update_outbound_bill(outbound_bill_id, amount_paid, payment_status):
        outbound_bill = OutboundBill.query.get(outbound_bill_id)

        if outbound_bill:
            outbound_bill.AmountPaid = amount_paid
            outbound_bill.PaymentStatus = payment_status

            db.session.commit()

        return outbound_bill

    @staticmethod
    def delete_outbound_bill(outbound_bill_id):
        outbound_bill = OutboundBill.query.get(outbound_bill_id)

        if outbound_bill:
            db.session.delete(outbound_bill)
            db.session.commit()
            return True

        return False
    
    @staticmethod
    def get_outbound_bills_by_customer_order_id(customer_order_id):
        return OutboundBill.query.filter_by(CustomerOrderID=customer_order_id).all()