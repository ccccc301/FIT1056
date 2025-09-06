from app.schedule import ScheduleManager

def front_desk_daily_roster(manager):
    """Display the daily lesson roster for a specific day"""
    day = input("Day (e.g., Monday): ").strip()
    roster = manager.get_daily_lessons(day)
    if not roster:
        print(f"No lessons scheduled on {day}.")
        return
    print(f"\n== {day} Roster ==")
    for item in roster:
        print(f"[{item['start_time']}] {item['course_name']} ({item['instrument']}) | Teacher: {item['teacher_name']} | Room: {item['room']} | Students: {item['student_count']}")

def check_in_student(manager):
    """Handle student check-in process"""
    try:
        sid = int(input("Enter student ID: ").strip())
        cid = int(input("Enter course ID: ").strip())
    except ValueError:
        print("Error: Please enter valid numeric IDs.")
        return
    manager.check_in(sid, cid)

def view_all_courses(manager):
    """Display all courses with their details"""
    print("\n== All Courses ==")
    for c in manager.courses:
        t = manager.find_teacher_by_id(c.teacher_id)
        teacher_name = t.name if t else "Unknown"
        print(f"#{c.id if hasattr(c,'id') else c.course_id} {c.name} [{c.instrument}] | Teacher: {teacher_name} | Enrolled: {len(c.enrolled_student_ids)}")
        for lesson in c.lessons:
            print(f"   - {lesson.get('day','?')} {lesson.get('start_time','?')} @ {lesson.get('room','?')}")

def switch_student_course(manager):
    """Handle switching a student from one course to another"""
    try:
        student_id = int(input("Enter student ID: ").strip())
        from_course_id = int(input("Enter current course ID: ").strip())
        to_course_id = int(input("Enter new course ID: ").strip())
    except ValueError:
        print("Error: Please enter valid numeric IDs.")
        return
    s = manager.find_student_by_id(student_id)
    from_c = manager.find_course_by_id(from_course_id)
    to_c = manager.find_course_by_id(to_course_id)
    if not s or not from_c or not to_c:
        print("Error: invalid IDs.")
        return
    if student_id not in from_c.enrolled_student_ids:
        print("Error: student not enrolled in the current course.")
        return
    if from_course_id in getattr(s, "enrolled_course_ids", []):
        s.enrolled_course_ids.remove(from_course_id)
    if to_course_id not in getattr(s, "enrolled_course_ids", []):
        s.enrolled_course_ids.append(to_course_id)
    if student_id in from_c.enrolled_student_ids:
        from_c.enrolled_student_ids.remove(student_id)
    if student_id not in to_c.enrolled_student_ids:
        to_c.enrolled_student_ids.append(student_id)
    manager._save_data()
    print(f"Switched student {student_id} from course {from_course_id} to {to_course_id}.")

def review_all_students(manager):
    """Display all students with their enrollment details"""
    print("\n== All Students ==")
    for s in manager.students:
        ids = getattr(s, "enrolled_course_ids", [])
        names = []
        for cid in ids:
            c = manager.find_course_by_id(cid)
            if c:
                names.append(c.name)
        sid = s.user_id if hasattr(s, "user_id") else getattr(s, "id", None)
        print(f"#{sid} {s.name} | Enrolled: {len(ids)}" + ("" if not names else f" | {', '.join(names)}"))

def review_all_teachers(manager):
    """Display all teachers with their course assignments"""
    print("\n== All Teachers ==")
    for t in manager.teachers:
        courses = [c for c in manager.courses if c.teacher_id == (t.user_id if hasattr(t, "user_id") else getattr(t, "id", None))]
        tid = t.user_id if hasattr(t, "user_id") else getattr(t, "id", None)
        print(f"#{tid} {t.name} | {getattr(t,'speciality','')} | Courses: {len(courses)}" + ("" if not courses else f" | {', '.join(c.name for c in courses)}"))

def main():
    """Main application entry point"""
    manager = ScheduleManager("data/msms.json")
    while True:
        print("\n===== MSMS v3 (Object-Oriented) =====")
        print("1. Daily Roster")
        print("2. Check-in Student")
        print("3. View All Courses")
        print("4. Switch Student Course")
        print("5. Review All Students")
        print("6. Review All Teachers")
        print("7. Quit")
        choice = input("Choose: ").strip()
        if choice == "1":
            front_desk_daily_roster(manager)
        elif choice == "2":
            check_in_student(manager)
        elif choice == "3":
            view_all_courses(manager)
        elif choice == "4":
            switch_student_course(manager)
        elif choice == "5":
            review_all_students(manager)
        elif choice == "6":
            review_all_teachers(manager)
        elif choice == "7" or choice.lower() == "q":
            print("Bye.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()