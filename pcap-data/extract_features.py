import subprocess
import pandas as pd
import os

TSHARK = r"C:\Program Files\Wireshark\tshark.exe"

# Fields to extract — maps directly to tshark field names
FIELDS = [
    "frame.time_epoch",
    "frame.len",
    "tcp.dstport",
    "tcp.srcport",
    "tcp.flags.syn",
    "tcp.flags.fin",
    "tcp.flags.push",
    "tcp.flags.ack",
]

def extract_with_tshark(pcap_path, label, is_attack):
    if not os.path.exists(pcap_path):
        print(f"  ERROR: File not found: {pcap_path}")
        return pd.DataFrame()

    print(f"Processing: {pcap_path}")

    # Build tshark command
    cmd = [TSHARK, "-r", pcap_path, "-T", "fields", "-E", "header=y", "-E", "separator=,", "-E", "quote=d", "-E", "occurrence=f"]
    for field in FIELDS:
        cmd += ["-e", field]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

        if result.returncode != 0:
            print(f"  tshark error: {result.stderr[:200]}")
            return pd.DataFrame()

        # Parse output
        lines = result.stdout.strip().split('\n')
        if len(lines) < 2:
            print(f"  No data returned")
            return pd.DataFrame()

        # Write to temp CSV and read with pandas
        temp_csv = f"temp_{label}.csv"
        with open(temp_csv, 'w') as f:
            f.write(result.stdout)

        df = pd.read_csv(temp_csv, low_memory=False)
        os.remove(temp_csv)

        # Rename columns
        df.columns = [
            "timestamp", "packet_length", "dst_port", "src_port",
            "tcp_flag_syn", "tcp_flag_fin", "tcp_flag_psh", "tcp_flag_ack"
        ]

        # Clean up — drop rows with no timestamp (non-TCP packets)
        df = df.dropna(subset=["timestamp", "packet_length"])
        df["timestamp"]     = pd.to_numeric(df["timestamp"],     errors="coerce")
        df["packet_length"] = pd.to_numeric(df["packet_length"], errors="coerce")
        df["dst_port"]      = pd.to_numeric(df["dst_port"],      errors="coerce").fillna(0).astype(int)
        df["src_port"]      = pd.to_numeric(df["src_port"],      errors="coerce").fillna(0).astype(int)
        df["tcp_flag_syn"]  = pd.to_numeric(df["tcp_flag_syn"],  errors="coerce").fillna(0).astype(int)
        df["tcp_flag_fin"]  = pd.to_numeric(df["tcp_flag_fin"],  errors="coerce").fillna(0).astype(int)
        df["tcp_flag_psh"]  = pd.to_numeric(df["tcp_flag_psh"],  errors="coerce").fillna(0).astype(int)
        df["tcp_flag_ack"]  = pd.to_numeric(df["tcp_flag_ack"],  errors="coerce").fillna(0).astype(int)
        df = df.dropna(subset=["timestamp", "packet_length"])

        # Calculate inter-arrival time
        df = df.sort_values("timestamp").reset_index(drop=True)
        df["inter_arrival_time"] = df["timestamp"].diff().fillna(0)

        # Add labels
        df["traffic_type"] = label
        df["is_attack"]    = is_attack

        print(f"  -> {len(df):,} packets extracted from {label}")
        return df

    except subprocess.TimeoutExpired:
        print(f"  ERROR: tshark timed out on {pcap_path}")
        return pd.DataFrame()
    except Exception as e:
        print(f"  ERROR: {e}")
        return pd.DataFrame()


# ── MAIN ──────────────────────────────────────────────────────────────────────

PCAP_FILES = [
    ("normal/rest_normal.pcapng",      "rest_normal",     0),
    ("normal/grpc_normal.pcapng",      "grpc_normal",     0),
    ("normal/rabbitmq_normal.pcapng",  "rabbitmq_normal", 0),
    ("attacks/http_flood.pcapng",      "http_flood",      1),
    ("attacks/slow_loris.pcapng",      "slow_loris",      1),
    ("attacks/grpc_abuse.pcapng",      "grpc_abuse",      1),
    ("attacks/queue_flood.pcapng",     "queue_flood",     1),
]

print("=" * 55)
print("FEATURE EXTRACTION VIA TSHARK")
print("=" * 55)

all_dfs = []
for path, label, is_attack in PCAP_FILES:
    df_temp = extract_with_tshark(path, label, is_attack)
    if not df_temp.empty:
        all_dfs.append(df_temp)

if not all_dfs:
    print("ERROR: No data extracted. Check your file paths.")
else:
    df = pd.concat(all_dfs, ignore_index=True)
    df.to_csv("traffic_features.csv", index=False)

    print()
    print("=" * 55)
    print(f"DONE — Total packets: {len(df):,}")
    print(f"Saved to: traffic_features.csv")
    print()
    print("Packets per traffic type:")
    for tt, count in df["traffic_type"].value_counts().items():
        attack_label = "ATTACK" if df[df["traffic_type"]==tt]["is_attack"].iloc[0]==1 else "NORMAL"
        print(f"  {tt:<25} {count:>7,}  [{attack_label}]")
    print()
    print("Class balance:")
    normal = (df["is_attack"]==0).sum()
    attack = (df["is_attack"]==1).sum()
    print(f"  Normal: {normal:,} ({normal/len(df)*100:.1f}%)")
    print(f"  Attack: {attack:,} ({attack/len(df)*100:.1f}%)")