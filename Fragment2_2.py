def add_student(name, enrolled_in=None):
    """
    Add a new student to the system.
    :param name: Student's name (string)
    :param enrolled_in: List of enrolled courses (optional)
    :return: The new student's ID
    """
    if enrolled_in is None:
        enrolled_in = []
    student_id = app_data["next_student_id"]
    new_student = {
        "id": student_id,
        "name": name,
        "enrolled_in": enrolled_in
    }
    app_data["students"].append(new_student)
    app_data["next_student_id"] += 1
    save_data()
    print(f"Student '{name}' added with ID {student_id}.")
    return student_id

def add_teacher(name, speciality):
    """
    Add a new teacher to the system.
    :param name: Teacher's name (string)
    :param speciality: Teacher's speciality (string)
    """
    teacher_id = app_data["next_teacher_id"]
    new_teacher = {"id": teacher_id, "name": name, "speciality": speciality}
    app_data["teachers"].append(new_teacher)
    app_data["next_teacher_id"] += 1
    save_data()
    print(f"Teacher '{name}' added with ID {teacher_id}.")

def update_teacher(teacher_id, **fields):
    """
    Update an existing teacher's information.
    :param teacher_id: Teacher ID to update (int)
    :param fields: Key-value pairs of fields to update
    :return: True if updated, False if teacher not found
    """
    for teacher in app_data['teachers']:
        if teacher['id'] == teacher_id:
            teacher.update(fields)
            save_data()
            print(f"Teacher {teacher_id} updated.")
            return True
    print(f"Error: Teacher with ID {teacher_id} not found.")
    return False

def remove_teacher(teacher_id):
    """
    Remove a teacher from the system by ID.
    :param teacher_id: Teacher ID to remove (int)
    :return: True if removed, False if teacher not found
    """
    for teacher in app_data['teachers']:
        if teacher['id'] == teacher_id:
            app_data['teachers'].remove(teacher)
            save_data()
            print(f"Teacher {teacher_id} removed.")
            return True
    print(f"Error: Teacher with ID {teacher_id} not found.")
    return False

def update_student(student_id, **fields):
    """
    Update an existing student's information.
    :param student_id: Student ID to update (int)
    :param fields: Key-value pairs of fields to update
    :return: True if updated, False if student not found
    """
    for student in app_data['students']:
        if student['id'] == student_id:
            student.update(fields)
            save_data()
            print(f"Student {student_id} updated.")
            return True
    print(f"Error: Student with ID {student_id} not found.")
    return False

def remove_student(student_id):
    """
    Remove a student from the system by ID.
    :param student_id: Student ID to remove (int)
    :return: True if removed, False if student not found
    """
    for student in app_data['students']:
        if student['id'] == student_id:
            app_data['students'].remove(student)
            save_data()
            print(f"Student {student_id} removed.")
            return True
    print(f"Error: Student with ID {student_id} not found.")
    return False