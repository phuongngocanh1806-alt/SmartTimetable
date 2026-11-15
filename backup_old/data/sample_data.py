# data/sample_data.py

# 1. Khung giờ học trong tuần (Time Slots)
TIME_SLOTS = [
    {"slot_id": "T2_1", "day": "Thứ 2", "period": 1},
    {"slot_id": "T2_2", "day": "Thứ 2", "period": 2},
    {"slot_id": "T3_1", "day": "Thứ 3", "period": 1},
    {"slot_id": "T3_2", "day": "Thứ 3", "period": 2},
    {"slot_id": "T4_1", "day": "Thứ 4", "period": 1},
    {"slot_id": "T4_2", "day": "Thứ 4", "period": 2},
    {"slot_id": "T5_1", "day": "Thứ 5", "period": 1},
    {"slot_id": "T5_2", "day": "Thứ 5", "period": 2},
    {"slot_id": "T6_1", "day": "Thứ 6", "period": 1},
    {"slot_id": "T6_2", "day": "Thứ 6", "period": 2},
]

# 2. Danh sách phòng học (Rooms)
ROOMS = [
    {"room_id": "P101", "capacity": 50, "type": "LyThuyet"},
    {"room_id": "P102", "capacity": 40, "type": "LyThuyet"},
    {"room_id": "LAB01", "capacity": 30, "type": "ThucHanh"},
]

# 3. Danh sách giảng viên (Teachers)
TEACHERS = [
    {"teacher_id": "GV01", "name": "Nguyễn Văn A"},
    {"teacher_id": "GV02", "name": "Trần Thị B"},
    {"teacher_id": "GV03", "name": "Lê Văn C"},
]

# 4. Danh sách lớp học phần cần xếp lịch (Courses / Classes)
COURSES = [
    {
        "course_id": "AI101_01",
        "subject_name": "Trí tuệ nhân tạo",
        "teacher_id": "GV01",
        "num_students": 45,
        "required_room_type": "LyThuyet",
        "total_sessions": 2  # Số tiết/buổi cần học trong tuần (HC06)
    },
    {
        "course_id": "DB102_01",
        "subject_name": "Cơ sở dữ liệu",
        "teacher_id": "GV02",
        "num_students": 25,
        "required_room_type": "ThucHanh",
        "total_sessions": 2
    },
    {
        "course_id": "SE103_01",
        "subject_name": "Công nghệ phần mềm",
        "teacher_id": "GV03",
        "num_students": 35,
        "required_room_type": "LyThuyet",
        "total_sessions": 2
    }
]