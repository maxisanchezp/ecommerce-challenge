from app.queue import publish_order_message

def test_publish_message():
    publish_order_message(order_id=6294, total_amount=100.0)
    assert True