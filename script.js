let lastStudentId = null;

function fetchStudentInfo() {
    fetch('/student_info')
        .then(response => response.json())
        .then(data => {
            if (data.name && data.id && data.id !== lastStudentId) {
                // แสดงข้อมูลนักเรียน
                document.getElementById('name').innerText = data.name;
                document.getElementById('id').innerText = data.id;
                document.getElementById('major').innerText = data.major;
                document.getElementById('attendance').innerText = data.total_attendance;

                const now = new Date();
                const timeString = now.toLocaleTimeString();
                document.getElementById('checkin_time').innerText = timeString;

                lastStudentId = data.id;
            } else if (data.name === "not found") {
                // ไม่รู้จักใบหน้า
                document.getElementById('name').innerText = "not found";
                document.getElementById('id').innerText = "-";
                document.getElementById('major').innerText = "-";
                document.getElementById('attendance').innerText = "-";
                document.getElementById('checkin_time').innerText = "-";
                lastStudentId = null;
            } else if (!data.name) {
                // ไม่พบใบหน้าใดๆ
                document.getElementById('name').innerText = "No face detected";
                document.getElementById('id').innerText = "-";
                document.getElementById('major').innerText = "-";
                document.getElementById('attendance').innerText = "-";
                document.getElementById('checkin_time').innerText = "-";
                lastStudentId = null;
            }
        })
        .catch(error => console.error('Error fetching student info:', error));
}

// Auto update every 2 seconds
setInterval(fetchStudentInfo, 2000);