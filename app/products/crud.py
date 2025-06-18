from sqlalchemy.orm import Session
from .schema import ProductCreate, ProductUpdate
from .models import Products

def create_product(db: Session, product: ProductCreate):
    db_product = Products(**product.__dict__)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def admin_get_all_products(db: Session, skip: int = 0, limit: int = 10):
    products = db.query(Products).offset(skip).limit(limit).all()
    return products if products else []

def get_product_by_id(db: Session, product_id: int):
    product = db.query(Products).filter(Products.id == product_id).first()
    return product if product else None

def update_product(db: Session, product_id: int, product: ProductUpdate):
    db_product = db.query(Products).filter(Products.id == product_id).first()
    if not db_product:
        return None
    for key, value in product.dict(exclude_unset=True).items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = db.query(Products).filter(Products.id == product_id).first()
    if not db_product:
        return None
    db.delete(db_product)
    db.commit()