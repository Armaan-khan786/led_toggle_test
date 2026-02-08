import serial
import time
import sys

PORT = "COM7"
BAUD = 115200
EXPECTED_MIN_PERIOD = 0.8   # seconds
EXPECTED_MAX_PERIOD = 1.2   # seconds
MIN_TOGGLES = 5
TIMEOUT = 15  # seconds total test duration

print("Opening serial port:", PORT)

try:
    ser = serial.Serial(PORT, BAUD, timeout=1)
except Exception as e:
    print("❌ FAILURE: Cannot open serial port:", e)
    sys.exit(1)

start_time = time.time()
last_state = None
last_toggle_time = None
periods = []
toggle_count = 0

print("Listening for HIGH/LOW...")

while time.time() - start_time < TIMEOUT:
    try:
        line = ser.readline().decode().strip()
    except:
        continue

    if line not in ["HIGH", "LOW"]:
        continue

    current_time = time.time()

    if last_state is None:
        last_state = line
        last_toggle_time = current_time
        continue

    if line != last_state:
        toggle_count += 1
        period = current_time - last_toggle_time
        periods.append(period)
        print(f"Toggle {toggle_count} detected. Period: {period:.3f} sec")
        last_toggle_time = current_time
        last_state = line

    if toggle_count >= MIN_TOGGLES:
        break

ser.close()

print("\n========== ANALYSIS ==========")

if toggle_count < MIN_TOGGLES:
    print(f"❌ FAILURE: Only {toggle_count} toggles detected (Minimum required {MIN_TOGGLES})")
    sys.exit(1)

avg_period = sum(periods) / len(periods)
print(f"Average Period: {avg_period:.3f} sec")

if avg_period < EXPECTED_MIN_PERIOD:
    print("❌ FAILURE: Blink too fast")
    sys.exit(1)

if avg_period > EXPECTED_MAX_PERIOD:
    print("❌ FAILURE: Blink too slow")
    sys.exit(1)

print("✅ TEST PASS: Toggle timing within expected range")
sys.exit(0)
