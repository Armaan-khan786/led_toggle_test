echo Uploading Sender...
arduino-cli upload -p COM6 --fqbn esp32:esp32:esp32 sender\sender.ino
timeout /t 5

echo Uploading Receiver...
arduino-cli upload -p COM7 --fqbn esp32:esp32:esp32 receiver\receiver.ino
timeout /t 5

echo Starting Monitor Test...
python monitor.py
echo Monitor Exit Code: %ERRORLEVEL%

IF %ERRORLEVEL% NEQ 0 (
    echo TEST FAILED
    exit /b 1
)

echo TEST PASSED
exit /b 0
