import requests
import random

items = ["book", "pen", "laptop", "phone", "tablet", "charger", "mouse", "keyboard", "monitor", "desk"]
success_count = 0

for i in range(10):
    payload = {
        "item": items[i],
        "quantity": random.randint(1, 5)
    }
    response = requests.post("http://localhost:8080/orders", json=payload)
    print(f"Status: {response.status_code} | Response: {response.text}")
    if response.status_code == 200:
        success_count += 1

print(f"\n{success_count}/10 requests succeeded")