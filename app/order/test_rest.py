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

# --- gRPC integration test ---
print("\n--- gRPC integration test ---")
grpc_items = ["book", "pen", "laptop", "phone", "tablet"]
grpc_pass_count = 0

for i in range(5):
    payload = {
        "item": grpc_items[i],
        "quantity": random.randint(1, 5)
    }
    response = requests.post("http://localhost:8080/orders", json=payload)
    has_grpc_confirmation = "stock confirmed via gRPC" in response.text
    status = "PASS" if has_grpc_confirmation else "FAIL"
    if has_grpc_confirmation:
        grpc_pass_count += 1
    print(f"Status: {response.status_code} | Response: {response.text} | {status}")

print(f"\ngRPC integration: {grpc_pass_count}/5 passed")