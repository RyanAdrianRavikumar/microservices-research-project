import grpc
import concurrent.futures
import time
import inventory_pb2
import inventory_pb2_grpc

TARGET = "localhost:9090"
CHANNELS = 50
REQUESTS_PER_CHANNEL = 100

def abuse_channel(channel_id):
    success = 0
    failed = 0
    try:
        channel = grpc.insecure_channel(TARGET)
        stub = inventory_pb2_grpc.InventoryServiceStub(channel)
        for i in range(REQUESTS_PER_CHANNEL):
            try:
                # Send oversized item name to stress the service
                request = inventory_pb2.CheckStockRequest(
                    item_name="FLOOD_" + "X" * 500 + f"_{channel_id}_{i}"
                )
                response = stub.CheckStock(request, timeout=10)
                success += 1
            except Exception:
                failed += 1
        channel.close()
    except Exception as e:
        print(f"Channel {channel_id} error: {e}")
    return success, failed

print(f"Starting gRPC stream abuse — {CHANNELS} channels x {REQUESTS_PER_CHANNEL} requests")
print(f"Total requests: {CHANNELS * REQUESTS_PER_CHANNEL}")
print("Make sure Wireshark is capturing on loopback with filter: tcp.port == 9090")
input("Press ENTER when Wireshark is ready and capturing...")

start = time.time()
total_success = 0
total_failed = 0

with concurrent.futures.ThreadPoolExecutor(max_workers=CHANNELS) as executor:
    results = list(executor.map(abuse_channel, range(CHANNELS)))

for s, f in results:
    total_success += s
    total_failed += f

elapsed = time.time() - start
print(f"\nDone! {total_success} succeeded, {total_failed} failed in {elapsed:.2f} seconds")
print("\nNow stop Wireshark and save as: attacks/grpc_abuse.pcapng")