import os

from VaccineManager.Vaccine import Vaccine
import datetime
import pandas as pd
from VaccineManager.InputVaccinesTerminal import input_vaccines_terminal, get_input_date


class VaccineManager:
    def __init__(self):
        exe_dir = os.path.dirname(os.path.abspath(__file__))
        self.excel_dir = os.path.abspath(os.path.join(exe_dir, '../ExcelFiles'))

        self.initialised = False

        self.illnesses = []
        self.vaccines = []

        self.df_illnesses = None
        self.df_vaccines = None
        self.df_intervals = None
        self.df_min_ages = None

        self.excel_illnesses_path = os.path.abspath(os.path.join(self.excel_dir, 'Illnesses.xlsx'))
        self.excel_vaccines_path = os.path.abspath(os.path.join(self.excel_dir, 'Vaccines.xlsx'))
        self.excel_intervals_path = os.path.abspath(os.path.join(self.excel_dir, 'VaccineIntervals.xlsx'))
        self.excel_min_ages_path = os.path.abspath(os.path.join(self.excel_dir, 'VaccineMinimumAges.xlsx'))

        self.last_mod_time_illnesses = None
        self.last_mod_time_vaccines = None
        self.last_mod_time_intervals = None
        self.last_mod_time_min_ages = None

        self.reLoadVaccines()

    def checkExcelsExist(self):
        if os.path.isfile(self.excel_vaccines_path) and \
                os.path.isfile(self.excel_intervals_path) and \
                os.path.isfile(self.excel_min_ages_path) and \
                os.path.isfile(self.excel_illnesses_path):
            return True

        return False

    def checkExcelsModified(self):
        current_modification_time_vaccines = os.path.getmtime(self.excel_vaccines_path)
        current_modification_time_intervals = os.path.getmtime(self.excel_intervals_path)
        current_modification_time_min_ages = os.path.getmtime(self.excel_min_ages_path)
        current_modification_time_illnesses = os.path.getmtime(self.excel_illnesses_path)
        if self.last_mod_time_vaccines is not None and \
                self.last_mod_time_intervals is not None and \
                self.last_mod_time_min_ages is not None and \
                self.last_mod_time_illnesses is not None and \
                current_modification_time_vaccines == self.last_mod_time_vaccines and \
                current_modification_time_intervals == self.last_mod_time_intervals and \
                current_modification_time_min_ages == self.last_mod_time_min_ages and \
                current_modification_time_illnesses == self.last_mod_time_illnesses:
            return False
        return True

    def reLoadVaccines(self):
        if not self.checkExcelsExist():
            print("reload failed: excel files missing")
            return

        if not self.checkExcelsModified():
            return

        # update modification times
        self.last_mod_time_illnesses = os.path.getmtime(self.excel_illnesses_path)
        self.last_mod_time_vaccines = os.path.getmtime(self.excel_vaccines_path)
        self.last_mod_time_intervals = os.path.getmtime(self.excel_intervals_path)
        self.last_mod_time_min_ages = os.path.getmtime(self.excel_min_ages_path)

        # load in dataframes
        self.df_illnesses = pd.read_excel(self.excel_illnesses_path)
        self.df_vaccines = pd.read_excel(self.excel_vaccines_path)
        self.df_intervals = pd.read_excel(self.excel_intervals_path)
        self.df_min_ages = pd.read_excel(self.excel_min_ages_path)

        self.vaccines = []
        for index, row in self.df_vaccines.iterrows():
            name = row["name"]
            illness = [row["illness"]]
            doses = row["doses"]
            intervals = getIntervals(name, self.df_intervals)
            min_ages = getMinimumAges(name, self.df_min_ages)

            vaccine = Vaccine(
                name,
                illness,
                doses,
                intervals,
                min_ages)
            self.vaccines.append(vaccine)

        self.illnesses = []
        for index, row in self.df_illnesses.iterrows():
            name = row["name"]
            self.illnesses.append(name)

        self.initialised = True

    def check_vaccines(self, user_vaccines, birthday):
        remark_dict = {}
        for illness in self.illnesses:
            remark_dict[illness] = []

        covered_illnesses = get_covered_illnesses(self.vaccines, user_vaccines)

        # Check if all illnesses are covered
        for illness in self.illnesses:
            if covered_illnesses.count(illness) == 0:
                remark_dict[illness].append("Patient is missing a vaccine for this illness.")

        # Check if vaccines are correctly taken
        for vaccine_name, doses, dose_times in user_vaccines:
            vaccine = get_vaccine(self.vaccines, vaccine_name)

            # Check if all doses are taken
            if doses != vaccine.doses:
                if doses < vaccine.doses:
                    for illness in vaccine.illnesses:
                        remark_dict[illness].append(vaccine.name +
                                                    ": Patient is missing some doses. " +
                                                    str(doses) + "/" + str(vaccine.doses))
                elif doses > vaccine.doses:
                    for illness in vaccine.illnesses:
                        remark_dict[illness].append(vaccine.name +
                                                    ": Patient has too many doses. " +
                                                    str(doses) + "/" + str(vaccine.doses))

            # Check dose time intervals
            for i in range(1, len(dose_times)):
                current_interval = dose_times[i] - dose_times[i - 1]
                min_interval = vaccine.doses_intervals[i - 1]
                if current_interval < min_interval:
                    for illness in vaccine.illnesses:
                        remark_dict[illness].append(vaccine.name +
                                                    ": Dose " + str(i - 1) + "-" + str(i) +
                                                    " interval is too small.\n" +
                                                    "Vaccine interval: " + str(min_interval) + "\n" +
                                                    "Patient interval: " + str(current_interval))

            # Check minimum age
            for i in range(len(dose_times)):
                current_age = dose_times[i] - birthday
                min_age = vaccine.doses_min_age[i]
                if current_age < min_age:
                    for illness in vaccine.illnesses:
                        remark_dict[illness].append(vaccine.name +
                                                    ": Dose " + str(i) + " patient age is too small.\n" +
                                                    "Vaccine minimum age: " + str(min_age) + "\n" +
                                                    "Patient age : " + str(current_age))

            # If there are no remarks for the illness then that means that the patient is protected
            for illness in vaccine.illnesses:
                if len(remark_dict[illness]) == 0:
                    remark_dict[illness].append("Patient is protected from this illness with vaccine: " + vaccine.name)

        return remark_dict


def getIntervals(name: str, df) -> list[datetime]:
    intervals = df[df['name'] == name].sort_values(by='dose')['interval (weeks)'].tolist()

    interval_dates = []
    for interval in intervals:
        interval_date = datetime.timedelta(weeks=interval)
        interval_dates.append(interval_date)

    return interval_dates


def getMinimumAges(name: str, df) -> list[datetime]:
    min_ages = df[df['name'] == name].sort_values(by='dose')['minimum age (weeks)'].tolist()

    min_age_dates = []
    for min_age in min_ages:
        min_age_date = datetime.timedelta(weeks=min_age)
        min_age_dates.append(min_age_date)

    return min_age_dates


def get_covered_illnesses(vaccines: list[Vaccine], user_vaccines):
    covered_illnesses = []
    for vaccine_name, _, _ in user_vaccines:
        vaccine = get_vaccine(vaccines, vaccine_name)

        if vaccine is None:
            raise Exception("A user vaccine is not supported by the system: " + vaccine_name)

        covered_illnesses.extend(vaccine.illnesses)

    return covered_illnesses


def get_vaccine(vaccines: list[Vaccine], vaccine_name: str) -> Vaccine:
    vaccine = None
    for current_vaccine in vaccines:
        if current_vaccine.name == vaccine_name:
            vaccine = current_vaccine
            break
    if vaccine is None:
        raise Exception("A user vaccine is not supported by the system: " + vaccine_name)

    return vaccine
