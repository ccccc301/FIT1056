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