import serial
import time
import sys

# ------------------------------
# CONFIGURATION
# ------------------------------
COM_PORT = "COM7"        # Receiver ESP32 port
BAUD_RATE = 115200
TIMEOUT = 0.1
MAX_TOGGLES = 20

# ------------------------------
# INITIALIZATION
# ------------------------------
try:
    ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=TIMEOUT)
    print(f"[INFO] Connected to {COM_PORT}")
    time.sleep(2)   # allow ESP32 to reset and start printing
except Exception as e:
    print(f"[ERROR] Cannot open serial port {COM_PORT}: {e}")
    sys.exit(1)

receiver_count = 0
prev_receiver = None
toggle_limit = MAX_TOGGLES

start_time = time.time()

# ------------------------------
# MONITOR LOOP
# ------------------------------
while True:
    if time.time() - start_time > 60:   # increased timeout
        print("[ERROR] Timeout reached")
        break

    try:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        if not line:
            continue

        # Print incoming serial data
        print(line)

        # Detect receiver toggles
        if "[RECEIVER]" in line:
            value = line.split()[-1]
            if prev_receiver is not None and value != prev_receiver:
                receiver_count += 1
            prev_receiver = value

        # Stop after enough toggles
        if receiver_count >= toggle_limit:
            break

    except KeyboardInterrupt:
        print("[INFO] Monitor stopped by user")
        break
    except Exception as e:
        print(f"[ERROR] {e}")

ser.close()

# ------------------------------
# RESULT
# ------------------------------
print(f"[RESULT] Receiver Toggles: {receiver_count}")

if receiver_count == 0:
    print("[FAIL] Toggle test failed.")
    sys.exit(1)
else:
    print("[PASS] Toggle test passed.")
    sys.exit(0)
