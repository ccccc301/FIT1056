from Fragment1_1 import Student, student_db, next_student_id
from Fragment1_2 import find_students, find_teachers
# --- Front Desk Functions ---
def find_student_by_id(student_id):
    """
    Finds a student in the database by their unique ID.

    Args:
        student_id (int): The ID of the student to find.

    Returns:
        Student: The student object if found, otherwise None.
    """
    for student in student_db:
        if student.id == student_id:
            return student
    return None

def front_desk_register(name, instrument):
    """
    Registers a new student and immediately enrolls them in an instrument.

    Args:
        name (str): Student's name.
        instrument (str): Instrument to enroll the student in.
    """
    global next_student_id
    name = name.strip()
    instrument = instrument.strip()

    if not name or not instrument:
        print("Error: Student name and instrument cannot be empty.")
        return
    new_student = Student(next_student_id, name)
    student_db.append(new_student)
    next_student_id += 1

    # Automatically enroll the student in their chosen instrument
    front_desk_enrol(new_student.id, instrument)
    print(f"Front Desk: Successfully registered '{name}' and enrolled them in '{instrument}'.")

def front_desk_enrol(student_id, instrument):
    """
    Enrolls an existing student in a new instrument.

    Args:
        student_id (int): ID of the student to enroll.
        instrument (str): Instrument to add.
    """
    student = find_student_by_id(student_id)
    if student:
        student.enrolled_in.append(instrument)
        print(f"Front Desk: Enrolled student {student_id} in '{instrument}'.")
    else:
        print(f"Error: Student ID {student_id} not found.")

def front_desk_lookup(term):
    """
    Performs a search for both students and teachers.

    Args:
        term (str): Search term.
    """
    print(f"\n--- Performing lookup for '{term}' ---")
    find_students(term)
    find_teachers(term)