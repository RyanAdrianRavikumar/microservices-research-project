import pika
import time

MESSAGES = 10000
EXCHANGE = "orders-exchange"
ROUTING_KEY = "order.created"

print(f"Starting RabbitMQ queue flood — {MESSAGES} messages")
print("Make sure Wireshark is capturing on loopback with filter: tcp.port == 5672")
input("Press ENTER when Wireshark is ready and capturing...")

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672)
)
channel = connection.channel()

# Declare exchange to make sure it exists
channel.exchange_declare(
    exchange=EXCHANGE,
    exchange_type='topic',
    durable=True
)

start = time.time()
for i in range(MESSAGES):
    message = f"Order{{id={i}, item=flood-item, quantity=99}}"
    channel.basic_publish(
        exchange=EXCHANGE,
        routing_key=ROUTING_KEY,
        body=message.encode()
    )
    if i % 1000 == 0:
        print(f"Published {i}/{MESSAGES} messages...")

elapsed = time.time() - start
connection.close()

print(f"\nDone! {MESSAGES} messages published in {elapsed:.2f} seconds")
print(f"Rate: {MESSAGES/elapsed:.0f} messages/second")
print("\nNow stop Wireshark and save as: attacks/queue_flood.pcapng")
print("Check RabbitMQ dashboard at http://localhost:15672 — queue depth should be very high")