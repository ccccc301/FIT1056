# MSMS.py - The In-Memory Prototype

# --- Data Models ---
class Student:
    """
    Represents a student in the music school.
    
    Attributes:
        id (int): Unique student ID.
        name (str): Full name of the student.
        enrolled_in (list): List of instruments the student is currently learning.
    """
    def __init__(self, student_id, name):
        # Assign provided ID and name to the student
        self.id = student_id
        self.name = name
        # Initialize with an empty list of instruments
        self.enrolled_in = []

class Teacher:
    """
    Represents a teacher in the music school.
    
    Attributes:
        id (int): Unique teacher ID.
        name (str): Full name of the teacher.
        speciality (str): The instrument(s) the teacher specializes in.
    """
    def __init__(self, teacher_id, name, speciality):
        self.id = teacher_id
        self.name = name
        self.speciality = speciality

# --- In-Memory Databases ---
# Lists to store all current students and teachers in memory
student_db = []
teacher_db = []
# ID counters for assigning unique IDs to students and teachers.
next_student_id = 1
next_teacher_id = 1