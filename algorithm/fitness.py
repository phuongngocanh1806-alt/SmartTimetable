# algorithm/fitness.py

# Nhập hàm kiểm tra ràng buộc cứng từ code của Thành viên 1
from constraints.hard_constraints import validate_hard_constraints
from constraints.soft_constraints import SoftConstraintEvaluator

def calculate_fitness(chromosome):
    """
    HÀM TÍNH ĐIỂM FITNESS CHÍNH:
    - Nhận vào đối tượng Chromosome.
    - Kiểm tra ràng buộc cứng -> Vi phạm trả về 0.0 điểm.
    - Hợp lệ -> Tính điểm ràng buộc mềm (tối đa 100.0 điểm) để thuật toán GA dùng max().
    """
    # Trích xuất danh sách schedule linh hoạt từ chromosome
    raw_schedule = getattr(chromosome, "schedule", chromosome if isinstance(chromosome, list) else [])

    # Chuẩn hóa dữ liệu để khớp với đầu vào của hàm validate_hard_constraints (Thành viên 1)
    normalized_timetable = []
    for item in raw_schedule:
        room_obj = item.get("room", {})
        room_id = room_obj.get("room_id") if isinstance(room_obj, dict) else str(room_obj)

        slot_obj = item.get("timeslot", item.get("slot_id", ""))
        if isinstance(slot_obj, dict):
            slot_id = slot_obj.get("slot_id", slot_obj.get("id", str(slot_obj)))
        else:
            slot_id = str(slot_obj)

        normalized_timetable.append({
            "course_id": item.get("course_id"),
            "slot_id": slot_id,
            "room_id": room_id,
            "teacher_id": item.get("teacher_id")
        })

    # 1. Chốt chặn ràng buộc cứng (Thành viên 1)
    is_valid, _ = validate_hard_constraints(normalized_timetable)
    if not is_valid:
        return 0.0  # Vi phạm ràng buộc cứng -> Nhận 0 điểm tuyệt đối

    # 2. Chấm điểm ràng buộc mềm (Thành viên 3)
    evaluator = SoftConstraintEvaluator()
    soft_counts = evaluator.evaluate_soft_constraints(normalized_timetable)
    
    total_penalty = sum(soft_counts[sc] * evaluator.weights[sc] for sc in soft_counts)
    fitness_score = max(0.0, 100.0 - total_penalty)

    return round(fitness_score, 2)