import serial
import time
import sys

# === CONFIGURE PORTS & SETTINGS ===
SENDER_PORT = "COM6"      # Set your sender COM port
RECEIVER_PORT = "COM7"    # Set your receiver COM port
BAUD_RATE = 115200
TOGGLE_COUNT_REQUIRED = 5
TIMEOUT = 10  # seconds to wait for toggles

# === HELPER FUNCTION ===
def monitor_port(port_name):
    try:
        ser = serial.Serial(port_name, BAUD_RATE, timeout=1)
        print(f"[INFO] Connected to {port_name}")
        return ser
    except Exception as e:
        print(f"[ERROR] Cannot open {port_name}: {e}")
        return None

def check_toggle(ser, label):
    toggle_count = 0
    start_time = time.time()
    while time.time() - start_time < TIMEOUT:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line:
                print(f"[{label}] {line}")
                if "TOGGLE" in line.upper():  # Your ESP prints "TOGGLE"
                    toggle_count += 1
        if toggle_count >= TOGGLE_COUNT_REQUIRED:
            break
    return toggle_count

# === MAIN MONITOR ===
def main():
    sender = monitor_port(SENDER_PORT)
    receiver = monitor_port(RECEIVER_PORT)

    if sender is None or receiver is None:
        print("[ERROR] Failed to open COM ports")
        sys.exit(1)

    print("[INFO] Monitoring sender for toggles...")
    sender_toggles = check_toggle(sender, "SENDER")

    print("[INFO] Monitoring receiver for toggles...")
    receiver_toggles = check_toggle(receiver, "RECEIVER")

    print(f"[RESULT] Sender Toggles: {sender_toggles}")
    print(f"[RESULT] Receiver Toggles: {receiver_toggles}")

    sender.close()
    receiver.close()

    if sender_toggles >= TOGGLE_COUNT_REQUIRED and receiver_toggles >= TOGGLE_COUNT_REQUIRED:
        print("[PASS] Both Sender and Receiver toggled correctly!")
        sys.exit(0)
    else:
        print("[FAIL] Toggle test failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
