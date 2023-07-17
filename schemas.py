

import strawberry
from typing import List, Optional
from models import Supplier, Category, Membership, Customer

from datetime import date, timedelta
from DAO import *

@strawberry.type
class SupplierType:
    supplier_id: int
    name: str
    address: str
    contact: str
    contact_number: str
    email: str
    category_id: Optional[int]
    category_name: Optional[str]

@strawberry.type
class CategoryType:
    category_id: int
    category_name: str
    # def Products(self) -> List[Product]:
    #     return ProductDao.get_product_by_id(self.id)
    
@strawberry.type
class SupplierOrderedItemsType:
    item_id: int
    order_id: int
    product_id: int
    quantity: int


@strawberry.type
class Membership:
    membership_id: int
    membership_type: str

@strawberry.type
class Product:
    product_id: int
    name: str
    description: str
    category_id: int
    category_name: Optional[str]
    unit_price: float
    units_in_stock: int
    units_on_order: int
    reorder_level: int
    discontinued: bool


    # @strawberry.field
    # def category(self) -> Optional[str]:
    #     if self.category_id:
    #         category = CategoryDao.get_category_by_id(self.category_id)
    #         return category.CategoryName if category else None
    #     return None

@strawberry.input
class SupplierOrderInput:
    supplier_id: int
    quantity: int
    product_id: int


@strawberry.type
class SupplierOrder:
    OrderID: int
    SupplierID: int
    OrderDate: date
    ExpectedDeliveryDate: date
    TotalAmount: float
    Quantity: int
    ProductID: int

@strawberry.input
class UpdateInboundBillInput:
    inbound_bill_id: int
    amount_paid: float

@strawberry.type
class InboundBill:
    InboundBillID: int
    SupplierOrderID: int
    BillDate: date
    DueDate: date
    AmountDue: float
    AmountPaid: float
    PaymentStatus: str

@strawberry.type
class CustomerType:
    customer_id: int
    name: str
    address: str
    contact: Optional[str]
    contact_number: str
    email: str
    membership_id: Optional[int]
    membership_type: Optional[str]

@strawberry.type
class CustomerOrder:
    order_id: int
    customer_id: int
    order_date: date
    shipping_address: str
    quantity: int
    total_amount: float
    discount: float
    product_id: int
@strawberry.input
class CustomerOrderInput:
    customer_id: int
    shipping_address: str
    quantity: int
    product_id: int


@strawberry.type
class OutboundBill:
    outbound_bill_id: int
    customer_order_id: int
    bill_date: date
    due_date: date
    discount: float
    amount_paid: float
    payment_status: str



@strawberry.type
class Query:
    @strawberry.field
    def get_supplier_by_id(self, supplier_id: int) -> Optional[SupplierType]:
        supplier = SupplierDao.get_supplier_by_id(supplier_id)
        if supplier:
            category = CategoryDao.get_category_by_id(supplier.CategoryID)
            category_name = category.CategoryName if category else None
            return SupplierType(
                supplier_id=supplier.SupplierID,
                name=supplier.SupplierName,
                address=supplier.Address,
                contact=supplier.ContactPerson,
                contact_number=supplier.ContactNumber,
                email=supplier.Email,
                category_id=supplier.CategoryID,
                category_name=category_name
            )
        return None

    @strawberry.field
    def get_all_suppliers(self) -> List[SupplierType]:
        suppliers = SupplierDao.get_all_suppliers()
        supplier_types = []
        for supplier in suppliers:
            category = CategoryDao.get_category_by_id(supplier.CategoryID)
            category_name = category.CategoryName if category else None
            supplier_types.append(
                SupplierType(
                    supplier_id=supplier.SupplierID,
                    name=supplier.SupplierName,
                    address=supplier.Address,
                    contact=supplier.ContactPerson,
                    contact_number=supplier.ContactNumber,
                    email=supplier.Email,
                    category_id=supplier.CategoryID,
                    category_name=category_name
                )
            )
        return supplier_types
    
    @strawberry.field
    def get_suppliers_by_name(self, supplier_name: str) -> List[SupplierType]:
        suppliers = SupplierDao.get_suppliers_by_name(supplier_name)
        supplier_types = []
        for supplier in suppliers:
            supplier_type = SupplierType(
                supplier_id=supplier.SupplierID,
                supplier_name=supplier.SupplierName,
                contact_number=supplier.ContactNumber,
                email=supplier.Email
            )
            supplier_types.append(supplier_type)
        return supplier_types
    
    @strawberry.field
    def get_category(self, category_id: int) -> Optional[CategoryType]:
        category = CategoryDao.get_category_by_id(category_id)
        if category:
            return CategoryType(
                category_id=category.CategoryID,
                category_name=category.CategoryName
            )
        return None

    @strawberry.field
    def get_all_categories(self) -> List[CategoryType]:
        categories = CategoryDao.get_all_categories()
        return [
            CategoryType(
                category_id=category.CategoryID,
                category_name=category.CategoryName
            )
            for category in categories
        ]
    
    @strawberry.field
    def get_product_by_id(product_id: int) -> Optional[Product]:
        product = ProductDao.get_product_by_id(product_id)
        if product:
            category = CategoryDao.get_category_by_id(product.CategoryID)
            category_name = category.category_name if category and hasattr(category, 'category_name') else None
            return Product(
                    product_id=product.ProductID,
                    name=product.ProductName,
                    description=product.ProductDescription,
                    category_id=product.CategoryID,
                    category_name=category_name,
                    unit_price=product.UnitPrice,
                    units_in_stock=product.UnitsInStock,
                    units_on_order=product.UnitsOnOrder,
                    reorder_level=product.ReorderLevel,
                    discontinued=product.Discontinued
            )
        return None

    @strawberry.field
    def get_all_products() -> List[Product]:
        products = ProductDao.get_all_products()
        result = []
        for product in products:
            category = CategoryDao.get_category_by_id(product.CategoryID)
            category_name = category.category_name if category and hasattr(category, 'category_name') else None
            result.append(
                Product(
                    product_id=product.ProductID,
                    name=product.ProductName,
                    description=product.ProductDescription,
                    category_id=product.CategoryID,
                    category_name=category_name,
                    unit_price=product.UnitPrice,
                    units_in_stock=product.UnitsInStock,
                    units_on_order=product.UnitsOnOrder,
                    reorder_level=product.ReorderLevel,
                    discontinued=product.Discontinued
                )
            )
        return result
    
    @strawberry.field
    def get_membership_by_id(self, membership_id: int) -> Membership:
        return MembershipDAO.get_membership_by_id(membership_id)

    @strawberry.field
    def get_all_memberships(self) -> List[Membership]:
        return MembershipDAO.get_all_memberships()

    @strawberry.field
    def get_supplier_order(self, order_id: int) -> Optional[SupplierOrder]:
        supplier_order = SupplierOrderDAO.get_supplier_order(order_id)
        return supplier_order
    @strawberry.field
    def get_supplier_order(self, order_id: int) -> SupplierOrder:
        # Get the supplier order from the DAO
        supplier_order = SupplierOrderDAO.get_supplier_order(order_id)
        return supplier_order

    @strawberry.field
    def get_all_supplier_orders(self) -> List[SupplierOrder]:
        # Get all supplier orders from the DAO
        supplier_orders = SupplierOrderDAO.get_all_supplier_orders()
        return supplier_orders

    @strawberry.field
    def get_supplier_name_by_order_id(order_id: int) -> Optional[str]:
        supplier_order = SupplierOrder.query.get(order_id)
        if supplier_order and supplier_order.supplier_id:
            supplier = Supplier.query.get(supplier_order.supplier_id)
            if supplier:
                return supplier.SupplierName
        return None

    @strawberry.field
    def get_product_name_by_order_id(order_id: int) -> Optional[str]:
        supplier_order = SupplierOrder.query.get(order_id)
        if supplier_order and supplier_order.product_id:
            product = Product.query.get(supplier_order.product_id)
            if product:
                return product.ProductName
        return None

    @strawberry.field
    def get_inbound_bill(self, inbound_bill_id: int) -> InboundBill:
        return InboundBillDAO.get_inbound_bill(inbound_bill_id)

    @strawberry.field
    def get_all_inbound_bills(self) -> List[InboundBill]:
        return InboundBillDAO.get_all_inbound_bills()
    
    @strawberry.field
    def get_customer_by_id(self, customer_id: int) -> Optional[CustomerType]:
        customer = CustomerDao.get_customer_by_id(customer_id)
        if customer:
            return CustomerType(
                customer_id=customer.CustomerID,
                name=customer.CustomerName,
                address=customer.Address,
                contact=customer.ContactPerson,
                contact_number=customer.ContactNumber,
                email=customer.Email,
                membership_id=customer.membership_id,
                membership_type=customer.membership.membership_type if customer.membership else None
            )
        return None

    @strawberry.field
    def get_all_customers(self) -> List[CustomerType]:
        customers = CustomerDao.get_all_customers()
        return [
            CustomerType(
                customer_id=customer.CustomerID,
                name=customer.CustomerName,
                address=customer.Address,
                contact=customer.ContactPerson,
                contact_number=customer.ContactNumber,
                email=customer.Email,
                membership_id=customer.membership_id,
                membership_type=customer.membership.membership_type if customer.membership else None
            )
            for customer in customers
        ]

    def get_customer_order_by_id(order_id: int) -> Optional[CustomerOrder]:
        return CustomerOrderDAO.get_customer_order_by_id(order_id)

    @strawberry.field
    def get_all_customer_orders() -> List[CustomerOrder]:
        return CustomerOrderDAO.get_all_customer_orders()

    @strawberry.field
    def get_outbound_bill_by_id(bill_id: int) -> Optional[OutboundBill]:
        return OutboundBillDAO.get_outbound_bill_by_id(bill_id)

    @strawberry.field
    def get_outbound_bills_by_customer_order_id(customer_order_id: int) -> List[OutboundBill]:
        return OutboundBillDAO.get_outbound_bills_by_customer_order_id(customer_order_id)



@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_supplier(
        self,
        name: str,
        address: str,
        contact: str,
        contact_number: str,
        email: str,
        category_id: Optional[int] = None
    ) -> Optional[SupplierType]:
        category = CategoryDao.get_category_by_id(category_id)
        if not category:
            return None

        supplier = SupplierDao.create_supplier(name, address, contact, contact_number, email, category.CategoryID)
        return SupplierType(
            supplier_id=supplier.SupplierID,
            name=supplier.SupplierName,
            address=supplier.Address,
            contact=supplier.ContactPerson,
            contact_number=supplier.ContactNumber,
            email=supplier.Email,
            category_id=supplier.CategoryID,
            category_name=category.CategoryName
        )

    @strawberry.mutation
    def update_supplier(
        self,
        supplier_id: int,
        name: Optional[str] = None,
        address: Optional[str] = None,
        contact: Optional[str] = None,
        contact_number: Optional[str] = None,
        email: Optional[str] = None,
        category_id: Optional[int] = None,
    ) -> Optional[SupplierType]:
        supplier = SupplierDao.get_supplier_by_id(supplier_id)
        if supplier:
            if name:
                supplier.SupplierName = name
            if address:
                supplier.Address = address
            if contact:
                supplier.ContactPerson = contact
            if contact_number:
                supplier.ContactNumber = contact_number
            if email:
                supplier.Email = email
            if category_id:
                supplier.CategoryID = category_id

            # Update the supplier in the database
            SupplierDao.update_supplier(supplier)

            # Retrieve the updated supplier with the associated category
            updated_supplier = SupplierDao.get_supplier_by_id(supplier_id)
            category = CategoryDao.get_category_by_id(updated_supplier.CategoryID)
            category_name = category.CategoryName if category else None

            return SupplierType(
                supplier_id=updated_supplier.SupplierID,
                name=updated_supplier.SupplierName,
                address=updated_supplier.Address,
                contact=updated_supplier.ContactPerson,
                contact_number=updated_supplier.ContactNumber,
                email=updated_supplier.Email,
                category_id=updated_supplier.CategoryID,
                category_name=category_name,
            )

        return None

    @strawberry.mutation
    def delete_supplier(self, supplier_id: int) -> bool:
        supplier = SupplierDao.get_supplier_by_id(supplier_id)
        if supplier:
            SupplierDao.delete_supplier(supplier)
            return True

        return False
# ==================================================================================================================================================

    @strawberry.mutation
    def create_category(category_name: str) -> CategoryType:
        category = CategoryDao.create_category(category_name)
        return CategoryType(
            category_id=category.CategoryID,
            category_name=category.CategoryName
        )

    @strawberry.mutation
    def update_category(category_id: int, category_name: str) -> Optional[CategoryType]:
        category = CategoryDao.update_category(category_id, category_name)
        if category:
            return CategoryType(
                category_id=category.CategoryID,
                category_name=category.CategoryName
            )
        return None

    @strawberry.mutation
    def delete_category(category_id: int) -> bool:
        return CategoryDao.delete_category(category_id)

    
# ================================================================================category=======================================================
    @strawberry.mutation
    def create_product(
        self,
        name: str,
        description: str,
        category_id: int,
        unit_price: float,
        units_in_stock: int,
        units_on_order: int,
        reorder_level: int,
        discontinued: bool
    ) -> Optional[Product]:
        product = ProductDao.create_product(
            name,
            description,
            category_id,
            unit_price,
            units_in_stock,
            units_on_order,
            reorder_level,
            discontinued
        )
        if product:
            category_name = CategoryDao.get_category_name_by_id(product.CategoryID)
            return Product(
                product_id=product.product_id,
                name=product.name,
                description=product.description,
                category_id=product.category_id,
                category_name=category_name,
                unit_price=product.unit_price,
                units_in_stock=product.units_in_stock,
                units_on_order=product.units_on_order,
                reorder_level=product.reorder_level,
                discontinued=product.discontinued
            )
        return None

    @strawberry.mutation
    def update_product(
        self,
        product_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        category_id: Optional[int] = None,
        unit_price: Optional[float] = None,
        units_in_stock: Optional[int] = None,
        units_on_order: Optional[int] = None,
        reorder_level: Optional[int] = None,
        discontinued: Optional[bool] = None
    ) -> Optional[Product]:
        product = ProductDao.update_product(
            product_id,
            name,
            description,
            category_id,
            unit_price,
            units_in_stock,
            units_on_order,
            reorder_level,
            discontinued
        )
        if product:
            category = CategoryDao.get_category_by_id(product.category_id)
            return Product(
                product_id=product.product_id,
                name=product.name,
                description=product.description,
                category_id=product.category_id,
                category_name=category.category_name if category else None,
                unit_price=product.unit_price,
                units_in_stock=product.units_in_stock,
                units_on_order=product.units_on_order,
                reorder_level=product.reorder_level,
                discontinued=product.discontinued
            )
        return None

    @strawberry.mutation
    def delete_product(self, product_id: int) -> bool:
        return ProductDao.delete_product(product_id)

    @strawberry.mutation
    def create_supplier_order(self, input: SupplierOrderInput) -> SupplierOrder:
        supplier_id = input.supplier_id
        quantity = input.quantity
        product_id = input.product_id

        # Create the supplier order and return the result
        return SupplierOrderDAO.create_supplier_order(supplier_id, quantity, product_id)

    @strawberry.mutation
    def update_supplier_order(self, order_id: int, input: SupplierOrderInput) -> SupplierOrder:
        supplier_id = input.supplier_id
        quantity = input.quantity
        product_id = input.product_id

        # Update the supplier order and return the result
        return SupplierOrderDAO.update_supplier_order(order_id, supplier_id, quantity, product_id)

    @strawberry.mutation
    def delete_supplier_order(self, order_id: int) -> bool:
        # Delete the supplier order and return the result
        return SupplierOrderDAO.delete_supplier_order(order_id)
    
    @strawberry.mutation
    def update_inbound_bill(self, input: UpdateInboundBillInput) -> InboundBill:
        return InboundBillDAO.update_inbound_bill_amount_paid(input.inbound_bill_id, input.amount_paid)
    @strawberry.mutation
    def create_customer(
        self,
        name: str,
        address: str,
        contact: str,
        contact_number: str,
        email: str,
        membership_id: Optional[int] = None
    ) -> Optional[CustomerType]:
        if not CustomerDao.is_valid_email(email):
            raise ValueError("Invalid email address")

        if not CustomerDao.is_valid_contact_number(contact_number):
            raise ValueError("Invalid contact number")

        customer = CustomerDao.create_customer(
            name,
            address,
            contact,
            contact_number,
            email,
            membership_id
        )

        return CustomerType(
            customer_id=customer.CustomerID,
            name=customer.CustomerName,
            address=customer.Address,
            contact=customer.ContactPerson,
            contact_number=customer.ContactNumber,
            email=customer.Email,
            membership_id=customer.membership_id if customer.membership_id else None,
            membership_type=customer.membership.membership_type if customer.membership else None
        )


    @strawberry.mutation
    def update_customer(
        self,
        customer_id: int,
        name: Optional[str] = None,
        address: Optional[str] = None,
        contact: Optional[str] = None,
        contact_number: Optional[str] = None,
        email: Optional[str] = None,
        membership_id: Optional[int] = None,
        ) -> Optional[CustomerType]:
        customer = CustomerDao.get_customer_by_id(customer_id)
        if not customer:
            return None

        if email is not None and not CustomerDao.is_valid_email(email):
            raise ValueError("Invalid email address")

        if contact_number is not None and not CustomerDao.is_valid_contact_number(contact_number):
            raise ValueError("Invalid contact number")

        updated_customer = CustomerDao.update_customer(
            customer_id,
            name or customer.CustomerName,
            contact or customer.ContactPerson,
            contact_number or customer.ContactNumber,
            email or customer.Email,
            address or customer.Address
        )

        return CustomerType(
            customer_id=updated_customer.CustomerID,
            name=updated_customer.CustomerName,
            address=updated_customer.Address,
            contact=updated_customer.ContactPerson,
            contact_number=updated_customer.ContactNumber,
            email=updated_customer.Email,
            membership_id=updated_customer.membership_id,
            membership_type=updated_customer.membership.membership_type if updated_customer.membership else None
        )

    @strawberry.mutation
    def delete_customer(self, customer_id: int) -> bool:
        return CustomerDao.delete_customer(customer_id)
    



    @strawberry.mutation
    def create_customer_order(self, input: CustomerOrderInput) -> Optional[CustomerOrder]:
        customer_id = input.customer_id
        order_date = date.today()  # Get today's date
        shipping_address = input.shipping_address
        quantity = input.quantity
        product_id = input.product_id

        # Calculate total_amount based on quantity and product unit price
        product = Product.query.get(product_id)
        total_amount = quantity * product.UnitPrice

        # Create the customer order and return the result
        return CustomerOrderDAO.create_customer_order(
            customer_id,
            order_date,
            shipping_address,
            quantity,
            total_amount,
            product_id
        )
    @strawberry.mutation
    def update_customer_order(self, order_id: int, input: CustomerOrderInput) -> Optional[CustomerOrder]:
        customer_id = input.customer_id
        shipping_address = input.shipping_address
        quantity = input.quantity
        product_id = input.product_id

        # Update the customer order and return the result
        return CustomerOrderDAO.update_customer_order(order_id, customer_id, shipping_address, quantity, product_id)

    @strawberry.mutation
    def delete_customer_order(self, order_id: int) -> bool:
        # Delete the customer order and return the result
        return CustomerOrderDAO.delete_customer_order(order_id)

    @strawberry.mutation
    def create_outbound_bill(
        self,
        customer_order_id: int,
        bill_date: date,
        amount_paid: float,
        payment_status: str,
    ) -> Optional[OutboundBill]:
        outbound_bill = OutboundBillDAO.create_outbound_bill(
            customer_order_id,
            bill_date,
            amount_paid,
            payment_status,
        )

        return outbound_bill

    @strawberry.mutation
    def update_outbound_bill(
        self,
        outbound_bill_id: int,
        amount_paid: float,
        payment_status: str,
    ) -> Optional[OutboundBill]:
        updated_bill = OutboundBillDAO.update_outbound_bill(outbound_bill_id, amount_paid, payment_status)

        return updated_bill

    @strawberry.mutation
    def delete_outbound_bill(self, outbound_bill_id: int) -> bool:
        return OutboundBillDAO.delete_outbound_bill(outbound_bill_id)


    
schema = strawberry.Schema(query=Query, mutation=Mutation)
