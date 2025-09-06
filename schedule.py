import json
import datetime

from app.student import StudentUser
from app.teacher import TeacherUser, Course


class ScheduleManager:
    """Main controller class handling all business logic and data management"""
    def __init__(self, data_path="data/msms.json"):
        self.data_path = data_path
        self.students = []  # List of all student objects
        self.teachers = []  # List of all teacher objects
        self.courses = []   # List of all course objects
        self.attendance_log = []  # List of attendance records
        self.next_student_id = 1  # Counter for next student ID
        self.next_teacher_id = 1  # Counter for next teacher ID
        self.next_course_id = 1   # Counter for next course ID
        self._load_data()  # Load data from file on initialization

    def _load_data(self):
        """Load data from JSON file and populate object lists"""
        try:
            with open(self.data_path, "r", encoding="utf-8") as f:
                raw = json.load(f)
        except FileNotFoundError:
            return  # If file doesn't exist, start with empty data

        # Load students, teachers, and courses from JSON data
        self.students = [
            StudentUser(s["id"], s["name"]) for s in raw.get("students", [])
        ]
        self.teachers = [
            TeacherUser(t["id"], t["name"], t["speciality"])
            for t in raw.get("teachers", [])
        ]
        self.courses = [
            Course(c["id"], c["name"], c["instrument"], c["teacher_id"])
            for c in raw.get("courses", [])
        ]

        # Load enrollment and lesson data for each course
        for idx, c in enumerate(self.courses):
            c.enrolled_student_ids = raw["courses"][idx].get("enrolled_student_ids", [])
            c.lessons = raw["courses"][idx].get("lessons", [])

        # Load attendance records
        self.attendance_log = list(raw.get("attendance", []))

        # Set next ID values, using max existing ID + 1 as fallback
        self.next_student_id = raw.get(
            "next_student_id",
            max([s.id for s in self.students], default=0) + 1
        )
        self.next_teacher_id = raw.get(
            "next_teacher_id",
            max([t.id for t in self.teachers], default=0) + 1
        )
        self.next_course_id = raw.get(
            "next_course_id",
            max([c.id for c in self.courses], default=0) + 1
        )

    def _save_data(self):
        """Convert object lists to dictionaries and save to JSON file"""
        out = {
            "students": [{"id": s.id, "name": s.name} for s in self.students],
            "teachers": [
                {"id": t.id, "name": t.name, "speciality": t.speciality}
                for t in self.teachers
            ],
            "courses": [
                {
                    "id": c.id,
                    "name": c.name,
                    "instrument": c.instrument,
                    "teacher_id": c.teacher_id,
                    "enrolled_student_ids": list(c.enrolled_student_ids),
                    "lessons": list(c.lessons),
                }
                for c in self.courses
            ],
            "attendance": list(self.attendance_log),
            "next_student_id": self.next_student_id,
            "next_teacher_id": self.next_teacher_id,
            "next_course_id": self.next_course_id,
        }
        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump(out, f, indent=4, ensure_ascii=False)

    def find_student_by_id(self, student_id):
        """Find a student by ID, return None if not found"""
        for s in self.students:
            if s.id == student_id:
                return s
        return None

    def find_teacher_by_id(self, teacher_id):
        """Find a teacher by ID, return None if not found"""
        for t in self.teachers:
            if t.id == teacher_id:
                return t
        return None

    def find_course_by_id(self, course_id):
        """Find a course by ID, return None if not found"""
        for c in self.courses:
            if c.id == course_id:
                return c
        return None

    def get_daily_lessons(self, day):
        """Get all lessons scheduled for a specific day, sorted by start time"""
        day_lower = str(day).lower()
        result = []
        for c in self.courses:
            for lesson in c.lessons:
                if str(lesson.get("day", "")).lower() == day_lower:
                    teacher = self.find_teacher_by_id(c.teacher_id)
                    result.append({
                        "course_id": c.id,
                        "course_name": c.name,
                        "instrument": c.instrument,
                        "teacher_name": teacher.name if teacher else "Unknown",
                        "start_time": lesson.get("start_time", ""),
                        "room": lesson.get("room", ""),
                        "student_count": len(c.enrolled_student_ids),
                    })
        result.sort(key=lambda x: x["start_time"])  # Sort by start time
        return result

    def check_in(self, student_id, course_id):
        """Record student attendance for a course with validation"""
        student = self.find_student_by_id(student_id)
        course = self.find_course_by_id(course_id)
        if not student or not course:
            print("Error: Check-in failed. Invalid Student or Course ID.")
            return False
        if student_id not in course.enrolled_student_ids:
            print("Error: Student is not enrolled in this course.")
            return False
        ts = datetime.datetime.now().isoformat()  # Current timestamp
        self.attendance_log.append({
            "student_id": student_id,
            "course_id": course_id,
            "timestamp": ts
        })
        self._save_data()  # Persist changes to file
        print(f"Success: Student {student.name} checked into {course.name}.")
        return True