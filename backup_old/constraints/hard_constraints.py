# constraints/hard_constraints.py

from data.sample_data import ROOMS, COURSES

def validate_hard_constraints(timetable):
    """
    Kiểm tra các ràng buộc cứng (HC01 - HC06) cho một phương án thời khóa biểu.
    
    Cấu trúc của một cá thể thời khóa biểu (timetable):
    [
        {"course_id": "AI101_01", "slot_id": "T2_1", "room_id": "P101", "teacher_id": "GV01"},
        ...
    ]
    """
    violations = []
    
    room_dict = {r["room_id"]: r for r in ROOMS}
    course_dict = {c["course_id"]: c for c in COURSES}
    
    teacher_schedule = {}     # Key: (teacher_id, slot_id)
    room_schedule = {}        # Key: (room_id, slot_id)
    course_session_count = {} # Key: course_id

    for item in timetable:
        c_id = item["course_id"]
        s_id = item["slot_id"]
        r_id = item["room_id"]
        t_id = item["teacher_id"]
        
        # Đếm số tiết đã xếp cho môn học (dùng cho HC06)
        course_session_count[c_id] = course_session_count.get(c_id, 0) + 1
        
        # Ghi nhận lịch giảng viên (HC01)
        t_key = (t_id, s_id)
        if t_key not in teacher_schedule:
            teacher_schedule[t_key] = []
        teacher_schedule[t_key].append(c_id)
        
        # Ghi nhận lịch phòng học (HC02)
        r_key = (r_id, s_id)
        if r_key not in room_schedule:
            room_schedule[r_key] = []
        room_schedule[r_key].append(c_id)
        
        # Kiểm tra HC04 & HC05
        room_info = room_dict.get(r_id)
        course_info = course_dict.get(c_id)
        
        if room_info and course_info:
            # HC04: Sức chứa phòng học phải đủ
            if room_info["capacity"] < course_info["num_students"]:
                violations.append(f"HC04 Vi phạm: Phòng {r_id} (chứa {room_info['capacity']}) không đủ cho lớp {c_id} ({course_info['num_students']} SV)")
            
            # HC05: Phòng học phải đúng loại (Lý thuyết / Thực hành)
            if room_info["type"] != course_info["required_room_type"]:
                violations.append(f"HC05 Vi phạm: Lớp {c_id} cần phòng {course_info['required_room_type']} nhưng lại xếp vào phòng {room_info['type']} ({r_id})")

    # Kiểm tra HC01: Giảng viên không được dạy 2 lớp cùng khung giờ
    for (t_id, s_id), c_list in teacher_schedule.items():
        if len(c_list) > 1:
            violations.append(f"HC01 Vi phạm: Giảng viên {t_id} bị trùng lịch dạy các lớp {c_list} tại khung giờ {s_id}")

    # Kiểm tra HC02: Phòng học không được xếp 2 lớp cùng khung giờ
    for (r_id, s_id), c_list in room_schedule.items():
        if len(c_list) > 1:
            violations.append(f"HC02 Vi phạm: Phòng {r_id} bị trùng lịch xếp cho các lớp {c_list} tại khung giờ {s_id}")

    # Kiểm tra HC06: Môn học phải được xếp đủ số tiết quy định
    for c_id, req_course in course_dict.items():
        actual_sessions = course_session_count.get(c_id, 0)
        if actual_sessions != req_course["total_sessions"]:
            violations.append(f"HC06 Vi phạm: Môn {c_id} xếp {actual_sessions} tiết (Yêu cầu: {req_course['total_sessions']} tiết)")

    # Trả về kết quả: True nếu không có lỗi, False nếu có lỗi kèm danh sách vi phạm
    is_valid = len(violations) == 0
    return is_valid, violations