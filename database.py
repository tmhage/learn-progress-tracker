from models import Course, Student


class Database:

    def __init__(self) -> None:
        self.student_table = {}
        self.email_table = EmailHashTable()
        self.course_table: dict[str, Course] = {
            "python": Course("Python", 600),
            "dsa": Course("DSA", 400),
            "databases": Course("Databases", 480),
            "flask": Course("Flask", 550)
        }
        self.to_be_notified = {}
        # self.update_course('dsa', 1)
        # self.update_course('databases', 4)
        # self.update_course('python', 4)

        # Add sample data
        # student_a = Student('jim', 'bang', 'jimbang@gmail.com')
        # student_b = Student('jane', 'doe', 'janedoe@hotmail.com')
        # student_c = Student('timmy', 'dal', 'timdal@hotmail.com')
        # self.add_student(student_a)
        # self.add_student(student_b)
        # self.add_student(student_c)

    def get_enrolled_students_ids(self, course_name: str) -> list[int]:
        return self.course_table[course_name].enrolled_students

    def get_student_course(self, student_id: int, course_name: str) -> dict:
        return self.student_table[student_id].score_card.courses[course_name]

    def add_student(self, student: Student) -> None:
        self.student_table[student.id] = student
        self.email_table.add_email(student.email, student.id)

    def get_student(self, student_id: int) -> Student:
        return self.student_table.get(student_id, None)

    def get_student_by_email(self, email: str) -> Student:
        student_id = self.email_table.get_student_id(email)
        return self.student_table.get(student_id, None)

    def get_course(self, course_name: str) -> Course:
        return self.course_table.get(course_name, None)

    def get_courses_by_attribute(self, attribute_name: str, threshold: int = 1) -> list[Course]:
        selected_courses = [
            course for course_name, course in self.course_table.items() if getattr(course, attribute_name) >= threshold]

        return selected_courses

    def add_completed_notification(self, student: Student, course_name: str) -> None:
        student_id = student.id
        new_notifications = self.to_be_notified
        if student_id not in new_notifications:
            new_notifications[student_id] = []
        new_notifications[student_id].append(course_name)

    def update_completed_course(self, student: Student, course_name: str, new_points: int) -> None:
        course = self.get_course(course_name)
        current_points = student.score_card.get_points(course_name)
        # If addition of new points passes the completion threshold
        if new_points > 0 and current_points < course.pass_threshold <= current_points + new_points:
            course.completed += 1
            self.add_completed_notification(student, course_name)

    def update_enrolled_course(self, student: Student, course_name: str, new_points: int) -> None:
        current_points = student.score_card.get_points(course_name)
        if current_points == 0 and new_points > 0:
            course = self.course_table[course_name]
            course.enrolled_students.append(student.id)


class EmailHashTable:
    def __init__(self):
        self.table = {}

    def add_email(self, email, student_id):
        hashed = hash(email)
        self.table[hashed] = student_id

    def get_student_id(self, email: str) -> int:
        hashed = hash(email)
        return self.table.get(hashed, None)
