import streamlit as st

def show_student_management_page(manager):
    """Renders all components for the student management page."""
    st.header("Student Management")
    
    # --- Student Search Section ---
    st.subheader("Find a Student")
    # Text input for searching students by name
    search_name = st.text_input("Search by name")
    
    # Display search results if search term is provided
    if search_name:
        # Filter students whose names contain the search term (case-insensitive)
        found_students = [s for s in manager.students if search_name.lower() in s.name.lower()]
        if found_students:
            # Display each found student's information
            for student in found_students:
                st.write(f"ID: {student.id}, Name: {student.name}, Instrument: {student.instrument}")
        else:
            st.info("No students found.")
    
    # --- Student Registration Section ---
    st.subheader("Register New Student")
    # Create a form that clears on submit for student registration
    with st.form("registration_form", clear_on_submit=True): 
        # Input fields for new student information
        reg_name = st.text_input("New Student Name")
        reg_instrument = st.text_input("First Instrument")
        submitted = st.form_submit_button("Register Student")
        
        # Process form submission
        if submitted:
            # Validate that both fields are filled
            if not reg_name or not reg_instrument:
                st.warning("Please enter both a name and an instrument.")
            else:
                # Normalize input for duplicate checking (case-insensitive, trimmed)
                norm = reg_name.strip().casefold()
                # Check if a student with the same name already exists
                if any(s.name.strip().casefold() == norm for s in manager.students):
                    st.error("A student with the same name already exists.")
                else:
                    # Register new student through the manager
                    new_id = manager.register_new_student(reg_name, reg_instrument)
                    if new_id:
                        st.success(f"Successfully registered {reg_name} (ID: {new_id})!")
                    else:
                        st.error("Could not register student (duplicate name or invalid data).")