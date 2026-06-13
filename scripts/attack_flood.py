import requests
import concurrent.futures
import time

TARGET_URL = "http://localhost:8080/orders"
TOTAL_REQUESTS = 1000
THREADS = 10

payload = {"item": "flood-test", "quantity": 1}
headers = {"Content-Type": "application/json"}

success = 0
failed = 0
lock = __import__('threading').Lock()

def send_request(i):
    global success, failed
    try:
        r = requests.post(TARGET_URL, json=payload, headers=headers, timeout=5)
        with lock:
            global success
            success += 1
            if i % 100 == 0:
                print(f"Request {i}: {r.status_code}")
    except Exception as e:
        with lock:
            global failed
            failed += 1

print(f"Starting HTTP flood — {TOTAL_REQUESTS} requests, {THREADS} threads")
print("Make sure Wireshark is capturing on loopback with filter: tcp.port == 8080")
input("Press ENTER when Wireshark is ready and capturing...")

start = time.time()

with concurrent.futures.ThreadPoolExecutor(max_workers=THREADS) as executor:
    executor.map(send_request, range(TOTAL_REQUESTS))

elapsed = time.time() - start
print(f"\nDone! {success} succeeded, {failed} failed in {elapsed:.2f} seconds")
print(f"Rate: {TOTAL_REQUESTS/elapsed:.0f} requests/second")
print("\nNow stop Wireshark and save as: attacks/http_flood.pcapng")