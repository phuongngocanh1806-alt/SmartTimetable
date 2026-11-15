
import random


class Chromosome:
    def __init__(self, data_model):
        """
        Khởi tạo một cá thể thời khóa biểu.
        """
        self.data_model = data_model
        self.schedule = []
        self.fitness = 0.0

    def get_data(self, name):
        """
        Lấy dữ liệu từ sample_data.py.
        Hỗ trợ dữ liệu dạng dictionary hoặc module/object.
        """
        data_names = {
            "courses": "COURSES",
            "rooms": "ROOMS",
            "timeslots": "TIME_SLOTS",
            "teachers": "TEACHERS"
        }

        if isinstance(self.data_model, dict):
            return self.data_model.get(
                name,
                self.data_model.get(data_names[name], [])
            )

        return getattr(
            self.data_model,
            data_names[name],
            []
        )

    def generate_random(self):
        """
        Tạo ngẫu nhiên một thời khóa biểu ban đầu.
        """

        self.schedule = []

        courses = self.get_data("courses")
        rooms = self.get_data("rooms")
        timeslots = self.get_data("timeslots")
        teachers = self.get_data("teachers")

        if not courses:
            raise ValueError("Danh sách môn học đang trống.")

        if not rooms:
            raise ValueError("Danh sách phòng học đang trống.")

        if not timeslots:
            raise ValueError("Danh sách khung giờ đang trống.")

        for course in courses:

            total_sessions = course.get("total_sessions", 1)

            if total_sessions > len(timeslots):
                raise ValueError(
                    "Số buổi học nhiều hơn số khung giờ."
                )

            # Tìm phòng phù hợp với môn học
            suitable_rooms = []

            for room in rooms:
                if (
                    room.get("type") == course.get("required_room_type")
                    and room.get("capacity", 0) >= course.get("num_students", 0)
                ):
                    suitable_rooms.append(room)

            if not suitable_rooms:
                raise ValueError(
                    "Không tìm thấy phòng phù hợp cho "
                    + course["subject_name"]
                )

            # Tìm thông tin giảng viên
            teacher = None

            for item in teachers:
                if item["teacher_id"] == course["teacher_id"]:
                    teacher = item
                    break

            # Chọn các khung giờ khác nhau cho cùng một lớp học phần
            selected_timeslots = random.sample(
                timeslots,
                total_sessions
            )

            for timeslot in selected_timeslots:

                gene = {
                    "course": course,
                    "course_id": course["course_id"],
                    "subject_name": course["subject_name"],
                    "teacher_id": course["teacher_id"],
                    "teacher": teacher,
                    "room": random.choice(suitable_rooms),
                    "timeslot": timeslot
                }

                self.schedule.append(gene)

        return self.schedule

    def calculate_fitness(self):
        """
        Lấy điểm Fitness sau khi tích hợp module của TV3.
        """
        return self.fitness
