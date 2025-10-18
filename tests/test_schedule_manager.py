# tests/test_schedule_manager.py
import pytest
import os
from app.schedule import ScheduleManager

@pytest.fixture
def fresh_manager():
    """Creates a fresh ScheduleManager instance using a temporary test data file."""
    test_file = "test_data.json"
    if os.path.exists(test_file):
        os.remove(test_file)
    mgr = ScheduleManager(data_path=test_file)

    # Seed with minimal fixtures used by tests
    # Add one student (id=1) and a teacher so create_course works nicely
    from app.student import StudentUser
    from app.teacher import TeacherUser
    mgr.students.append(StudentUser(1, "Test Student"))
    mgr.teachers.append(TeacherUser(1, "Test Teacher", "Piano"))
    mgr._save_data()
    return mgr

def test_create_course(fresh_manager):
    # ARRANGE
    # ACT
    course_id = fresh_manager.create_course("Beginner Piano", "Piano", 1)
    # ASSERT
    assert len(fresh_manager.courses) == 1
    assert fresh_manager.courses[0].name == "Beginner Piano"
    assert fresh_manager.courses[0].id == course_id

def test_record_payment_and_history(fresh_manager):
    # ARRANGE
    student_id_to_test = 1

    # ACT 1: Record a payment for that student.
    fresh_manager.record_payment(student_id_to_test, 100.00, "Credit Card")
    # ACT 2: Fetch the student's payment history.
    history = fresh_manager.get_payment_history(student_id_to_test)

    # ASSERT
    assert len(history) == 1
    assert history[0]['amount'] == 100.00
    assert history[0]['method'] == "Credit Card"

def test_get_payment_history_no_results(fresh_manager):
    # ARRANGE: use a student id with no payments
    student_id_with_no_payments = 999
    # ACT
    history = fresh_manager.get_payment_history(student_id_with_no_payments)
    # ASSERT
    assert history == []
