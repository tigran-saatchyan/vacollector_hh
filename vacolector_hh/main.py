import traceback

from vacolector_hh.constants import EMPLOYERS_LIST
from vacolector_hh.db_manager import DBManager
from vacolector_hh.file_handler import FileHandler
from vacolector_hh.parser_hh import HHParser


def delete_or_add_employer_selector() -> str:
    """
    Prompt the user to select an operation: delete employers, add employers, or continue to vacancies.

    Returns:
        str: User's selected operation.
    """
    user_input = input(
        "Please select Operation:\n"
        "0. Delete Employers\n"
        "1. Add employers\n"
        "2. Continue to vacancies\n"
        ">>> "
    )
    return user_input


def delete_all_or_one_employer_selector() -> str:
    """
    Prompt the user to select a deletion type: delete one employer by ID, delete all employers, or cancel.

    Returns:
        str: User's selected deletion type.
    """
    one_or_all_to_delete = input(
        "Please select deletion type:\n"
        "0. Remove one employer by ID\n"
        "1. Delete all employers\n"
        "2. Cancel\n"
        ">>> "
    )
    return one_or_all_to_delete


def employer_adding_type_selector() -> str:
    """
    Prompt the user to select an employer adding type: add from file, add by name, or continue.

    Returns:
        str: User's selected employer adding type.
    """
    adding_type = input(
        "Add employers to subscription list:\n"
        "0. Add from file\n"
        "1. Add employers by name\n"
        "2. Continue\n"
        ">>> "
    )
    return adding_type


def vacancy_operation_selector() -> str:
    """
    Prompt the user to select a vacancy operation: update vacancies or continue.

    Returns:
        str: User's selected vacancy operation.
    """
    vacancy_operation = input(
        "Please select operation:\n"
        "0. Update vacancies\n"
        "1. Continue\n"
        ">>> "
    )
    return vacancy_operation


def select_employer(employers: list) -> list:
    """
    Prompt the user to select employers from a list of employers with similar names.

    Args:
        employers (list): List of employers.

    Returns:
        list: Selected employers.
    """
    for i, employer in enumerate(employers):
        print(i, '-', employer)
    selected_employers = input(
        "Please select employers indexes from list of employers "
        "with similar names (separated by comma if more than 1 selected): "
    )

    selected_employers = [
        int(i.strip())
        if "," in selected_employers
        else int(selected_employers)
        for i in selected_employers.split(',')
    ]

    extracted_employers = [employers[index] for index in selected_employers]
    return extracted_employers


def add_by_employer_by_name(db_manager, hh_parser):
    """
    Add employers to the subscription list by employer name.

    Args:
        db_manager: Instance of the DBManager class.
        hh_parser: Instance of the HHParser class.
    """
    employers_list = input("Please enter employers name/names: ")
    if not employers_list:
        print(
            "You must enter at least one employer name or type "
            "CANCEL to cancel operation\n"
        )
        add_by_employer_by_name(db_manager, hh_parser)
    elif employers_list.lower() == "cancel":
        print("Operation canceled by user")
        return

    if ',' in employers_list:
        employers_list = employers_list.split(',')
    else:
        employers_list = [employers_list]

    for employer in employers_list:
        employers = hh_parser.parse_employers(employer)
        if len(employers) > 1:
            employers = select_employer(employers)
        db_manager.set_employers(employers)

    is_it_more_to_add = input("Do you want to add more employers? (y/n): ")

    if is_it_more_to_add == "y":
        add_by_employer_by_name(db_manager, hh_parser)
    elif is_it_more_to_add == "n":
        print("Operation canceled by user")
    else:
        print("Wrong input, Operation canceled")


def add_employers_from_file(db_manager, file_handler, hh_parser):
    """
    Add employers to the subscription list from a file.

    Args:
        db_manager: Instance of the DBManager class.
        file_handler: Instance of the FileHandler class.
        hh_parser: Instance of the HHParser class.
    """
    try:
        employers_list: list = file_handler.get_employers_from_file(
            EMPLOYERS_LIST
        )
        for employer in employers_list:
            employers = hh_parser.parse_employers(employer)
            if len(employers) > 1:
                employers = select_employer(employers)
            db_manager.set_employers(employers)
    except Exception:
        traceback.print_exc()


def add_employers(db_manager, file_handler, hh_parser):
    """
    Add employers to the subscription list.

    Args:
        db_manager: Instance of the DBManager class.
        file_handler: Instance of the FileHandler class.
        hh_parser: Instance of the HHParser class.
    """
    adding_type = employer_adding_type_selector()

    if adding_type == "0":  # from file
        add_employers_from_file(db_manager, file_handler, hh_parser)
        add_vacancies(db_manager, file_handler, hh_parser)
    elif adding_type == "1":  # by id
        add_by_employer_by_name(db_manager, hh_parser)
        add_vacancies(db_manager, file_handler, hh_parser)
    elif adding_type == "2":  # Continue
        add_vacancies(db_manager, file_handler, hh_parser)
    else:
        print("Wrong input, Please select from listed")
        add_employers(db_manager, file_handler, hh_parser)


def delete_one_employer(db_manager, file_handler):
    """
    Delete one employer by ID.

    Args:
        db_manager: Instance of the DBManager class.
        file_handler: Instance of the FileHandler class.
    """
    employers_id = input("Please enter employers ID: ")
    db_manager.delete_employer(employers_id)
    print(f"Employer with ID {employers_id} successfully deleted.")
    more_to_delete = input("Do you want to delete more employers? (y/n): ")
    if more_to_delete == "y":
        delete_one_employer(db_manager, file_handler)
    elif more_to_delete == "n":
        print("Operation canceled by user")
    else:
        print("Wrong input, Please select from listed")
        delete_one_employer(db_manager, file_handler)


def delete_all_employers(db_manager, file_handler, hh_parser):
    """
    Delete all employers.

    Args:
        db_manager: Instance of the DBManager class.
        file_handler: Instance of the FileHandler class.
        hh_parser: Instance of the HHParser class.
    """
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
        print("Operation canceled by user")
    else:
        print("Wrong input, Please select from listed")
        delete_all_employers(db_manager, file_handler, hh_parser)


def delete_employers(db_manager, file_handler, hh_parser):
    """
    Perform employer deletion operations.

    Args:
        db_manager: Instance of the DBManager class.
        file_handler: Instance of the FileHandler class.
        hh_parser: Instance of the HHParser class.
    """
    one_or_all_to_delete = delete_all_or_one_employer_selector()

    if one_or_all_to_delete == "0":
        delete_one_employer(db_manager, file_handler)
        add_employers(db_manager, file_handler, hh_parser)
    elif one_or_all_to_delete == "1":
        delete_all_employers(db_manager, file_handler, hh_parser)
        add_employers(db_manager, file_handler, hh_parser)


def get_all_vacancies_from_api(db_manager, hh_parser) -> list:
    """
    Retrieve all vacancies from the API.

    Args:
        db_manager: Instance of the DBManager class.
        hh_parser: Instance of the HHParser class.

    Returns:
        list: List of all vacancies.
    """
    all_vacancies = []
    all_employers = db_manager.get_employers()
    if all_employers:
        for employer_id in all_employers:
            all_vacancies.extend(hh_parser.parse_vacancies(employer_id))
        return all_vacancies
    else:
        print("No employers found")


def update_vacancies_from_remote(db_manager, file_handler, hh_parser):
    """
    Update vacancies from the remote API.

    Args:
        db_manager: Instance of the DBManager class.
        file_handler: Instance of the FileHandler class.
        hh_parser: Instance of the HHParser class.
    """
    vacancies = get_all_vacancies_from_api(db_manager, hh_parser)
    if not vacancies:
        print("No Vacancies found by selected employers")
        add_employers(db_manager, file_handler, hh_parser)

    db_manager.set_vacancies(vacancies)


def db_data_handling_menu() -> str:
    """
    Display the database data handling menu and prompt the user to select an operation.

    Returns:
        str: User's selected operation.
    """
    vacancy_operation = input(
        "Please select operation:\n"
        "0. Get all companies and open vacancies count\n"
        "1. Get all vacancies\n"
        "2. Get average salary\n"
        "3. Get vacancies with salary above average\n"
        "4. Get vacancies by keyword\n"
        "5. Exit\n"
        ">>> "
    )
    return vacancy_operation


def to_be_continued(db_manager):
    """
    Prompt the user to continue or exit from the app.

    Args:
        db_manager: Instance of the DBManager class.
    """
    to_continue = input(
        "Please select option to continue or to exit from app: \n"
        "1. Continue\n"
        "0. Exit\n"
        ">>> "
    )

    if to_continue == "1":
        local_vacancies_interaction(db_manager)
    else:
        print("Have a nice day! Bye Bye!")
        exit()


def print_vacancies(vacancies):
    """
    Print a list of vacancies.

    Args:
        vacancies (list): List of vacancies.
    """
    for vacancy in vacancies:
        employer_name, \
            vacancy_name, \
            salary_from, \
            salary_to, \
            currency, \
            alternate_url = vacancy

        print("Company: ", employer_name)
        print("Vacancy: ", vacancy_name)
        print("Salary: ", salary_from, " - ", salary_to, " ", currency)
        print("URL: ", alternate_url)
        print("-" * 40)


def get_companies_and_vacancies_count(db_manager):
    """
    Retrieve all companies and their open vacancies count from the database.

    Args:
        db_manager: Instance of the DBManager class.
    """
    companies = db_manager.get_companies_and_vacancies_count()
    for company in companies:
        employer, vacancy_count = company
        print("Company: ", employer)
        print("Open Vacancies: ", vacancy_count)
        print("-" * 40)
    to_be_continued(db_manager)


def get_all_vacancies(db_manager):
    """
    Retrieve all vacancies from the database.

    Args:
        db_manager: Instance of the DBManager class.
    """
    vacancies = db_manager.get_all_vacancies()
    print_vacancies(vacancies)
    to_be_continued(db_manager)


def get_avg_salary(db_manager):
    """
    Retrieve the average salary from the database.

    Args:
        db_manager: Instance of the DBManager class.
    """
    avg_salary = db_manager.get_avg_salary()
    print(avg_salary)
    to_be_continued(db_manager)


def get_vacancies_with_higher_salary(db_manager):
    """
    Retrieve vacancies with salary above average from the database.

    Args:
        db_manager: Instance of the DBManager class.
    """
    vacancies = db_manager.get_vacancies_with_higher_salary()
    print_vacancies(vacancies)
    to_be_continued(db_manager)


def get_vacancies_with_keyword(db_manager):
    """
    Retrieve vacancies containing a specific keyword from the database.

    Args:
        db_manager: Instance of the DBManager class.
    """
    keyword = input("Enter a keyword: ")
    vacancies = db_manager.get_vacancies_with_keyword(keyword)
    print_vacancies(vacancies)
    to_be_continued(db_manager)


def local_vacancies_interaction(db_manager):
    """
    Perform database data handling operations.

    Args:
        db_manager: Instance of the DBManager class.
    """
    user_selected_operation = db_data_handling_menu()
    if user_selected_operation == '0':
        get_companies_and_vacancies_count(db_manager)
    elif user_selected_operation == '1':
        get_all_vacancies(db_manager)
    elif user_selected_operation == '2':
        get_avg_salary(db_manager)
    elif user_selected_operation == '3':
        get_vacancies_with_higher_salary(db_manager)
    elif user_selected_operation == '4':
        get_vacancies_with_keyword(db_manager)
    else:
        print("Have a nice day! Bye Bye!")
        exit()


def add_vacancies(db_manager, file_handler, hh_parser):
    """
    Add vacancies to the database.

    Args:
        db_manager: Instance of the DBManager class.
        file_handler: Instance of the FileHandler class.
        hh_parser: Instance of the HHParser class.
    """
    vacancy_action = vacancy_operation_selector()

    if vacancy_action == "0":
        update_vacancies_from_remote(db_manager, file_handler, hh_parser)
        local_vacancies_interaction(db_manager)
    elif vacancy_action == "1":
        local_vacancies_interaction(db_manager)
    else:
        print("Wrong input, Please select from listed")
        add_vacancies(db_manager, file_handler, hh_parser)


def user_interaction(db_manager, file_handler, hh_parser):
    """
    Perform user interaction and operations.

    Args:
        db_manager: Instance of the DBManager class.
        file_handler: Instance of the FileHandler class.
        hh_parser: Instance of the HHParser class.
    """
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


def print_header():
    """
    Print the application header.
    """
    print("-" * 40)
    print("|     Welcome to Va-collector app!     |")
    print("-" * 40)


def main():
    file_handler = FileHandler()
    db_manager = DBManager()
    hh_parser = HHParser()

    db_manager.create_database()
    is_exists = db_manager.is_tables_existing()

    if not is_exists:
        db_manager.create_tables()

    print_header()

    user_interaction(db_manager, file_handler, hh_parser)


if __name__ == '__main__':
    main()
