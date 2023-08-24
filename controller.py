from database import Database
from models import Student, ScoreCard
from typing import Union
from exceptions import \
    NoStudentError, EmailExistsError, IncorrectPointsFormatError, NoCourseError


class Controller:
    def __init__(self, db: Database):
        self.db: Database = db

    def add_student(self, student_input: str) -> None:
        student = Student.from_str(student_input)
        if self.db.get_student_by_email(student.email):
            raise EmailExistsError
        else:
            self.db.add_student(student)

    def add_points(self, points_input: str) -> None:
        points: list = points_input.split()
        student: Student = self.get_student(points[0])

        if len(points) != 5:
            raise IncorrectPointsFormatError

        try:
            scores = [int(point) for point in points[1:]]
            new_scores = ScoreCard(student.id)
            new_scores.add_scores(scores)
            self.update_course_statistics(new_scores)
            student.score_card.add_scores(scores)

        except ValueError:
            raise IncorrectPointsFormatError

    def update_course_statistics(self, score_card: ScoreCard) -> None:
        """ Update db course stats based on new scorecard """
        student = self.db.get_student(score_card.student_id)
        for course_name, stats in score_card.courses.items():
            course = self.db.get_course(course_name)
            new_points = stats["points"]
            self.db.update_completed_course(student, course_name, new_points)
            self.db.update_enrolled_course(student, course_name, new_points)
            course.total_score += new_points
            course.submissions += 1
            course.set_avg_score()

    def get_course_statistics(self, course_name: str) -> list:
        course = self.db.get_course(course_name)
        if course:
            enrolled_students = self.db.get_enrolled_students_ids(course_name)
            stats = []
            if enrolled_students:
                for student_id in enrolled_students:
                    score_card = self.db.get_student_course(student_id, course_name)
                    points = score_card["points"]
                    completed = self.get_progression_percentage(course_name, points)
                    stats.append((student_id, points, f"{completed}%"))
            sorted_stats = sorted(stats, key=lambda x: (-x[1], x[0]))
            return sorted_stats
        else:
            raise NoCourseError

    def get_progression_percentage(self, course_name: str, points: int) -> float:
        threshold = self.db.course_table[course_name].pass_threshold
        percentage = (points / threshold) * 100
        rounded_percentage = round(percentage, 1)
        return rounded_percentage

    def get_student(self, student_id: str) -> Student:
        try:
            int_id: int = int(student_id)
        except ValueError:
            raise NoStudentError(student_id)

        student: Student = self.db.get_student(int_id)
        if student is None:
            raise NoStudentError(student_id)

        return student

    def get_courses_maxmin(self, attribute: str) -> tuple[Union[list[str], str], Union[list[str], str]]:
        """ Gets the courses with maximum and minimum value of {attribute} from the db """
        courses = self.db.get_courses_by_attribute(attribute)

        if courses:
            values = [getattr(course, attribute) for course in courses]
            most_extreme_value = max(values)
            least_extreme_value = min(values)

            max_courses = [course.name for course in courses
                           if getattr(course, attribute) == most_extreme_value]
            min_courses = [course.name for course in courses
                           if getattr(course, attribute) == least_extreme_value
                           and course.name not in max_courses]

            return self.joined_courses(max_courses),\
                self.joined_courses(min_courses)

        return "n/a", "n/a"

    def get_new_notifications(self) -> dict:
        """ Returns a dictionary with student_id and its notifications """
        new_notifications = self.db.to_be_notified
        formatted_notifications = {}
        if new_notifications:
            for student_id, courses in new_notifications.items():
                student = self.db.get_student(student_id)
                formatted_notes = self.format_notifications(student, courses)
                formatted_notifications[student_id] = formatted_notes
            self.clear_notifications()
        return formatted_notifications

    def clear_notifications(self):
        self.db.to_be_notified.clear()

    @staticmethod
    def format_notifications(student: Student, courses: list) -> list:
        message = (
            "To: {}\n"
            "Re: Your Learning Progress\n"
            "Hello, {} {}! You have accomplished our {} course!"
        )
        formatted_notes = [
            message.format(
                student.email,
                student.first_name,
                student.last_name,
                course.capitalize()
            )
            for course in courses
        ]
        return formatted_notes

    @staticmethod
    def joined_courses(courses: list) -> str:
        if len(courses) <= 1:
            return courses[0] if courses else "N/A"
        return ", ".join(courses)

