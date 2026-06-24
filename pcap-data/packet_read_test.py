import pyshark

cap = pyshark.FileCapture("normal/rest_normal.pcapng")

count = 0
for pkt in cap:
    count += 1
    print(pkt)
    if count == 5:
        break

cap.close()

print("PACKETS:", count)