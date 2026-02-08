@echo off
setlocal enabledelayedexpansion

REM ================= CONFIG =================
set FQBN=esp32:esp32:esp32
set SENDER_PORT=COM6
set RECEIVER_PORT=COM7
set BAUD=115200
set SENDER_PATH=sender
set RECEIVER_PATH=receiver
set TIMEOUT_SECONDS=8
set LOGFILE=serial_log.txt
REM ==========================================

echo ==========================================
echo      ESP32 DUAL BOARD LED TOGGLE TEST
echo ==========================================

REM ---------- 1. COMPILE SENDER ----------
echo.
echo [STEP 1] Compiling Sender...
arduino-cli compile --fqbn %FQBN% %SENDER_PATH%
if errorlevel 1 (
    echo ❌ FAILURE: Sender Compilation Error
    exit /b 1
)
echo ✅ Sender Compile OK

REM ---------- 2. COMPILE RECEIVER ----------
echo.
echo [STEP 2] Compiling Receiver...
arduino-cli compile --fqbn %FQBN% %RECEIVER_PATH%
if errorlevel 1 (
    echo ❌ FAILURE: Receiver Compilation Error
    exit /b 1
)
echo ✅ Receiver Compile OK

REM ---------- 3. UPLOAD SENDER ----------
echo.
echo [STEP 3] Uploading Sender to %SENDER_PORT% ...
arduino-cli upload -p %SENDER_PORT% --fqbn %FQBN% %SENDER_PATH%
if errorlevel 1 (
    echo ❌ FAILURE: Sender Upload Failed (Check COM6)
    exit /b 1
)
echo ✅ Sender Upload OK

REM ---------- 4. UPLOAD RECEIVER ----------
echo.
echo [STEP 4] Uploading Receiver to %RECEIVER_PORT% ...
arduino-cli upload -p %RECEIVER_PORT% --fqbn %FQBN% %RECEIVER_PATH%
if errorlevel 1 (
    echo ❌ FAILURE: Receiver Upload Failed (Check COM7)
    exit /b 1
)
echo ✅ Receiver Upload OK

REM ---------- 5. SERIAL CAPTURE ----------
echo.
echo [STEP 5] Capturing Receiver Serial Output...

if exist %LOGFILE% del %LOGFILE%

powershell -Command ^
"try { ^
$port = new-Object System.IO.Ports.SerialPort '%RECEIVER_PORT%',%BAUD%,None,8,one; ^
$port.Open(); ^
Start-Sleep -Seconds %TIMEOUT_SECONDS%; ^
$data = $port.ReadExisting(); ^
$port.Close(); ^
$data | Out-File -Encoding ASCII '%LOGFILE%'; ^
} catch { ^
'ERROR_OPENING_SERIAL' | Out-File '%LOGFILE%'; ^
}"

if not exist %LOGFILE% (
    echo ❌ FAILURE: Serial Log Not Created
    exit /b 1
)

echo.
echo ===== RECEIVER SERIAL OUTPUT =====
type %LOGFILE%
echo ===================================

findstr "ERROR_OPENING_SERIAL" %LOGFILE% >nul
if %errorlevel%==0 (
    echo ❌ FAILURE: Could Not Open COM7
    exit /b 1
)

for %%A in (%LOGFILE%) do set SIZE=%%~zA
if %SIZE%==0 (
    echo ❌ FAILURE: No Serial Data Received From Receiver
    exit /b 1
)

REM ---------- 6. VALIDATE TOGGLE ----------
findstr "HIGH" %LOGFILE% >nul
set HIGH_FOUND=%errorlevel%

findstr "LOW" %LOGFILE% >nul
set LOW_FOUND=%errorlevel%

echo.
echo [STEP 6] Validating Toggle...

if %HIGH_FOUND%==0 if %LOW_FOUND%==0 (
    echo.
    echo ✅ TEST PASS: Sender COM6 toggling detected on Receiver COM7
    exit /b 0
)

if %HIGH_FOUND%==0 if not %LOW_FOUND%==0 (
    echo ❌ FAILURE: Only HIGH detected (No LOW toggling)
    exit /b 1
)

if %LOW_FOUND%==0 if not %HIGH_FOUND%==0 (
    echo ❌ FAILURE: Only LOW detected (No HIGH toggling)
    exit /b 1
)

echo ❌ FAILURE: Neither HIGH nor LOW detected
exit /b 1