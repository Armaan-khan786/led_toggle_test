@echo off
echo ================================
echo Build and Flash ESP32 Projects
echo ================================

REM --- Sender ---
echo ----- Compiling Sender -----
arduino-cli compile --fqbn esp32:esp32:esp32 sender/sender.ino
if %errorlevel% neq 0 (
    echo Compilation failed for Sender. Exiting...
    pause
    exit /b %errorlevel%
)

echo ----- Uploading Sender to COM6 -----
arduino-cli upload -p COM6 --fqbn esp32:esp32:esp32 sender/sender.ino
if %errorlevel% neq 0 (
    echo Upload failed for Sender. Exiting...
    pause
    exit /b %errorlevel%
)

REM --- Receiver ---
echo ----- Compiling Receiver -----
arduino-cli compile --fqbn esp32:esp32:esp32 receiver/receiver.ino
if %errorlevel% neq 0 (
    echo Compilation failed for Receiver. Exiting...
    pause
    exit /b %errorlevel%
)

echo ----- Uploading Receiver to COM7 -----
arduino-cli upload -p COM7 --fqbn esp32:esp32:esp32 receiver/receiver.ino
if %errorlevel% neq 0 (
    echo Upload failed for Receiver. Exiting...
    pause
    exit /b %errorlevel%
)

REM --- Start Monitoring ---
echo ===== Starting Monitor =====
python monitor.py

pause
