from flask import Flask, render_template, Response, jsonify
import cv2
import face_recognition
import pickle
import numpy as np
import firebase_admin
from firebase_admin import credentials, db, storage
from datetime import datetime
import serial
import time

app = Flask(__name__)

# Serial config
SERIAL_PORT = 'COM3'
BAUD_RATE = 9600
ser = None

def init_serial():
    global ser
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)
        print(f"✅ Connected to {SERIAL_PORT}")
    except Exception as e:
        print(f"❌ Could not connect to {SERIAL_PORT}: {e}")
        ser = None

init_serial()

# Firebase init
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendancerealtime-3a71a-default-rtdb.asia-southeast1.firebasedatabase.app/",
    'storageBucket': "faceattendancerealtime-3a71a.appspot.com"
})

bucket = storage.bucket()
cap = cv2.VideoCapture(0)

# Load encodings
with open('EncodeFile.p', 'rb') as file:
    encodeListKnown, studentIds = pickle.load(file)

# Globals
currentStudentInfo = {}
face_detected = False

def control_led(state):
    """Send LED control command to ESP32"""
    if ser is not None and ser.is_open:
        try:
            ser.write(f'{state}\n'.encode())  # ส่ง 1 หรือ 0 ตามต้องการ
            print(f"[INFO] Sent to ESP32: {state}")
        except serial.SerialException:
            print("[ERROR] Failed to send data to ESP32.")
    else:
        print("[WARNING] Serial not available.")

def gen_frames():
    global currentStudentInfo, face_detected
    while True:
        success, img = cap.read()
        if not success:
            break
        else:
            imgS = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            faceCurFrame = face_recognition.face_locations(imgS)
            encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

            if not faceCurFrame:
                if face_detected:
                    face_detected = False
                    control_led(1)  # ✅ ไม่เจอหน้า → เปิดไฟ
                currentStudentInfo = {}
            else:
                recognized = False
                for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
                    matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                    faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                    matchIndex = np.argmin(faceDis)

                    if matches[matchIndex]:
                        recognized = True
                        id = studentIds[matchIndex]
                        studentInfo = db.reference(f'Students/{id}').get()

                        if studentInfo:
                            datetimeObject = datetime.strptime(studentInfo['last_attendance_time'], "%Y-%m-%d %H:%M:%S")
                            secondsElapsed = (datetime.now() - datetimeObject).total_seconds()

                            if secondsElapsed > 30:
                                ref = db.reference(f'Students/{id}')
                                studentInfo['total_attendance'] += 1
                                ref.child('total_attendance').set(studentInfo['total_attendance'])
                                ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

                            currentStudentInfo = {
                                "id": id,
                                "name": studentInfo['name'],
                                "major": studentInfo['major'],
                                "total_attendance": studentInfo['total_attendance'],
                            }

                            if not face_detected:
                                face_detected = True
                                control_led(0)  # ✅ เจอหน้า → ปิดไฟ
                        break

                if not recognized:
                    if face_detected:
                        face_detected = False
                        control_led(1)  # ✅ ถ้าไม่รู้จัก → เปิดไฟ
                    currentStudentInfo = {"name": "not found"}

            ret, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/student_info')
def student_info():
    return jsonify(currentStudentInfo)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)