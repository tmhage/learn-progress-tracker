class CustomException(Exception):
    def __str__(self) -> str:
        return f"{super().__str__()}" or f"{self.__doc__}"


class InvalidInputError(CustomException):
    """Input is invalid."""


class NoInputError(InvalidInputError):
    """No Input."""


class NotEnoughWordsError(InvalidInputError):
    """Incorrect credentials."""


class EmailExistsError(InvalidInputError):
    """This email is already taken."""


class NoStudentError(InvalidInputError):
    """No student is found for id="""
    def __init__(self, user_id=None):
        super().__init__(f"{self.__doc__}{user_id}")


class IncorrectPointsFormatError(InvalidInputError):
    """Incorrect points format."""


class EmailError(InvalidInputError):
    """Incorrect email."""


class LastNameError(InvalidInputError):
    """Incorrect last name."""


class FirstNameError(InvalidInputError):
    """Incorrect first name."""


class NoCourseError(InvalidInputError):
    """Unknown course."""
