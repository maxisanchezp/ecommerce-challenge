import pika
import json


RABBIT_HOST = 'localhost'
RABBIT_QUEUE = 'orders'


def publish_order_message(order_id: int, total_amount: float):
    
    ### PUBLICAR MENSAJE CUANDO SE CREA UNA ORDER
    
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=RABBIT_QUEUE, durable=True)\
    
    message = json.dumps({
        "order_id": order_id,
        "total_amount": total_amount,
    })
    
    channel.basic_publish(
        exchange="",
        routing_key=RABBIT_QUEUE,
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2
        )
    )
    
    print(f"[x] Sent order message: {message}")
    connection.close()