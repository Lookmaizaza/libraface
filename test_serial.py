import serial

try:
    ser = serial.Serial('COM3', 115200, timeout=1)
    print("✅ Connected to COM3")
    ser.write(b"TEST\n")
    ser.close()
except Exception as e:
    print(f"❌ Error: {e}")