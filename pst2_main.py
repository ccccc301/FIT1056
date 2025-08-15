import json
import datetime

DATA_FILE = "msms.json"  # File name for saving persistent data

# Global dictionary to store all application data
app_data = {}

def load_data(path=DATA_FILE):
    """
    Load all application data from the JSON file.
    If the file does not exist, initialize with a default empty structure.
    """
    global app_data
    try:
        with open(path, 'r') as f:
            app_data = json.load(f)
            print("Data loaded successfully.")
    except FileNotFoundError:
        print("Data file not found. Initializing with default structure.")
        app_data = {
            "students": [],
            "teachers": [],
            "attendance": [],
            "next_student_id": 1,
            "next_teacher_id": 1
        }

def save_data(path=DATA_FILE):
    """
    Save the current application data into the JSON file.
    """
    with open(path, "w") as f:
        json.dump(app_data, f, indent=4)
    print("Data saved successfully.")

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

def main():
    """
    Main menu loop for the Music School Management System.
    Allows user to choose operations until they decide to quit.
    """
    load_data()
    while True:
        print("\n===== MSMS v2 (Persistent) =====")
        print("1. Add Student")
        print("2. Add Teacher")
        print("3. Update Student Info")
        print("4. Update Teacher Info")
        print("5. Remove Student")
        print("6. Remove Teacher")
        print("7. Check-in Student")
        print("8. Print Student Card")
        print("q. Quit")
        
        choice = input("Enter your choice: ").strip().lower()
        try:
            if choice == '1':
                name = input("Enter student name: ")
                courses = input("Enter enrolled courses (comma separated): ").split(',')
                add_student(name, [c.strip() for c in courses if c.strip()])
            elif choice == '2':
                name = input("Enter teacher name: ")
                speciality = input("Enter teacher speciality: ")
                add_teacher(name, speciality)
            elif choice == '3':
                student_id = int(input("Enter student ID to update: "))
                name = input("Enter new name (leave blank to keep current): ")
                courses = input("Enter new courses (comma separated, leave blank to keep): ")
                update_data = {}
                if name: update_data['name'] = name
                if courses: 
                    update_data['enrolled_in'] = [c.strip() for c in courses.split(',') if c.strip()]
                if update_data:
                    update_student(student_id, **update_data)
                else:
                    print("No changes made.")
            elif choice == '4':
                teacher_id = int(input("Enter teacher ID to update: "))
                name = input("Enter new name (leave blank to keep current): ")
                speciality = input("Enter new speciality (leave blank to keep): ")
                update_data = {}
                if name: update_data['name'] = name
                if speciality: update_data['speciality'] = speciality
                if update_data:
                    update_teacher(teacher_id, **update_data)
                else:
                    print("No changes made.")
            elif choice == '5':
                student_id = int(input("Enter student ID to remove: "))
                remove_student(student_id)
            elif choice == '6':
                teacher_id = int(input("Enter teacher ID to remove: "))
                remove_teacher(teacher_id)
            elif choice == '7':
                student_id = int(input("Enter student ID: "))
                course_id = input("Enter course ID: ")
                check_in(student_id, course_id)
            elif choice == '8':
                student_id = int(input("Enter student ID: "))
                print_student_card(student_id)
            elif choice == 'q':
                print("Exiting application.")
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Error: Please enter a valid number for ID fields.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()