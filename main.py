from controller import Controller
from database import Database
from exceptions import InvalidInputError, NoInputError, NoStudentError
from typing import Union


def get_validated_input(prompt: str = "") -> Union[str, None]:
    while True:
        user_input = input(prompt).strip().lower()
        if not user_input:
            raise NoInputError
        elif user_input == "back":
            return None
        else:
            return user_input


def add_students() -> None:
    print("Enter student credentials or 'back' to return:")
    newly_added_counter = 0

    while True:
        try:
            student_input = get_validated_input()
            if student_input:
                controller.add_student(student_input)
                print("The student has been added.")
                newly_added_counter += 1
            else:
                print("Total {} students have been added.".format(newly_added_counter))
                return None
        except InvalidInputError as e:
            print(e)


def add_points() -> None:
    print("Enter an id and points or 'back' to return")

    while True:
        try:
            points_input = get_validated_input()
            if points_input:
                controller.add_points(points_input)
                print("Points updated.")
            else:
                return None
        except InvalidInputError as e:
            print(e)


def find() -> None:
    print("Enter an id or 'back' to return:")

    while True:
        try:
            find_input = get_validated_input()
            if find_input:
                student = controller.get_student(find_input)
                print(student.score_card)
            else:
                return None
        except InvalidInputError as e:
            print(e)


def list_student_ids() -> None:
    student_ids = controller.get_all_student_ids()
    if student_ids:
        print("Students:")
        for student_id in student_ids:
            print(student_id)
    else:
        print("No students found.")


def exit_program():
    print("Bye!")
    exit()


def print_statistics() -> None:
    attributes = [
        ("enrolled", "Most popular", "Least popular"),
        ("submissions", "Highest activity", "Lowest activity"),
        ("avg_score", "Easiest course", "Hardest course")]

    for attribute, most_label, least_label in attributes:
        most_courses, least_courses = controller.get_courses_maxmin(attribute)
        print(f"{most_label}: {most_courses}")
        print(f"{least_label}: {least_courses}")


def statistics():
    print("Type the name of a course to see details or 'back' to quit")
    print_statistics()

    while True:
        course = get_validated_input()

        if course:
            try:
                course_stats = controller.get_course_statistics(course)
                print(course.capitalize())
                print("{:<6}{:<10}{:5}".format("id", "points", "completed"))

                if course_stats:
                    for stat in course_stats:
                        student_id, points, completed = stat
                        print("{:<6}{:<10}{:<5}".format(student_id, points, completed))

            except InvalidInputError as e:
                print(e)
        else:
            return None


def notify():
    new_notifications = controller.get_new_notifications()
    total_students_notified = len(new_notifications)

    for notifications in new_notifications.values():
        for note in notifications:
            print(note)

    print(f"Total {total_students_notified} students have been notified.")


def main():
    cmd_dict = {
        'exit': exit_program,
        'add students': add_students,
        'list': list_student_ids,
        'add points': add_points,
        'find': find,
        'statistics': statistics,
        'notify': notify
    }

    print("Learning progress tracker")

    while True:
        try:
            cmd = get_validated_input()
            if cmd is None:
                print("Enter 'exit' to exit the program")
            elif cmd in cmd_dict:
                cmd_dict[cmd]()
            else:
                print("Error: unknown command!")
        except InvalidInputError as e:
            print(e)


if __name__ == "__main__":
    controller = Controller(Database())
    main()
