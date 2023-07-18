from typing import List, Optional
from sqlalchemy.orm import Session
from models import *
from dao import *

# Resolver functions for the Query type
def resolve_get_supplier_by_int(supplier_int: int, session: Session) -> Optional[Supplier]:
    supplier_dao = SupplierDAO(session)
    return supplier_dao.get_supplier_by_int(supplier_int)

def resolve_get_all_suppliers(session: Session) -> List[Supplier]:
    supplier_dao = SupplierDAO(session)
    return supplier_dao.get_all_suppliers()


def resolve_get_product_by_int(product_int: int, session: Session) -> Optional[Product]:
    product_dao = ProductDAO(session)
    return product_dao.get_product_by_int(product_int)

def resolve_get_all_products(session: Session) -> List[Product]:
    product_dao = ProductDAO(session)
    return product_dao.get_all_products()

def resolve_get_products_by_category(category_int: int, session: Session) -> List[Product]:
    product_dao = ProductDAO(session)
    return product_dao.get_products_by_category(category_int)


def resolve_get_category_by_int(category_int: int, session: Session) -> Optional[Category]:
    category_dao = CategoryDAO(session)
    return category_dao.get_category_by_int(category_int)

def resolve_get_all_categories(session: Session) -> List[Category]:
    category_dao = CategoryDAO(session)
    return category_dao.get_all_categories()

def resolve_get_supplier_order_by_int(supplier_order_int: int, session: Session) -> Optional[SupplierOrder]:
    supplier_order_dao = SupplierOrderDAO(session)
    return supplier_order_dao.get_supplier_order_by_int(supplier_order_int)

def resolve_get_all_supplier_orders(session: Session) -> List[SupplierOrder]:
    supplier_order_dao = SupplierOrderDAO(session)
    return supplier_order_dao.get_all_supplier_orders()

def resolve_get_supplier_order_item_by_int(
    supplier_order_item_int: int, session: Session
) -> Optional[SupplierOrderItem]:
    supplier_order_item_dao = SupplierOrderItemDAO(session)
    return supplier_order_item_dao.get_supplier_order_item_by_int(supplier_order_item_int)

def resolve_get_all_supplier_order_items(session: Session) -> List[SupplierOrderItem]:
    supplier_order_item_dao = SupplierOrderItemDAO(session)
    return supplier_order_item_dao.get_all_supplier_order_items()

def resolve_get_consumer_order_by_int(consumer_order_int: int, session: Session) -> Optional[ConsumerOrder]:
    consumer_order_dao = ConsumerOrderDAO(session)
    return consumer_order_dao.get_consumer_order_by_int(consumer_order_int)

def resolve_get_all_consumer_orders(session: Session) -> List[ConsumerOrder]:
    consumer_order_dao = ConsumerOrderDAO(session)
    return consumer_order_dao.get_all_consumer_orders()

def resolve_get_consumer_order_item_by_int(
    consumer_order_item_int: int, session: Session
) -> Optional[ConsumerOrderItem]:
    consumer_order_item_dao = ConsumerOrderItemDAO(session)
    return consumer_order_item_dao.get_consumer_order_item_by_int(consumer_order_item_int)

def resolve_get_all_consumer_order_items(session: Session) -> List[ConsumerOrderItem]:
    consumer_order_item_dao = ConsumerOrderItemDAO(session)
    return consumer_order_item_dao.get_all_consumer_order_items()

def resolve_get_consumer_by_int(consumer_int: int, session: Session) -> Optional[Consumer]:
    consumer_dao = ConsumerDAO(session)
    return consumer_dao.get_consumer_by_int(consumer_int)

def resolve_get_consumers_by_name(name: str, session: Session) -> List[Consumer]:
    consumer_dao = ConsumerDAO(session)
    return consumer_dao.get_consumers_by_name(name)

def resolve_get_all_consumers(session: Session) -> List[Consumer]:
    consumer_dao = ConsumerDAO(session)
    return consumer_dao.get_all_consumers()


# Resolver functions for the Mutation type
def resolve_create_supplier(name: str, contact_number: str, session: Session) -> Supplier:
    supplier_dao = SupplierDAO(session)
    return supplier_dao.create_supplier(name, contact_number)

def resolve_update_supplier(supplier_int: int, session: Session, name: Optional[str] = None, contact_number: Optional[str] = None) -> Optional[Supplier]:
    supplier_dao = SupplierDAO(session)
    return supplier_dao.update_supplier(supplier_int, name, contact_number)

def resolve_delete_supplier(supplier_int: int, session: Session) -> bool:
    supplier_dao = SupplierDAO(session)
    return supplier_dao.delete_supplier(supplier_int)

def resolve_create_product(name: str, unit_price: float, description: str, category_int: int, session: Session) -> Product:
    product_dao = ProductDAO(session)
    return product_dao.create_product(name, unit_price, description, category_int)

def resolve_update_product(
    product_int: int, session: Session, name: Optional[str] = None, unit_price: Optional[float] = None, description: Optional[str] = None
) -> Optional[Product]:
    product_dao = ProductDAO(session)
    return product_dao.update_product(product_int, name, unit_price, description)

def resolve_delete_product(product_int: int, session: Session) -> bool:
    product_dao = ProductDAO(session)
    return product_dao.delete_product(product_int)

def resolve_create_category(category_name: str, session: Session) -> Category:
    category_dao = CategoryDAO(session)
    return category_dao.create_category(category_name)

def resolve_update_category(category_int: int, session: Session, category_name: str) -> Optional[Category]:
    category_dao = CategoryDAO(session)
    return category_dao.update_category(category_int, category_name)

def resolve_delete_category(category_int: int, session: Session) -> bool:
    category_dao = CategoryDAO(session)
    return category_dao.delete_category(category_int)

def resolve_create_supplier_order(
    supplier_int: int, order_date: str, total_amount: float, session: Session
) -> SupplierOrder:
    supplier_order_dao = SupplierOrderDAO(session)
    return supplier_order_dao.create_supplier_order(supplier_int, order_date, total_amount)

def resolve_update_supplier_order(
    supplier_order_int: int, session: Session, order_date: Optional[str] = None, total_amount: Optional[float] = None
) -> Optional[SupplierOrder]:
    supplier_order_dao = SupplierOrderDAO(session)
    return supplier_order_dao.update_supplier_order(supplier_order_int, order_date, total_amount)

def resolve_delete_supplier_order(supplier_order_int: int, session: Session) -> bool:
    supplier_order_dao = SupplierOrderDAO(session)
    return supplier_order_dao.delete_supplier_order(supplier_order_int)

def resolve_create_supplier_order_item(
    supplier_order_int: int,
    product_int: int,
    item_name: str,
    quantity: int,
    unit_price: float,
    session: Session,
) -> SupplierOrderItem:
    supplier_order_item_dao = SupplierOrderItemDAO(session)
    return supplier_order_item_dao.create_supplier_order_item(
        supplier_order_int, product_int, item_name, quantity, unit_price
    )

def resolve_update_supplier_order_item(
    supplier_order_item_int: int,
    session: Session,
    item_name: Optional[str] = None,
    quantity: Optional[int] = None,
    unit_price: Optional[float] = None,
) -> Optional[SupplierOrderItem]:
    supplier_order_item_dao = SupplierOrderItemDAO(session)
    return supplier_order_item_dao.update_supplier_order_item(
        supplier_order_item_int, item_name, quantity, unit_price
    )

def resolve_delete_supplier_order_item(supplier_order_item_int: int, session: Session) -> bool:
    supplier_order_item_dao = SupplierOrderItemDAO(session)
    return supplier_order_item_dao.delete_supplier_order_item(supplier_order_item_int)

def resolve_create_consumer_order(
    consumer_int: int, order_date: str, total_amount: float, session: Session
) -> ConsumerOrder:
    consumer_order_dao = ConsumerOrderDAO(session)
    return consumer_order_dao.create_consumer_order(consumer_int, order_date, total_amount)

def resolve_update_consumer_order(
    consumer_order_int: int, session: Session, order_date: Optional[str] = None, total_amount: Optional[float] = None
) -> Optional[ConsumerOrder]:
    consumer_order_dao = ConsumerOrderDAO(session)
    return consumer_order_dao.update_consumer_order(consumer_order_int, order_date, total_amount)

def resolve_delete_consumer_order(consumer_order_int: int, session: Session) -> bool:
    consumer_order_dao = ConsumerOrderDAO(session)
    return consumer_order_dao.delete_consumer_order(consumer_order_int)

def resolve_create_consumer_order_item(
    consumer_order_int: int,
    product_int: int,
    item_name: str,
    quantity: int,
    unit_price: float,
    session: Session,
) -> ConsumerOrderItem:
    consumer_order_item_dao = ConsumerOrderItemDAO(session)
    return consumer_order_item_dao.create_consumer_order_item(
        consumer_order_int, product_int, item_name, quantity, unit_price
    )

def resolve_update_consumer_order_item(
    consumer_order_item_int: int,
    session: Session,
    item_name: Optional[str] = None,
    quantity: Optional[int] = None,
    unit_price: Optional[float] = None,
) -> Optional[ConsumerOrderItem]:
    consumer_order_item_dao = ConsumerOrderItemDAO(session)
    return consumer_order_item_dao.update_consumer_order_item(
        consumer_order_item_int, item_name, quantity, unit_price
    )

def resolve_delete_consumer_order_item(consumer_order_item_int: int, session: Session) -> bool:
    consumer_order_item_dao = ConsumerOrderItemDAO(session)
    return consumer_order_item_dao.delete_consumer_order_item(consumer_order_item_int)

def resolve_create_consumer(name: str, contact_number: str, session: Session) -> Consumer:
    consumer_dao = ConsumerDAO(session)
    return consumer_dao.create_consumer(name, contact_number)

def resolve_update_consumer(consumer_int: int, session: Session, name: Optional[str] = None, contact_number: Optional[str] = None) -> Optional[Consumer]:
    consumer_dao = ConsumerDAO(session)
    return consumer_dao.update_consumer(consumer_int, name, contact_number)

def resolve_delete_consumer(consumer_int: int, session: Session) -> bool:
    consumer_dao = ConsumerDAO(session)
    return consumer_dao.delete_consumer(consumer_int)



def resolve_get_consumer_membership_by_id(membership_id: int, session: Session) -> Optional[ConsumerMembership]:
    consumer_membership_dao = ConsumerMembershipDAO(session)
    return consumer_membership_dao.get_consumer_membership_by_id(membership_id)

def resolve_get_all_consumer_memberships(session: Session) -> List[ConsumerMembership]:
    consumer_membership_dao = ConsumerMembershipDAO(session)
    return consumer_membership_dao.get_all_consumer_memberships()

def resolve_create_consumer_membership(
    consumer_id: int, start_date: str, end_date: str, session: Session
) -> ConsumerMembership:
    consumer_membership_dao = ConsumerMembershipDAO(session)
    return consumer_membership_dao.create_consumer_membership(consumer_id, start_date, end_date)

def resolve_update_consumer_membership(
    membership_id: int,
    session: Session,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> Optional[ConsumerMembership]:
    consumer_membership_dao = ConsumerMembershipDAO(session)
    return consumer_membership_dao.update_consumer_membership(membership_id, start_date, end_date)

def resolve_delete_consumer_membership(membership_id: int, session: Session) -> bool:
    consumer_membership_dao = ConsumerMembershipDAO(session)
    return consumer_membership_dao.delete_consumer_membership(membership_id)
