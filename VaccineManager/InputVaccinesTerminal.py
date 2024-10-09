import datetime


def input_vaccines_terminal():
    vaccine_number = 1
    input_str = input("Do you want to enter a new vaccine? (Yes/No)\n")
    user_vaccines = []
    while get_input_answer(input_str):
        print("---------------------ADDING VACCINE---------------------")
        vaccine_name, doses, dose_times = input_vaccine(vaccine_number)
        if vaccine_name is not None and doses is not None and dose_times is not None:
            user_vaccines.append((vaccine_name, doses, dose_times))
            vaccine_number += 1
        input_str = input("Do you want to enter another vaccine? (Yes/No)\n")

    return user_vaccines


def get_input_int(input_str: str) -> int:
    try:
        return int(input_str)
    except Exception:
        input_str = input("Input was not an int, please try again.\n")
        return get_input_int(input_str)


def get_input_date(input_str: str) -> datetime:
    try:
        return datetime.datetime.strptime(input_str, '%d/%m/%y')
    except Exception:
        input_str = input("Input was not in the correct format, please try again.\n"
                          "The input format is: 'day/month/year'.\n")
        return get_input_date(input_str)


def get_input_answer(input_str: str) -> bool:
    if input_str.upper() == "YES" or input_str.upper() == "Y":
        return True
    if input_str.upper() == "NO" or input_str.upper() == "N":
        return False

    input_str = input("Input was not in the correct format, please answer 'yes' or 'no'.\n")
    return get_input_answer(input_str)


def input_vaccine(vaccine_number: int):
    # Ask for vaccine name
    input_str = input("Enter name of vaccine " + str(vaccine_number) + ".\nEnter 'abort' to abort procedure.\n")
    if input_str == "abort": return None, None, None
    vaccine_name = input_str

    # Ask for amount of doses
    input_str = input("Enter number of doses of " + vaccine_name + ".\nEnter 'abort' to abort procedure.\n")
    if input_str == "abort": return None, None, None
    doses = get_input_int(input_str)

    # Ask for times of each dose
    dose_times = []
    for dose_number in range(1, doses + 1):
        input_str = input("Enter date of dose " + str(dose_number) +
                          ".\n"
                          "The input format is: 'day/month/year'.\n"
                          "Enter 'abort' to abort procedure.\n")
        if input_str == "abort": return None, None, None
        dose_time = get_input_date(input_str)
        dose_times.append(dose_time)

    return vaccine_name, doses, dose_times
