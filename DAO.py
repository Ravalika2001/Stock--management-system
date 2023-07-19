import re
from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload
from models import *
from datetime import date


class SupplierDAO:
    def __init__(self, session: Session):
        self.session = session

    def create_supplier(self, name: str, contact_number: str) -> Supplier:
        supplier = Supplier(name=name, contact_number=contact_number)
        self.session.add(supplier)
        self.session.commit()
        return supplier

    def get_supplier_by_id(self, supplier_id: int) -> Optional[Supplier]:
        return self.session.query(Supplier).get(supplier_id)

    
    def get_all_suppliers(self) -> List[Supplier]:
        return self.session.query(Supplier).all()
    
    def get_products_by_supplier_name(self, supplier_name: str) -> List[Product]:
        return (
            self.session.query(Product)
            .join(SupplierOrderItem, SupplierOrderItem.product_id == Product.id)
            .join(SupplierOrder, SupplierOrder.id == SupplierOrderItem.supplier_order_id)
            .join(Supplier, Supplier.id == SupplierOrder.supplier_id)
            .filter(Supplier.name == supplier_name)
            .all()
        )
    

    def update_supplier(self, supplier_id: int, name: Optional[str] = None, contact_number: Optional[str] = None) -> Optional[Supplier]:
        supplier = self.session.query(Supplier).get(supplier_id)
        if supplier:
            if name:
                supplier.name = name
            if contact_number:
                supplier.contact_number = contact_number
            self.session.commit()
            return supplier
        return None

    def delete_supplier(self, supplier_id: int) -> bool:
        supplier = self.session.query(Supplier).get(supplier_id)
        if supplier:
            self.session.delete(supplier)
            self.session.commit()
            return True
        return False

    def get_supplier_products(self, supplier_id: int) -> List[Product]:
        supplier = self.session.query(Supplier).get(supplier_id)
        if supplier:
            products = (
            self.session.query(Product)
            .join(SupplierOrderItem, Product.id==SupplierOrderItem.product_id)
            .join(SupplierOrder)
            .filter(SupplierOrder.supplier_id == supplier_id)
            .all()
            )
        
            return products
    
    def get_supplier_by_name(self, supplier_name: str) -> List[Supplier]:
        suppliers = (
            self.session.query(Supplier)
            .filter(Supplier.name == supplier_name)
            .all()
        )

        return suppliers
    
    def get_suppliers_by_category_id(self, category_id: int) -> List[Supplier]:
        suppliers = (
            self.session.query(Supplier)
            .join(SupplierOrder, Supplier.id == SupplierOrder.supplier_id)
            .join(SupplierOrderItem, SupplierOrderItem.supplier_order_id == SupplierOrder.id)
            .join(Product, Product.id == SupplierOrderItem.product_id)
            .join(Category, Category.product_id == Product.id)
            .filter(Category.id == category_id)
            .all()
        )
        return suppliers
    
    def get_products_by_supplier_id(self, supplier_id: int) -> List[Product]:
        products = (
            self.session.query(Product)
            .join(SupplierOrderItem, SupplierOrderItem.product_id == Product.id)
            .join(SupplierOrder, SupplierOrder.id == SupplierOrderItem.supplier_order_id)
            .join(Supplier, Supplier.id == SupplierOrder.supplier_id)
            .filter(Supplier.id == supplier_id)
            .all()
        )
        return products
    

    
#================================================================================================================================   

class ProductDAO:
    def __init__(self, session: Session):
        self.session = session

    def get_most_sold_product(self) -> Optional[Product]:
        result = (
            self.session.query(
                ConsumerOrderItem.product_id,
                func.sum(ConsumerOrderItem.quantity).label("total_quantity")
            )
            .group_by(ConsumerOrderItem.product_id)
            .order_by(func.sum(ConsumerOrderItem.quantity).desc())
            .first()
        )
        if result:
            product_id, total_quantity = result
            product = self.session.query(Product).get(product_id)
            if product:
                product.total_quantity = total_quantity
            return product
        return None

    def get_most_bought_product(self) -> Optional[Product]:
        result = (
            self.session.query(
                SupplierOrderItem.product_id,
                func.sum(SupplierOrderItem.quantity).label("total_quantity")
            )
            .group_by(SupplierOrderItem.product_id)
            .order_by(func.sum(SupplierOrderItem.quantity).desc())
            .first()
        )
        if result:
            product_id, total_quantity = result
            product = self.session.query(Product).get(product_id)
            if product:
                product.total_quantity = total_quantity
            return product
        return None

    def create_product(self, name: str, unit_price: float, description: str, category_id: int) -> Product:
        product = Product(name=name, unit_price=unit_price, description=description, category_id=category_id)
        self.session.add(product)
        self.session.commit()
        return product

    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        return self.session.query(Product).get(product_id)

    def get_products_by_category(self, category_id: int) -> List[Product]:
        return self.session.query(Product).filter_by(category_id=category_id).all()
    
    def get_products_by_category_name(self, category_name: str) -> List[Product]:
        return (
                self.session.query(Product)
                .filter(Category.category_name == category_name)
                .all())

    def get_products_by_supplierorder_date(self, supplier_order_date: str) -> List[Product]:
        return (
            self.session.query(Product)
            .join(SupplierOrderItem, Product.id == SupplierOrderItem.product_id)
            .join(SupplierOrder, SupplierOrderItem.supplier_order_id == SupplierOrder.id)
            .filter(SupplierOrder.order_date == supplier_order_date)
            .all()
        )
    def get_supplier_by_productid(self, product_id: int) -> Optional[Supplier]:
        supplier = (
            self.session.query(Supplier)
            .join(SupplierOrder, Supplier.id == SupplierOrder.supplier_id)
            .join(SupplierOrderItem, SupplierOrderItem.supplier_order_id == SupplierOrder.id)
            .join(Product, Product.id == SupplierOrderItem.product_id)
            .filter(Product.id == product_id)
            .first()
        )
        return supplier
    
    def get_products_by_supplier_id(self, supplier_id: int) -> List[Product]:
        products = (
            self.session.query(Product)
            .join(SupplierOrderItem, SupplierOrderItem.product_id == Product.id)
            .join(SupplierOrder, SupplierOrder.id == SupplierOrderItem.supplier_order_id)
            .join(Supplier, Supplier.id == SupplierOrder.supplier_id)
            .filter(Supplier.id == supplier_id)
            .all()
        )
        return products

    
    def get_all_products(self) -> List[Product]:
        return self.session.query(Product).all()

    def update_product(self, product_id: int, name: Optional[str] = None, unit_price: Optional[float] = None,
                       description: Optional[str] = None) -> Optional[Product]:
        product = self.session.query(Product).get(product_id)
        if product:
            if name:
                product.name = name
            if unit_price:
                product.unit_price = unit_price
            if description:
                product.description = description
            self.session.commit()
            return product
        return None

    def delete_product(self, product_id: int) -> bool:
        product = self.session.query(Product).get(product_id)
        if product:
            self.session.delete(product)
            self.session.commit()
            return True
        return False
    
    def get_product_by_name(self, product_name: str) -> Optional[Product]:
        product = (
            self.session.query(Product)
            .filter(func.lower(Product.name) == func.lower(product_name))
            .first()
        )
        
        return product
    
    def get_suppliers_by_product_name(self, product_name: str) -> List[Supplier]:
        suppliers = (
            self.session.query(Supplier)
            .join(SupplierOrder, Supplier.id == SupplierOrder.supplier_id)
            .join(SupplierOrderItem, SupplierOrderItem.supplier_order_id == SupplierOrder.id)
            .join(Product, Product.id == SupplierOrderItem.product_id)
            .filter(Product.name == product_name)
            .all()
        )
        
        return suppliers
    
    def get_products_by_consumer_order_item(self, consumer_order_item_id: int) -> List[Product]:
        products = (
            self.session.query(Product)
            .join(ConsumerOrderItem, Product.id == ConsumerOrderItem.product_id)
            .filter(ConsumerOrderItem.id == consumer_order_item_id)
            .all()
        )
        return products
    
    def get_products_by_supplier_order_item(self, supplier_order_item_id: int) -> List[Product]:
        products = (
             self.session.query(Product)
            .join(SupplierOrderItem, Product.id == SupplierOrderItem.product_id)
            .filter(SupplierOrderItem.id == supplier_order_item_id)
            .all()
        )
        return products
    
    def get_category_by_product_id(self, product_id: int) -> Optional[Category]:
        product = self.session.query(Product).get(product_id)
        if product:
            category = product.category
            if category:
                return category
        return None
    
    def get_category_by_product_name(self, product_name: str) -> Optional[Category]:
        product = self.session.query(Product).filter(Product.name == product_name).first()
        if product:
            category = product.category
            if category:
                return category
        return None
    
# ================================================================================================================================================


class CategoryDAO:
    def __init__(self, session: Session):
        self.session = session

    def create_category(self, category_name: str) -> Category:
        category = Category(category_name=category_name)
        self.session.add(category)
        self.session.commit()
        return category
    


    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        return self.session.query(Category).get(category_id)
    
    def get_all_categories(self) -> List[Category]:
        return self.session.query(Category).all()

    def update_category(self, category_id: int, category_name: str) -> Optional[Category]:
        category = self.session.query(Category).get(category_id)
        if category:
            category.category_name = category_name
            self.session.commit()
            return category
        return None

    def delete_category(self, category_id: int) -> bool:
        category = self.session.query(Category).get(category_id)
        if category:
            self.session.delete(category)
            self.session.commit()
            return True
        return False
    
    def get_category_by_name(self, category_name: str) -> Optional[Category]:
        category = (
            self.session.query(Category)
            .filter(func.lower(Category.category_name) == func.lower(category_name))
            .first()
        )
        
        return category

    def get_category_by_supplierid(self, supplier_id: int) -> List[Category]:
        categories = (
            self.session.query(Category)
            .join(Product, Category.product_id == Product.id)
            .join(SupplierOrderItem, SupplierOrderItem.product_id == Product.id)
            .join(SupplierOrder, SupplierOrder.id == SupplierOrderItem.supplier_order_id)
            .join(Supplier, Supplier.id == SupplierOrder.supplier_id)
            .filter(Supplier.id == supplier_id)
            .all()
        )
        return categories

 
class SupplierOrderDAO:
    def __init__(self, session: Session):
        self.session = session

    def create_supplier_order(self, supplier_id: int, order_date: str, total_amount: float) -> SupplierOrder:
        supplier_order = SupplierOrder(supplier_id=supplier_id, order_date=order_date, total_amount=total_amount)
        self.session.add(supplier_order)
        self.session.commit()
        return supplier_order

    def get_supplier_order_by_id(self, supplier_order_id: int) -> Optional[SupplierOrder]:
        return self.session.query(SupplierOrder).get(supplier_order_id)
    
    def get_all_supplier_orders(self) -> List[SupplierOrder]:
        return self.session.query(SupplierOrder).all()

    def update_supplier_order(self, supplier_order_id: int, order_date: Optional[str] = None,
                              total_amount: Optional[float] = None) -> Optional[SupplierOrder]:
        supplier_order = self.session.query(SupplierOrder).get(supplier_order_id)
        if supplier_order:
            if order_date:
                supplier_order.order_date = order_date
            if total_amount:
                supplier_order.total_amount = total_amount
            self.session.commit()
            return supplier_order
        return None

    def delete_supplier_order(self, supplier_order_id: int) -> bool:
        supplier_order = self.session.query(SupplierOrder).get(supplier_order_id)
        if supplier_order:
            self.session.delete(supplier_order)
            self.session.commit()
            return True
        return False
    
    def get_suppliers_by_product_name(self, product_name: str) -> List[Supplier]:
        suppliers = (
            self.session.query(Supplier)
            .join(SupplierOrder, Supplier.id == SupplierOrder.supplier_id)
            .join(SupplierOrderItem, SupplierOrderItem.supplier_order_id == SupplierOrder.id)
            .join(Product, Product.id == SupplierOrderItem.product_id)
            .filter(Product.name == product_name)
            .all()
        )
        
        return suppliers
    
    def get_supplier_order_items_by_order_date(self, order_date: date) -> List[SupplierOrderItem]:
        supplier_order_items = (
            self.session.query(SupplierOrderItem)
            .join(SupplierOrder, SupplierOrder.id == SupplierOrderItem.supplier_order_id)
            .filter(SupplierOrder.order_date == order_date)
            .all()
        )
        return supplier_order_items
        
    def get_supplier_orders_by_order_date(self, order_date: date) -> List[SupplierOrder]:
        return self.session.query(SupplierOrder).filter(SupplierOrder.order_date == order_date).all()
    
    def get_products_by_supplier_order_id(self, supplier_order_id: int) -> List[Product]:
        products = (
            self.session.query(Product)
            .join(SupplierOrderItem, Product.id == SupplierOrderItem.product_id)
            .filter(SupplierOrderItem.supplier_order_id == supplier_order_id)
            .all()
        )
        return products
    
    
    
    


class SupplierOrderItemDAO:
    def __init__(self, session: Session):
        self.session = session

    def create_supplier_order_item(
        self,
        supplier_order_id: int,
        product_id: int,
        item_name: str,
        quantity: int,
        unit_price: float,
        calculate_total: bool = True,
    ) -> SupplierOrderItem:
        supplier_order_item = SupplierOrderItem(
            supplier_order_id=supplier_order_id,
            product_id=product_id,
            item_name=item_name,
            quantity=quantity,
            unit_price=unit_price,
        )

        if calculate_total:
            supplier_order_item.calculate_total_price()

        # Update the total_amount of the associated SupplierOrder
        supplier_order = self.session.query(SupplierOrder).get(supplier_order_id)
        if supplier_order:
            if supplier_order_item.total_price is not None:
                if supplier_order.total_amount is None:
                    supplier_order.total_amount = 0  # Initialize to 0 if None
                supplier_order.total_amount += supplier_order_item.total_price

        self.session.add(supplier_order_item)
        self.session.commit()

        return supplier_order_item

    def get_supplier_order_item_by_id(self, supplier_order_item_id: int) -> Optional[SupplierOrderItem]:
        return self.session.query(SupplierOrderItem).get(supplier_order_item_id)
    
    
    def get_all_supplier_order_items(self) -> List[SupplierOrderItem]:
        return self.session.query(SupplierOrderItem).all()

    def update_supplier_order_item(
        self,
        supplier_order_item_id: int,
        item_name: Optional[str] = None,
        quantity: Optional[int] = None,
        unit_price: Optional[float] = None,
        calculate_total: bool = True,
    ) -> Optional[SupplierOrderItem]:
        supplier_order_item = self.session.query(SupplierOrderItem).get(supplier_order_item_id)
        if supplier_order_item:
            if item_name is not None:
                supplier_order_item.item_name = item_name
            if quantity is not None:
                supplier_order_item.quantity = quantity
            if unit_price is not None:
                supplier_order_item.unit_price = unit_price

            if calculate_total:
                supplier_order_item.calculate_total_price()

            # Update the total_amount of the associated SupplierOrder
            supplier_order = supplier_order_item.order
            if supplier_order:
                if supplier_order_item.total_price is not None:
                    if supplier_order.total_amount is None:
                        supplier_order.total_amount = 0  # Initialize to 0 if None
                    supplier_order.total_amount += supplier_order_item.total_price

            self.session.commit()
            return supplier_order_item

        return None

    def delete_supplier_order_item(self, supplier_order_item_id: int) -> bool:
        supplier_order_item = self.session.query(SupplierOrderItem).get(supplier_order_item_id)
        if supplier_order_item:
            self.session.delete(supplier_order_item)
            self.session.commit()
            return True
        return False
    
    


class ConsumerOrderDAO:
    def __init__(self, session: Session):
        self.session = session

    def create_consumer_order(
        self,
        consumer_id: int,
        order_date: str,
        total_amount: float,
    ) -> ConsumerOrder:
        consumer_order = ConsumerOrder(consumer_id=consumer_id, order_date=order_date, total_amount=total_amount)

        self.session.add(consumer_order)
        self.session.commit()
        return consumer_order
    
    def get_consumer_orders_by_order_date(self, order_date: date) -> List[ConsumerOrder]:
        return self.session.query(ConsumerOrder).filter(ConsumerOrder.order_date == order_date).all()

    def get_consumer_order_by_id(self, consumer_order_id: int) -> Optional[ConsumerOrder]:
        return self.session.query(ConsumerOrder).get(consumer_order_id)
    
    def get_consumers_by_product_name(self, product_name: str) -> List[Consumer]:
        consumers = (
            self.session.query(Consumer)
            .join(ConsumerOrder, Consumer.id == ConsumerOrder.consumer_id)
            .join(ConsumerOrderItem, ConsumerOrderItem.consumer_order_id == ConsumerOrder.id)
            .join(Product, Product.id == ConsumerOrderItem.product_id)
            .filter(Product.name == product_name)
            .all()
        )
    
        return consumers
    
    def get_all_consumer_orders(self) -> List[ConsumerOrder]:
        return self.session.query(ConsumerOrder).all()

    def update_consumer_order(
        self,
        consumer_order_id: int,
        order_date: Optional[str] = None,
        total_amount: Optional[float] = None,
    ) -> Optional[ConsumerOrder]:
        consumer_order = self.session.query(ConsumerOrder).get(consumer_order_id)

        if consumer_order:
            if order_date is not None:
                consumer_order.order_date = order_date
            if total_amount is not None:
                consumer_order.total_amount = total_amount

            self.session.commit()
            return consumer_order

        return None

    def delete_consumer_order(self, consumer_order_id: int) -> bool:
        consumer_order = self.session.query(ConsumerOrder).get(consumer_order_id)
        if consumer_order:
            self.session.delete(consumer_order)
            self.session.commit()
            return True
        return False
    
    def get_products_by_consumer_order_date(self, order_date: date) -> List[Product]:
        products = (
            self.session.query(Product)
            .join(ConsumerOrderItem, Product.id == ConsumerOrderItem.product_id)
            .join(ConsumerOrder, ConsumerOrder.id == ConsumerOrderItem.consumer_order_id)
            .filter(ConsumerOrder.order_date == order_date)
            .all()
        )
        return products

    def get_products_by_consumer_order_id(self, order_id: int) -> List[Product]:
        products = (
            self.session.query(Product)
            .join(ConsumerOrderItem, Product.id == ConsumerOrderItem.product_id)
            .filter(ConsumerOrderItem.consumer_order_id == order_id)
            .all()
        )
        return products
    
    def get_products_by_consumer_order_id(self, consumer_order_id: int) -> List[Product]:
        products = (
            self.session.query(Product)
            .join(ConsumerOrderItem, Product.id == ConsumerOrderItem.product_id)
            .join(ConsumerOrder, ConsumerOrder.id == ConsumerOrderItem.consumer_order_id)
            .filter(ConsumerOrder.id == consumer_order_id)
            .all()
        )
        return products

    def get_products_by_consumer_order_date(self, consumer_order_date: str) -> List[Product]:
        products = (
            self.session.query(Product)
            .join(ConsumerOrderItem, Product.id == ConsumerOrderItem.product_id)
            .join(ConsumerOrder, ConsumerOrder.id == ConsumerOrderItem.consumer_order_id)
            .filter(ConsumerOrder.order_date == consumer_order_date)
            .all()
        )
        return products

# =======================================================================================================

class ConsumerOrderItemDAO:
    def __init__(self, session: Session):
        self.session = session

    

    def create_consumer_order_item(
        self,
        consumer_order_id: int,
        product_id: int,
        item_name: str,
        quantity: int,
        unit_price: float,
        total_price: float = 0.0,
    ) -> ConsumerOrderItem:
        consumer_order_item = ConsumerOrderItem(
            consumer_order_id=consumer_order_id,
            product_id=product_id,
            item_name=item_name,
            quantity=quantity,
            unit_price=unit_price,
            total_price=total_price,
        )
        consumer_order_item.total_price = quantity*unit_price
        self.session.add(consumer_order_item)

        # Update the total_amount of the associated ConsumerOrder
        consumer_order = consumer_order_item.order
        if consumer_order:
            consumer_order.total_amount += total_price

        self.session.commit()

        return consumer_order_item
    
    def get_consumer_order_items_by_order_date(self, order_date: date) -> List[ConsumerOrderItem]:
        consumer_order_items = (
            self.session.query(ConsumerOrderItem)
            .join(ConsumerOrder, ConsumerOrder.id == ConsumerOrderItem.consumer_order_id)
            .filter(ConsumerOrder.order_date == order_date)
            .all()
        )
        return consumer_order_items

    def get_consumer_order_item_by_id(self, consumer_order_item_id: int) -> Optional[ConsumerOrderItem]:
        return self.session.query(ConsumerOrderItem).get(consumer_order_item_id)
    
    def get_all_consumer_order_items(self) -> List[ConsumerOrderItem]:
        return self.session.query(ConsumerOrderItem).all()

    def update_consumer_order_item(
        self,
        consumer_order_item_id: int,
        item_name: Optional[str] = None,
        quantity: Optional[int] = None,
        unit_price: Optional[float] = None,
        total_price: Optional[float] = None,
    ) -> Optional[ConsumerOrderItem]:
        consumer_order_item = self.session.query(ConsumerOrderItem).get(consumer_order_item_id)
        if consumer_order_item:
            if item_name is not None:
                consumer_order_item.item_name = item_name
            if quantity is not None:
                consumer_order_item.quantity = quantity
            if unit_price is not None:
                consumer_order_item.unit_price = unit_price

            if quantity is not None and unit_price is not None:
                consumer_order_item.total_price = quantity * unit_price
            elif total_price is not None:
                consumer_order_item.total_price = total_price

            # Update the total_amount of the associated ConsumerOrder
            consumer_order = consumer_order_item.order
            if consumer_order:
                consumer_order.total_amount += consumer_order_item.total_price

            self.session.commit()
            return consumer_order_item

        return None



    def delete_consumer_order_item(self, consumer_order_item_id: int) -> bool:
        consumer_order_item = self.session.query(ConsumerOrderItem).get(consumer_order_item_id)
        if consumer_order_item:
            self.session.delete(consumer_order_item)
            self.session.commit()
            return True
        return False
    
    def get_most_sold_product(self) -> Optional[Product]:
        result = (
            self.session.query(
                ConsumerOrderItem.product_id,
                func.sum(ConsumerOrderItem.quantity).label("total_quantity")
            )
            .group_by(ConsumerOrderItem.product_id)
            .order_by(func.sum(ConsumerOrderItem.quantity).desc())
            .first()
        )
        if result:
            product_id, total_quantity = result
            product = self.session.query(Product).get(product_id)
            if product:
                product.total_quantity = total_quantity
            return product
        return None
    
    
# =====================================================================================================================

class ConsumerDAO:
    def __init__(self, session: Session):
        self.session = session

    def create_consumer(self, name: str, contact_number: str) -> Consumer:
        consumer = Consumer(name=name, contact_number=contact_number)
        self.session.add(consumer)
        self.session.commit()
        return consumer


    def get_consumer_by_id(self, consumer_id: int) -> Optional[Consumer]:
        return self.session.query(Consumer).get(consumer_id)

    def get_consumers_by_name(self, name: str) -> List[Consumer]:
        pattern = re.compile(name, re.IGNORECASE)
        return self.session.query(Consumer).filter(pattern.match(Consumer.name)).all()
    
    def get_all_consumers(self) -> List[Consumer]:
        return self.session.query(Consumer).all()

    def update_consumer(self, consumer_id: int, name: Optional[str] = None,
                        contact_number: Optional[str] = None) -> Optional[Consumer]:
        consumer = self.session.query(Consumer).get(consumer_id)
        if consumer:
            if name:
                consumer.name = name
            if contact_number:
                consumer.contact_number = contact_number
            self.session.commit()
            return consumer
        return None

    def delete_consumer(self, consumer_id: int) -> bool:
        consumer = self.session.query(Consumer).get(consumer_id)
        if consumer:
            self.session.delete(consumer)
            self.session.commit()
            return True
        return False
    
    def get_consumer_by_membership_id(self, membership_id: int) -> Optional[Consumer]:
        consumer = (
            self.session.query(Consumer)
            .join(ConsumerMembership, Consumer.id == ConsumerMembership.consumer_id)
            .filter(ConsumerMembership.id == membership_id)
            .first()
        )
        return consumer
    
    def get_products_by_consumer_id(self, consumer_id: int) -> List[Product]:
        return (
            self.session.query(Product)
            .join(ConsumerOrderItem, ConsumerOrderItem.product_id == Product.id)
            .join(ConsumerOrder, ConsumerOrder.id == ConsumerOrderItem.consumer_order_id)
            .join(Consumer, Consumer.id == ConsumerOrder.consumer_id)
            .filter(Consumer.id == consumer_id)
            .all()
        )

    def get_products_by_consumer_name(self, consumer_name: str) -> List[Product]:
        return (
            self.session.query(Product)
            .join(ConsumerOrderItem, ConsumerOrderItem.product_id == Product.id)
            .join(ConsumerOrder, ConsumerOrder.id == ConsumerOrderItem.consumer_order_id)
            .join(Consumer, Consumer.id == ConsumerOrder.consumer_id)
            .filter(Consumer.name == consumer_name)
            .all()
        )
    def get_consumers_by_name(self, consumer_name: str) -> List[Consumer]:
        return self.session.query(Consumer).filter(Consumer.name == consumer_name).all()

#================================================================================================================================== 
class ConsumerMembershipDAO:
    def __init__(self, session: Session):
        self.session = session

    def create_consumer_membership(self, consumer_id: int, start_date: str, end_date: str) -> ConsumerMembership:
        consumer_membership = ConsumerMembership(consumer_id=consumer_id, start_date=start_date, end_date=end_date)
        self.session.add(consumer_membership)
        self.session.commit()
        return consumer_membership

    def get_consumer_membership_by_id(self, membership_id: int) -> Optional[ConsumerMembership]:
        return self.session.query(ConsumerMembership).get(membership_id)

    def get_all_consumer_memberships(self) -> List[ConsumerMembership]:
        return self.session.query(ConsumerMembership).all()

    def update_consumer_membership(
        self,
        membership_id: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Optional[ConsumerMembership]:
        consumer_membership = self.session.query(ConsumerMembership).get(membership_id)
        if consumer_membership:
            if start_date:
                consumer_membership.start_date = start_date
            if end_date:
                consumer_membership.end_date = end_date
            self.session.commit()
            return consumer_membership
        return None

    def delete_consumer_membership(self, membership_id: int) -> bool:
        consumer_membership = self.session.query(ConsumerMembership).get(membership_id)
        if consumer_membership:
            self.session.delete(consumer_membership)
            self.session.commit()
            return True
        return False
    
    