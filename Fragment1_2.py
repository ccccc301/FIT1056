from Fragment1_1 import Student, Teacher, student_db, teacher_db, next_teacher_id
# --- Core Helper Functions ---
def add_teacher(name, speciality):
    """
    Creates a Teacher object and adds it to the in-memory teacher database.

    Args:
        name (str): Full name of the teacher.
        speciality (str): Instrument the teacher specializes in.
    """
    global next_teacher_id
    # Ensure name and speciality are not empty
    if not name.strip() or not speciality.strip():
        print("Error: Teacher name and speciality cannot be empty.")
        return
    # Create a new Teacher instance with the current available ID
    new_teacher = Teacher(next_teacher_id, name, speciality)
    teacher_db.append(new_teacher)  # Store in database
    next_teacher_id += 1  # Increment ID counter
    print(f"Core: Teacher '{name}' added successfully.")

def list_students():
    """
    Prints all students in the database, along with their enrolled instruments.
    """
    print("\n--- Student List ---")
    if not student_db:
        print("No students in the system.")
        return
    for student in student_db:
        print(f"  ID: {student.id}, Name: {student.name}, Enrolled in: {student.enrolled_in}")

def list_teachers():
    """
    Prints all teachers in the database, along with their speciality.
    """
    print("\n--- Teacher List ---")
    if not teacher_db:
        print("No teachers in the system.")
        return
    for teacher in teacher_db:
        print(f"  ID: {teacher.id}, Name: {teacher.name}, Speciality: {teacher.speciality}")

def find_students(term):
    """
    Searches for students by name.

    Args:
        term (str): Search term (case-sensitive match in current version).
    """
    print(f"\n--- Finding Students matching '{term}' ---")
    result = []
    for student in student_db:
        if term in student.name:
            result.append(student)
    if not result:
        print("No match found.")
    else:
        for s in result:
            print(f"  ID: {s.id}, Name: {s.name}, Enrolled in: {s.enrolled_in}")

def find_teachers(term):
    """
    Searches for teachers by name or speciality.

    Args:
        term (str): Search term (case-sensitive match in current version).
    """
    print(f"\n--- Finding Teachers matching '{term}' ---")
    results = []
    for teacher in teacher_db:
        if term in teacher.name or term in teacher.speciality:
            results.append(teacher)
    if not results:
        print("No match found.")
    else:
        for t in results:
            print(f"  ID: {t.id}, Name: {t.name}, Speciality: {t.speciality}")