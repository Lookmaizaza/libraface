import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendancerealtime-3a71a-default-rtdb.asia-southeast1.firebasedatabase.app/",
    'storageBucket': "faceattendancerealtime-3a71a.firebasestorage.app"
})

ref = db.reference('Students')

data = {
    "321654":
        {
            "name": "Murtaza Hassan",
            "major": "Robotics",
            "starting_year": 2017,
            "total_attendance": 7,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "852741":
        {
            "name": "Emly Blunt",
            "major": "Economics",
            "starting_year": 2021,
            "total_attendance": 12,
            "standing": "B",
            "year": 1,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "963852":
        {
            "name": "Elon Musk",
            "major": "Physics",
            "starting_year": 2020,
            "total_attendance": 7,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "661364":
        {
            "name": "Lookmai K",
            "major": "AI",
            "starting_year": 2024,
            "total_attendance": 10,
            "standing": "B",
            "year": 1,
            "last_attendance_time": "2025-3-11 12:54:34"
        },
    "661537":
        {
            "name": "Apasita Pasukree",
            "major": "AI",
            "starting_year": 2025,
            "total_attendance": 5,
            "standing": "A",
            "year": 2,
            "last_attendance_time": "2025-4-11 13:54:34"
        }
}

for key, value in data.items():
    ref.child(key).set(value)