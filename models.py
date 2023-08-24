import re
from exceptions import *
from typing import Sequence


class ScoreCard:

    def __init__(self, student_id, courses=("python", "dsa", "databases", "flask")):
        self.student_id: int = student_id
        self.course_names = courses
        self.courses = {c: {"submissions": 0, "points": 0} for c in courses}

    def __str__(self) -> str:
        python_score = self.courses["python"]["points"]
        dsa_score = self.courses["dsa"]["points"]
        databases_score = self.courses["databases"]["points"]
        flask_score = self.courses["flask"]["points"]

        return "{} points: Python={}; DSA={}; Databases={}; Flask={}".format(
            self.student_id, python_score, dsa_score, databases_score, flask_score)

    def get_points(self, course_name):
        return self.courses[course_name]["points"]

    def add_scores(self, scores: Sequence[int]) -> None:
        for name, score in zip(self.course_names, scores):
            self.add_score(name, score)

    def add_score(self, name: str, score: int) -> None:
        self.courses[name]["points"] += self.validate_score(score)
        self.courses[name]["submissions"] += 1

    @staticmethod
    def validate_score(score: int) -> int:
        if not (0 <= score <= 1000):
            raise IncorrectPointsFormatError
        return score


class Student:

    __next_id = 1

    def __init__(self, first_name, last_name, email):
        self.id: int = Student.__get_next_id()
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.email: str = email
        self.score_card: ScoreCard = ScoreCard(self.id)

    @classmethod
    def __get_next_id(cls):
        next_id = cls.__next_id
        Student.__next_id += 1
        return next_id

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    @property
    def email(self):
        return self._email

    @first_name.setter
    def first_name(self, value):
        regex = r"^[A-Za-z]+('|-)?[A-Za-z]+$"
        if not re.match(regex, value):
            raise FirstNameError
        self._first_name = value

    @last_name.setter
    def last_name(self, value):
        regex = r"^([A-Za-z]+('|-)?[A-Za-z]+(('|-)?[A-Za-z]+)?\s?)*$"
        if not re.match(regex, value):
            raise LastNameError
        self._last_name = value

    @email.setter
    def email(self, value):
        regex = r"[\w.-]+@([-\w]+\.)+[\w]+$"
        if not re.match(regex, value):
            raise EmailError
        self._email = value

    @classmethod
    def from_str(cls, str_input: str):
        input_list = str_input.split()
        if len(input_list) < 3:
            raise NotEnoughWordsError
        first_name = input_list[0]
        last_name = " ".join(input_list[1:-1])
        email = input_list[-1]
        return cls(first_name, last_name, email)


class Course:

    def __init__(self, name: str, pass_threshold: int):
        self.name = name
        self.pass_threshold = pass_threshold
        self.enrolled_students = []
        self.submissions = 0
        self.completed = 0
        self.total_score = 0
        self.avg_score = 0

    @property
    def enrolled(self):
        return len(self.enrolled_students)

    def set_avg_score(self) -> None:
        if self.submissions > 0:
            self.avg_score = self.total_score / self.submissions
        else:
            self.avg_score = 0
