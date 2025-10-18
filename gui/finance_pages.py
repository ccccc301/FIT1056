# gui/finance_pages.py
import streamlit as st
import pandas as pd

def show_finance_page(manager):
    """Renders the UI for all financial operations."""
    st.header("Finance & Payments")
    st.subheader("Record New Payment")
    with st.form("payment_form"):
        # Populate dropdown with current students (name → id mapping for UX)
        student_list = {s.name: s.id for s in manager.students}
        if not student_list:
            st.info("No students available yet. Please register students first.")
            submitted = st.form_submit_button("Record Payment", disabled=True)
        else:
            selected_student_name = st.selectbox("Select Student", list(student_list.keys()))
            amount = st.number_input("Amount", min_value=0.0, step=1.0, format="%.2f")
            method = st.text_input("Method (e.g., Cash, Credit Card, Bank Transfer)")
            submitted = st.form_submit_button("Record Payment")

        if submitted and student_list:
            try:
                student_id = student_list[selected_student_name]
                rec = manager.record_payment(student_id, amount, method or "Unspecified")
                st.success(f"Recorded payment: {rec['amount']:.2f} for {selected_student_name} via {rec['method']}.")
            except Exception as e:
                st.error(f"Failed to record payment: {e}")

    st.subheader("View Student Payment History")
    if not manager.students:
        st.info("No students to show payment history for.")
        return

    student_list = {s.name: s.id for s in manager.students}
    history_student_name = st.selectbox("Select Student to View History", list(student_list.keys()))
    if history_student_name:
        history_student_id = student_list[history_student_name]
        history = manager.get_payment_history(history_student_id)
        if history:
            df = pd.DataFrame(history)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("This student has no payment history.")
