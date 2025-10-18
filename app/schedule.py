import json
import csv
import datetime
import logging

from app.student import StudentUser
from app.teacher import TeacherUser, Course


class ScheduleManager:
    """The main controller for all business logic and data handling."""

    def __init__(self, data_path: str = "data/msms.json"):
        # Path to the JSON data file on disk.
        self.data_path = data_path

        # In-memory containers for our domain objects.
        self.students = []   # list[StudentUser]
        self.teachers = []   # list[TeacherUser]
        self.courses = []    # list[Course]
        self.next_lesson_id = 1
        self.finance_log = []
        # Read existing data from disk (if present) into the above containers.
        self._load_data()

    def _load_data(self) -> None:
        """Load data from the JSON file and populate the object lists."""
        try:
            with open(self.data_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.students.clear()
            for s in data.get("students", []):
                # StudentUser expects (user_id, name). The JSON also stores enrolled_course_ids.
                stu = StudentUser(s["id"], s["name"])
                # Populate the enrolled courses list if present.
                stu.enrolled_course_ids = list(s.get("enrolled_course_ids", []))
                self.students.append(stu)

            self.teachers.clear()
            for t in data.get("teachers", []):
                # TeacherUser expects (user_id, name, speciality).
                teacher = TeacherUser(t["id"], t["name"], t.get("speciality", "Unknown"))
                self.teachers.append(teacher)

            self.courses.clear()
            for c in data.get("courses", []):
                # Course expects (course_id, name, instrument, teacher_id)
                course = Course(c["id"], c["name"], c["instrument"], c["teacher_id"])
                # Fill enrolled students and lessons if provided.
                course.enrolled_student_ids = list(c.get("enrolled_student_ids", []))
                course.lessons = list(c.get("lessons", []))
                # Maintain next_lesson_id so newly created lessons keep unique ids.
                for les in course.lessons:
                    if "lesson_id" in les:
                        self.next_lesson_id = max(self.next_lesson_id, les["lesson_id"] + 1)
                self.courses.append(course)

            self.finance_log = list(data.get("finance_log", []))

        except FileNotFoundError:
            # It is fine to start fresh if the file does not exist.
            print("Data file not found. Starting with a clean state.")

    def _save_data(self) -> None:
        """Convert object lists back to plain dictionaries and write them to JSON."""
        data_to_save = {
            "students": [
                {
                    "id": s.id,
                    "name": s.name,
                    "enrolled_course_ids": list(getattr(s, "enrolled_course_ids", [])),
                }
                for s in self.students
            ],
            "teachers": [
                {
                    "id": t.id,
                    "name": t.name,
                    "speciality": getattr(t, "speciality", "Unknown"),
                }
                for t in self.teachers
            ],
            "courses": [
                {
                    "id": c.id,
                    "name": c.name,
                    "instrument": c.instrument,
                    "teacher_id": c.teacher_id,
                    "enrolled_student_ids": list(getattr(c, "enrolled_student_ids", [])),
                    "lessons": list(getattr(c, "lessons", [])),
                }
                for c in self.courses
            ],
            "finance_log": list(self.finance_log),
        }

        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump(data_to_save, f, indent=2, ensure_ascii=False)


    def register_new_student(self, name: str, instrument: str | None = None) -> int:
        """Create a new student, persist to JSON, and return the new student id."""
        if not name or not name.strip():
            raise ValueError("Student name is required.")

        new_id = max([s.id for s in self.students], default=0) + 1
        student = StudentUser(new_id, name.strip())

        # Ensure the field exists for persistence even if StudentUser didn't define it.
        if not hasattr(student, "enrolled_course_ids") or student.enrolled_course_ids is None:
            student.enrolled_course_ids = []

        self.students.append(student)
        self._save_data()
        logging.info(f"[STUDENT] Registered student id={new_id}, name={student.name}")
        return new_id

    def find_student(self, keyword: str):
        """Find by exact ID (numeric) or partial name (case-insensitive)."""
        if not keyword or not str(keyword).strip():
            return []

        q = str(keyword).strip()
        q_fold = q.casefold()

        if q.isdigit():
            target = int(q)
            exact = [s for s in self.students if s.id == target]
            if exact:
                return exact
        # Name partial 
        return [s for s in self.students if q_fold in str(s.name).casefold()]

    def search_students(self, query: str):
        """Thin wrapper so GUI can call a neutral name."""
        return self.find_student(query)

    def get_courses(self):
        """Return all courses for GUI listing."""
        return list(self.courses)

    def get_course_by_id(self, course_id: int):
        """Return a course object by id, or None if not found."""
        for c in self.courses:
            if getattr(c, "id", None) == course_id:
                return c
        return None

    def create_course(self, name: str, instrument: str, teacher_id: int) -> int:
        """Create a new Course and store it in memory (then persist)."""
        new_id = (max([c.id for c in self.courses], default=100) + 1)
        course = Course(new_id, name, instrument, teacher_id)
        course.enrolled_student_ids = []
        course.lessons = []
        self.courses.append(course)
        self._save_data()
        logging.info(f"[COURSE] Created course id={new_id}, name={name}, teacher={teacher_id}")
        return new_id

    def enroll_student_in_course(self, student_id: int, course_id: int) -> bool:
        """
        Add student to a course (idempotent); persist & log.
        Also updates student's 'enrolled_course_ids'.
        """
        course = self.get_course_by_id(course_id)
        if not course:
            return False

        # Ensure list exists on course
        if not hasattr(course, "enrolled_student_ids") or course.enrolled_student_ids is None:
            course.enrolled_student_ids = []

        # Ensure list exists on student
        student = next((s for s in self.students if s.id == student_id), None)
        if not student:
            return False
        if not hasattr(student, "enrolled_course_ids") or student.enrolled_course_ids is None:
            student.enrolled_course_ids = []

        # Idempotent updates
        if student_id not in course.enrolled_student_ids:
            course.enrolled_student_ids.append(student_id)
        if course_id not in student.enrolled_course_ids:
            student.enrolled_course_ids.append(course_id)

        self._save_data()
        logging.info(f"[ENROLL] student={student_id} -> course={course_id}")
        return True

    def check_in(self, student_id: int, course_id: int) -> bool:
        """
        Example roster operation used by the roster GUI.
        Returns True if the student is enrolled in the course; otherwise False.
        """
        course = next((c for c in self.courses if c.id == course_id), None)
        if not course:
            print("Course not found.")
            return False
        if student_id not in course.enrolled_student_ids:
            print("Student is not enrolled in this course.")
            return False
        # record attendance here.
        return True

    def record_payment(self, student_id: int, amount: float, method: str) -> dict:
        """Add a payment record to the in-memory finance log and persist it."""
        # Validate the student exists for better integrity/error messages.
        student_exists = any(s.id == student_id for s in self.students)
        if not student_exists:
            raise ValueError(f"Student with id {student_id} does not exist.")

        payment_record = {
            "student_id": int(student_id),
            "amount": float(amount),
            "method": str(method),
            "timestamp": datetime.datetime.now().isoformat(timespec="seconds"),
        }
        self.finance_log.append(payment_record)
        self._save_data()

        logging.info(
            f"[FINANCE] Payment recorded: student={student_id}, amount={amount}, method={method}"
        )
        return payment_record

    def get_payment_history(self, student_id: int) -> list[dict]:
        """Return all payments for a given student id."""
        return [p for p in self.finance_log if p.get("student_id") == student_id]

    def export_report(self, kind: str, out_path: str) -> str:
        """
        Export a CSV report.
        kind: one of {"payments", "students", "courses"}.
        """
        kind = (kind or "").strip().lower()
        if kind not in {"payments", "students", "courses"}:
            raise ValueError("Unsupported report kind. Use 'payments', 'students', or 'courses'.")

        with open(out_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)

            if kind == "payments":
                writer.writerow(["student_id", "amount", "method", "timestamp"])
                for p in self.finance_log:
                    writer.writerow(
                        [p.get("student_id"), p.get("amount"), p.get("method"), p.get("timestamp")]
                    )

            elif kind == "students":
                writer.writerow(["id", "name", "enrolled_courses_count"])
                for s in self.students:
                    writer.writerow([s.id, s.name, len(getattr(s, "enrolled_course_ids", []))])

            elif kind == "courses":
                writer.writerow(["id", "name", "instrument", "teacher_id", "enrolled_count"])
                for c in self.courses:
                    writer.writerow([c.id, c.name, c.instrument, c.teacher_id,
                                     len(getattr(c, "enrolled_student_ids", []))])

        logging.info(f"[REPORT] Exported '{kind}' report to {out_path}")
        return out_path
