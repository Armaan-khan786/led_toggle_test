import serial
import time
import sys

COM_PORT = "COM7"
BAUD_RATE = 115200
TIMEOUT = 0.2
MAX_TOGGLES = 10

try:
    ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=TIMEOUT)
    print(f"[INFO] Connected to {COM_PORT}")
    time.sleep(8)
    ser.reset_input_buffer()
except Exception as e:
    print(f"[ERROR] Cannot open serial port {COM_PORT}: {e}")
    sys.exit(1)

receiver_count = 0
prev_value = None
start_time = time.time()

while True:
    if time.time() - start_time > 60:
        print("[ERROR] Timeout reached")
        break

    line = ser.readline().decode('utf-8', errors='ignore').strip()
    if not line:
        continue

    print(line)

    if "[RECEIVER]" in line:
        value = line.split()[-1]

        if prev_value is not None and value != prev_value:
            receiver_count += 1

        prev_value = value

    if receiver_count >= MAX_TOGGLES:
        break

ser.close()

print(f"[RESULT] Receiver Toggles: {receiver_count}")

if receiver_count == 0:
    print("[FAIL] Toggle test failed.")
    sys.exit(1)
else:
    print("[PASS] Toggle test passed.")
    sys.exit(0)
