def check_in(student_id, course_id, timestamp=None):
    """
    Record a student's check-in for a course.
    :param student_id: ID of the student
    :param course_id: ID of the course
    :param timestamp: Optional custom timestamp, defaults to current time
    """
    if timestamp is None:
        timestamp = datetime.datetime.now().isoformat()
    check_in_record = {
        "student_id": student_id,
        "course_id": course_id,
        "timestamp": timestamp
    }
    app_data['attendance'].append(check_in_record)
    save_data()
    print(f"Student {student_id} checked into course {course_id} at {timestamp}.")

def print_student_card(student_id):
    """
    Generate and save a student's ID card to a text file.
    :param student_id: ID of the student to print
    """
    student_to_print = None
    for s in app_data['students']:
        if s['id'] == student_id:
            student_to_print = s
            break
    if student_to_print:
        filename = f"{student_id}_card.txt"
        with open(filename, 'w') as f:
            f.write("========================\n")
            f.write(f"  MUSIC SCHOOL ID BADGE\n")
            f.write("========================\n")
            f.write(f"ID: {student_to_print['id']}\n")
            f.write(f"Name: {student_to_print['name']}\n")
            f.write(f"Enrolled In: {', '.join(student_to_print.get('enrolled_in', []))}\n")
        print(f"Student card printed to {filename}.")
    else:
        print(f"Error: Student with ID {student_id} not found.")