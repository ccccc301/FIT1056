from app.user import User

class StudentUser(User):
    """Represents a student, inheriting from the base User class."""
    def __init__(self, user_id, name, instrument=None):
        super().__init__(user_id, name)
        self.instrument = instrument
        self.enrolled_course_ids = []