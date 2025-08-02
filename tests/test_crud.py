from app import crud, schemas
from app.models import SessionLocal

def test_create_product_and_order():
    db = SessionLocal()

    product_data = schemas.ProductCreate(
        name="Test product",
        description="Producto de prueba",
        price=10.0,
        stock=50
    )
    product = crud.create_product(db, product_data)
    assert product.id is not None

    # Crear orden
    order_data = schemas.OrderCreate(
        customer_id=1,
        items=[schemas.OrderItemCreate(product_id=product.id, quantity=3)]
    )
    order = crud.create_order(db, order_data)
    assert order.total_amount == 30.0
