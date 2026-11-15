# constraints/soft_constraints.py

class SoftConstraintEvaluator:
    def __init__(self, custom_weights=None):
        """
        Khởi tạo trọng số phạt cho các ràng buộc mềm (SC01 - SC06).
        """
        self.weights = custom_weights or {
            'SC01': 2.0,  # Hạn chế lịch học quá sớm
            'SC02': 3.0,  # Hạn chế lịch học vào buổi tối
            'SC03': 4.0,  # Hạn chế tiết trống giữa các buổi
            'SC04': 2.5,  # Phân bố lịch học đều trong tuần
            'SC05': 5.0,  # Ưu tiên khung giờ giảng viên mong muốn
            'SC06': 3.5   # Hạn chế học quá nhiều tiết liên tục
        }

    def evaluate_soft_constraints(self, timetable):
        """
        Đếm số lần vi phạm các ràng buộc mềm (SC01 - SC06).
        """
        counts = {
            'SC01': 0, 'SC02': 0, 'SC03': 0, 
            'SC04': 0, 'SC05': 0, 'SC06': 0
        }
        
        teacher_day_slots = {}

        for item in timetable:
            slot_id = str(item.get("slot_id", ""))
            teacher_id = item.get("teacher_id", "")
            
            # SC01: Lịch học quá sớm
            if "07:00" in slot_id or "_1" in slot_id:
                counts['SC01'] += 1

            # SC02: Lịch học buổi tối
            if "17:45" in slot_id or "21:00" in slot_id or "toi" in slot_id.lower():
                counts['SC02'] += 1

            # Tách chuỗi để check tiết trống (SC03) và tiết liên tục (SC06)
            parts = slot_id.split('_')
            if len(parts) >= 2:
                day = parts[0]
                try:
                    period = int(parts[1])
                except ValueError:
                    period = 1

                t_key = (teacher_id, day)
                if t_key not in teacher_day_slots:
                    teacher_day_slots[t_key] = []
                teacher_day_slots[t_key].append(period)

        for t_key, periods in teacher_day_slots.items():
            periods.sort()
            
            # SC03: Tiết trống giữa các buổi trong ngày
            for i in range(len(periods) - 1):
                if periods[i+1] - periods[i] > 1:
                    counts['SC03'] += 1

            # SC06: Học quá nhiều tiết liên tục (> 4 tiết)
            consecutive = 1
            for i in range(len(periods) - 1):
                if periods[i+1] - periods[i] == 1:
                    consecutive += 1
                    if consecutive > 4:
                        counts['SC06'] += 1
                else:
                    consecutive = 1

        return counts