from sqlalchemy.orm import Session
from ..core.database import get_db
from app.products.models import Products

def seed_products():
    db_gen = get_db()
    db: Session = next(db_gen)

    products = [
        Products(
            name="Wireless Mouse",
            description="Ergonomic wireless mouse with 2.4GHz connectivity.",
            price=999.99,
            stock=50,
            category="Electronics",
            image_url="https://example.com/mouse.jpg"
        ),
        Products(
            name="Bluetooth Headphones",
            description="Noise-cancelling over-ear Bluetooth headphones.",
            price=1999.50,
            stock=30,
            category="Electronics",
            image_url="https://example.com/headphones.jpg"
        ),
        Products(
            name="Yoga Mat",
            description="Non-slip yoga mat for daily workouts.",
            price=499.00,
            stock=100,
            category="Fitness",
            image_url="https://example.com/yogamat.jpg"
        )
    ]
    db.add_all(products)
    db.commit()
    db.close()
    try:
        next(db_gen)
    except StopIteration:
        pass
    print("✅ Seed data inserted successfully!")
    print("✅ Seed data inserted successfully!")

if __name__ == "__main__":
    seed_products()
