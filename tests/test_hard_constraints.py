# test_member1.py
from constraints.hard_constraints import validate_hard_constraints

# Lịch thử nghiệm 1: HỢP LỆ (Không vi phạm gì)
valid_timetable = [
    {"course_id": "AI101_01", "slot_id": "T2_1", "room_id": "P101", "teacher_id": "GV01"},
    {"course_id": "AI101_01", "slot_id": "T2_2", "room_id": "P101", "teacher_id": "GV01"},
    {"course_id": "DB102_01", "slot_id": "T3_1", "room_id": "LAB01", "teacher_id": "GV02"},
    {"course_id": "DB102_01", "slot_id": "T3_2", "room_id": "LAB01", "teacher_id": "GV02"},
    {"course_id": "SE103_01", "slot_id": "T4_1", "room_id": "P102", "teacher_id": "GV03"},
    {"course_id": "SE103_01", "slot_id": "T4_2", "room_id": "P102", "teacher_id": "GV03"},
]

# Lịch thử nghiệm 2: CỐ TÌNH VI PHẠM (Dạy trùng giờ HC01 & Sai loại phòng HC05)
invalid_timetable = [
    {"course_id": "AI101_01", "slot_id": "T2_1", "room_id": "P101", "teacher_id": "GV01"},
    # GV01 bị trùng lịch ở T2_1, đồng thời AI101_01 bị xếp vào phòng LAB01 sai loại phòng
    {"course_id": "AI101_01", "slot_id": "T2_1", "room_id": "LAB01", "teacher_id": "GV01"},
]

print("--- KIỂM THỬ LỊCH HỢP LỆ ---")
is_valid, errors = validate_hard_constraints(valid_timetable)
print("Hợp lệ:", is_valid)
print("Số lỗi:", len(errors))

print("\n--- KIỂM THỬ LỊCH VI PHẠM ---")
is_valid, errors = validate_hard_constraints(invalid_timetable)
print("Hợp lệ:", is_valid)
print("Danh sách lỗi phát hiện được:")
for err in errors:
    print("-", err)