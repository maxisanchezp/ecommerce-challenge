from sqlalchemy.orm import Session
from typing import List

import models
import schemas

### PRODUCTOS


def create_product(db: Session, product: schemas.ProductCreate) -> models.Product:
    db_product = models.Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
    )
    
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    return db_product


def get_product(db: Session, product_id: int) -> models.Product | None:
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def get_products(db: Session) -> List[models.Product]:
    return db.query(models.Product).all()

### ORDERS

def create_order(db: Session, order: schemas.OrderCreate) -> models.Order:
    
    # Calculate Total
    total_amount = 0.0
    db_items: List[models.OrderItem] = []
    
    for item in order.items:
        product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
        if not product:
            raise ValueError(f"Product {item.product_id} doesn't exist.")
        
        unit_price = product.price
        total_price = unit_price * item.quantity
        total_amount += total_price
        
        db_item = models.OrderItem(
            product_id = item.product_id,
            quantity=item.quantity,
            unit_price=unit_price,
            total_price=total_price,
        )
        
        db_items.append(db_item)
    
    db_order = models.Order(
        customer_id = order.customer_id,
        total_amount= total_amount,
        status='PENDIENTE',
        items=db_items,
    )
    
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    return db_order

def get_order(db: Session, order_id: int) -> models.Order | None:
    return(
        db.query(models.Order).filter(models.Order.id == order_id).first()
    )

def get_orders(db: Session) -> List[models.Order]:
    return db.query(models.Order).all()