import os

from vacolector_hh.constants import CODE_DIR
from vacolector_hh.db_manager import DBManager
from vacolector_hh.file_handler import FileHandler
from vacolector_hh.parser_hh import HHParser


def delete_or_add_employer_selector():
    user_input = input(
        "Please select action:\n"
        "0. Delete Employers\n"
        "1. Add employers\n"
        "2. Continue to vacancies\n"
        ">>> "
    )
    return user_input


def delete_all_or_one_employer_selector():
    one_or_all_to_delete = input(
        "Please select deletion type:\n"
        "0. Remove one employer by ID\n"
        "1. Delete all employers\n"
        "2. Cancel\n"
        ">>> "
    )
    return one_or_all_to_delete


def employer_adding_type_selector():
    adding_type = input(
        "Add employers to subscription list:\n"
        "0. Add from file\n"
        "1. Add by employers id\n"
        "2. Continue\n"
        ">>> "
    )
    return adding_type


def vacancy_operation_selector():
    vacancy_operation = input(
        "Please select operation:\n"
        "0. Update vacancies\n"
        "1. Continue\n"
        ">>> "
    )
    return vacancy_operation


def add_by_employer_by_id(db_manager):
    employers_id = input("Please enter employers ID: ")
    db_manager.set_employers([employers_id])
    is_it_more_to_add = input("Do you want to add more employers? (y/n): ")
    if is_it_more_to_add == "y":
        add_by_employer_by_id(db_manager)
    elif is_it_more_to_add == "n":
        print("Action canceled by user")


def add_employers_from_file(db_manager, file_handler):
    try:
        employers_list: list = file_handler.get_employers_from_file(
            os.path.join(CODE_DIR, 'employer.txt')
        )
        db_manager.set_employers(employers_list)
    except Exception as e:
        print("message:", e)


def add_employers(db_manager, file_handler, hh_parser):
    adding_type = employer_adding_type_selector()

    if adding_type == "0":  # from file
        add_employers_from_file(db_manager, file_handler)
        add_vacancies(db_manager, file_handler, hh_parser)
    elif adding_type == "1":  # by id
        add_by_employer_by_id(db_manager)
        add_vacancies(db_manager, file_handler, hh_parser)
    elif adding_type == "2":  # Continue
        add_vacancies(db_manager, file_handler, hh_parser)
    else:
        print("Wrong input, Please select from listed")
        add_employers(db_manager, file_handler, hh_parser)


def delete_one_employer(db_manager, file_handler):
    employers_id = input("Please enter employers ID: ")
    db_manager.delete_employer(employers_id)
    print(f"Employer with ID {employers_id} successfully deleted.")
    more_to_delete = input("Do you want to delete more employers? (y/n): ")
    if more_to_delete == "y":
        delete_one_employer(db_manager, file_handler)
    elif more_to_delete == "n":
        print("Action canceled by user")
    else:
        print("Wrong input, Please select from listed")
        delete_one_employer(db_manager, file_handler)


def delete_all_employers(db_manager, file_handler, hh_parser):
    user_confirmation = input(
        "Are you sure you want to delete all employers? (y/n): "
    )
    if user_confirmation == "y":
        try:
            db_manager.delete_employer()
            print(f"Employers successfully deleted.")
        except Exception as e:
            print(e)
    elif user_confirmation == "n":
        print("Action canceled by user")
    else:
        print("Wrong input, Please select from listed")
        delete_all_employers(db_manager, file_handler, hh_parser)


def delete_employers(db_manager, file_handler, hh_parser):
    one_or_all_to_delete = delete_all_or_one_employer_selector()

    if one_or_all_to_delete == "0":
        delete_one_employer(db_manager, file_handler)
        add_employers(db_manager, file_handler, hh_parser)
    elif one_or_all_to_delete == "1":
        delete_all_employers(db_manager, file_handler, hh_parser)
        add_employers(db_manager, file_handler, hh_parser)


def update_vacancies_from_remote(db_manager, file_handler, hh_parser):
    all_vacancies = []
    all_employers = db_manager.get_employers()

    for employer_id in all_employers:
        all_vacancies.extend(hh_parser.parse_vacancies(employer_id))


def local_vacancies_interaction(db_manager, file_handler):
    pass


def add_vacancies(db_manager, file_handler, hh_parser):
    vacancy_action = vacancy_operation_selector()

    if vacancy_action == "0":
        update_vacancies_from_remote(db_manager, file_handler, hh_parser)
    elif vacancy_action == "1":  # by id
        local_vacancies_interaction(db_manager, file_handler)
    else:
        print("Wrong input, Please select from listed")
        add_vacancies(db_manager, file_handler, hh_parser)


def user_interaction(db_manager, file_handler, hh_parser):

    delete_or_add_employers = delete_or_add_employer_selector()

    if delete_or_add_employers == "0":  # Delete
        delete_employers(db_manager, file_handler, hh_parser)
    elif delete_or_add_employers == "1":  # Add
        add_employers(db_manager, file_handler, hh_parser)
    elif delete_or_add_employers == "2":  # Continue
        add_vacancies(db_manager, file_handler, hh_parser)
    else:
        print("Wrong input, Please select from listed")
        user_interaction(db_manager, file_handler, hh_parser)


def main():
    file_handler = FileHandler()
    db_manager = DBManager()
    hh_parser = HHParser()
    print("Welcome to Va-collector app!")
    print("-" * 40)
    user_interaction(db_manager, file_handler, hh_parser)


if __name__ == '__main__':
    main()
