# test_hard_constraints.py
from constraints.hard_constraints import validate_hard_constraints

# Lịch thử nghiệm 1: HỢP LỆ (Không vi phạm ràng buộc cứng nào)
valid_timetable = [
    {"course_id": "AI101_01", "slot_id": "T2_1", "room_id": "P101", "teacher_id": "GV01"},
    {"course_id": "AI101_01", "slot_id": "T2_2", "room_id": "P101", "teacher_id": "GV01"},
    {"course_id": "DB102_01", "slot_id": "T3_1", "room_id": "LAB01", "teacher_id": "GV02"},
    {"course_id": "DB102_01", "slot_id": "T3_2", "room_id": "LAB01", "teacher_id": "GV02"},
    {"course_id": "SE103_01", "slot_id": "T4_1", "room_id": "P102", "teacher_id": "GV03"},
    {"course_id": "SE103_01", "slot_id": "T4_2", "room_id": "P102", "teacher_id": "GV03"},
]

# Lịch thử nghiệm 2: CỐ TÌNH VI PHẠM (Trùng lịch giảng viên HC01 & Sai loại phòng HC05)
invalid_timetable = [
    {"course_id": "AI101_01", "slot_id": "T2_1", "room_id": "P101", "teacher_id": "GV01"},
    # Cố tình xếp trùng GV01 ở khung giờ T2_1 và xếp sai phòng LAB01 cho môn lý thuyết
    {"course_id": "AI101_01", "slot_id": "T2_1", "room_id": "LAB01", "teacher_id": "GV01"},
]

print("=== KIỂM THỬ 1: LỊCH HỢP LỆ ===")
is_valid, errors = validate_hard_constraints(valid_timetable)
print("Kết quả hợp lệ:", is_valid)
print("Số lỗi phát hiện:", len(errors))

print("\n=== KIỂM THỬ 2: LỊCH VI PHẠM ===")
is_valid, errors = validate_hard_constraints(invalid_timetable)
print("Kết quả hợp lệ:", is_valid)
print("Danh sách lỗi phát hiện được:")
for err in errors:
    print("-", err)