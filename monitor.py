import serial
import time
import sys

# ------------------------------
# CONFIGURATION
# ------------------------------
COM_PORT = "COM6"        # replace with your actual ESP32 port
BAUD_RATE = 115200       # same as in Arduino sketch
TIMEOUT = 0.1            # serial read timeout
MAX_TOGGLES = 20         # how many toggles to count before ending

# ------------------------------
# INITIALIZATION
# ------------------------------
try:
    ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=TIMEOUT)
    print(f"[INFO] Connected to {COM_PORT}")
except Exception as e:
    print(f"[ERROR] Cannot open serial port {COM_PORT}: {e}")
    sys.exit(1)

sender_count = 0
receiver_count = 0
prev_sender = None
prev_receiver = None
toggle_limit = MAX_TOGGLES

start_time = time.time()

# ------------------------------
# MONITOR LOOP
# ------------------------------
while True:
    if time.time() - start_time > 30:  # 30s timeout
        print("[ERROR] Timeout reached")
        break

    try:
        line = ser.readline().decode('utf-8').strip()
        if not line:
            continue

        # Debug: print all incoming lines
        print(line)

        # Detect sender toggles
        if "[SENDER]" in line:
            value = line.split()[-1]
            if prev_sender is not None and value != prev_sender:
                sender_count += 1
            prev_sender = value

        # Detect receiver toggles
        if "[RECEIVER]" in line:
            value = line.split()[-1]
            if prev_receiver is not None and value != prev_receiver:
                receiver_count += 1
            prev_receiver = value

        # Stop after enough toggles
        if sender_count >= toggle_limit and receiver_count >= toggle_limit:
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
print(f"[RESULT] Sender Toggles: {sender_count}")
print(f"[RESULT] Receiver Toggles: {receiver_count}")

if sender_count == 0 or receiver_count == 0:
    print("[FAIL] Toggle test failed.")
    sys.exit(1)
else:
    print("[PASS] Toggle test passed.")
    sys.exit(0)
