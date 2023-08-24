import pytest
from models import Student
from database import Database
from exceptions import *


class TestStudent:
    def test_valid_student(self):
        student = Student("John", "Doe", "johndoe@example.com")
        assert student.first_name == "John"
        assert student.last_name == "Doe"
        assert student.email == "johndoe@example.com"

        student = Student("John", "Doe Bong", "johndoe@example.com")
        assert student.first_name == "John"
        assert student.last_name == "Doe Bong"
        assert student.email == "johndoe@example.com"

    def test_invalid_first_name(self):
        invalid_first_names = ["123", "$%&", "John@Doe", "-John", "John-"]
        for first_name in invalid_first_names:
            with pytest.raises(FirstNameError):
                Student(first_name, "Doe", "johndoe@example.com")

    def test_invalid_last_name(self):
        invalid_last_names = ["Doe-", "Doe'", "John$Doe", "Doe -Doe", "-Doe doe"]
        for last_name in invalid_last_names:
            with pytest.raises(LastNameError):
                Student("John", last_name, "johndoe@example.com")

    def test_invalid_email(self):
        invalid_emails = ["invalid-email", "johndoe@example", "john@doe@com"]
        for email in invalid_emails:
            with pytest.raises(EmailError):
                Student("John", "Doe", email)

