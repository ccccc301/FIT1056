import streamlit as st


def _course_label(course) -> str:
    """Compact label without schedule details."""
    cid = getattr(course, "id", None)
    name = getattr(course, "name", "")
    inst = getattr(course, "instrument", "")
    return f"[{cid}] {name} — {inst}"


def show_student_management_page(manager):
    """Render all components for the Student Management page."""
    st.header("Student Management")

    st.subheader("Find a Student")

    # Using a form puts the submit button under the input and also enables pressing Enter to submit.
    with st.form("search_student_form", clear_on_submit=False):
        # Text input for name or ID
        search_key = st.text_input("Enter name or ID to search")

        # Submit button appears directly under the input
        search_clicked = st.form_submit_button("Search")

    # Handle the submission
    if search_clicked:
        if not search_key.strip():
            st.warning("Please enter a search keyword.")
        else:
            results = manager.find_student(search_key)
            if results:
                st.success(f"Found {len(results)} student(s):")
                for s in results:
                    st.write(f"ID: {s.id} | Name: {s.name}")
            else:
                st.error("No matching students found.")

    st.divider()

    st.subheader("Register a New Student")

    with st.form("registration_form", clear_on_submit=True):
        new_name = st.text_input("New Student Name")

        # Replace the old free-text instrument with a real course choice.
        courses = manager.get_courses()
        if not courses:
            st.info("No courses available yet. Please create a course first.")
            submit_btn = st.form_submit_button("Register Student", disabled=True)
            selected_course_id = None
        else:
            options = {_course_label(c): getattr(c, "id", None) for c in courses}
            chosen_label = st.selectbox("First Course", list(options.keys()))
            selected_course_id = int(options[chosen_label])
            submit_btn = st.form_submit_button("Register Student")

        if submit_btn:
            if not new_name.strip():
                st.warning("Please enter the student's name.")
                st.stop()

            sid = manager.register_new_student(new_name.strip(), instrument=None)
            ok = False
            if selected_course_id is not None:
                ok = manager.enroll_student_in_course(int(sid), int(selected_course_id))

            if ok:
                course = manager.get_course_by_id(int(selected_course_id))
                st.success(
                    f"Registered '{new_name}' (ID: {sid}) and enrolled to "
                    f"[{course.id}] {course.name}."
                )
            else:
                st.success(f"Registered '{new_name}' (ID: {sid}).")
                st.warning("Enrollment step was skipped or failed; please enroll manually if needed.")