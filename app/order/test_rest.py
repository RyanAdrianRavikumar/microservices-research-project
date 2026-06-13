import requests
import random

items = ["book", "pen", "laptop", "phone", "tablet", "charger", "mouse", "keyboard", "monitor", "desk"]
success_count = 0

for i in range(200):
    payload = {
        "item": items[i % len(items)],
        "quantity": random.randint(1, 5)
    }
    response = requests.post("http://localhost:8080/orders", json=payload)
    print(f"Request {i+1}/20: POST /orders -> Status {response.status_code}: {response.text}")
    if response.status_code == 200:
        success_count += 1

print("====================")
print(f"Summary: {success_count}/20 succeeded")
print("Check RabbitMQ dashboard at http://localhost:15672")
print("Check notification-service console for 20 log entries")