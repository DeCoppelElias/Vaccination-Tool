import datetime


class Vaccine:
    def __init__(self, name: str, illnesses: list[str], doses: int, doses_intervals: list[datetime], doses_min_age: list[datetime]):
        self.name = name
        self.illnesses = illnesses
        self.doses = doses

        if len(doses_intervals) != doses - 1:
            raise Exception("Vaccine dose interval information does not match amount of doses: \n" + str(doses_intervals))

        if len(doses_min_age) != doses:
            print(doses_min_age)
            raise Exception("Vaccine min age information does not match amount of doses: \n" + str(doses_min_age))

        self.doses_intervals = doses_intervals
        self.doses_min_age = doses_min_age
