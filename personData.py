import copy
import math
import random

from person import Person


class PersonData:
    """
    PersonData reads CSV files containing data about people.
    Creates dictionaries used to randomly generate person attributes.
    """

    birthAndMarriageFile = "birth_and_marriage_rates.csv"
    fNamesFile = "first_names.csv"
    genderNameProbFile = "gender_name_probability.csv"
    lNamesFile = "last_names.csv"
    lifeExpectancyFile = "life_expectancy.csv"
    rankToProbFile = "rank_to_probability.csv"

    def __init__(self):
        print("Reading files...")

        self._readBAM()              # sets birthDict and marriageDict dictionaries
        self._readFNames()           # sets firstNameDict dictionary
        self._readLNames()           # sets lastNameDict dictionary
        self._readLifeExpec()        # sets expectancyDict dictionary
        self._readRankToProb()       # sets rankDict dictionary

        print("File read complete!")

    def _readBAM(self):
        """Read birth and marriage file; set birthDict and marriageDict."""
        with open(self.birthAndMarriageFile) as f:
            f.readline()
            birth_rates = {}
            marriage_rates = {}
            for line in f.readlines():
                data = line.split(",")
                year = int(data[0][:4])
                birth = float(data[1])
                marriage = float(data[2])
                birth_rates[year] = birth
                marriage_rates[year] = marriage
        self.birthDict = birth_rates
        self.marriageDict = marriage_rates

    def _readgenderNameProb(self):
        """Read gender_name_probability file (NOT NECESSARY)."""
        with open(self.genderNameProbFile) as f:
            f.readline()
            gender_name_probability = {}
            for line in f.readlines()[::2]:
                data = line.split(",")
                year = int(data[0][:4])
                m_prob = float(data[2])
                gender_name_probability[year] = m_prob
        self.genderNameProbability = gender_name_probability

    def _readFNames(self):
        """Read first_names.csv; produce dict with keys gender, year, name."""
        empty_year_container = {
            1950: {}, 1960: {}, 1970: {}, 1980: {}, 1990: {}, 2000: {},
            2010: {}, 2020: {}, 2030: {}, 2040: {}, 2050: {}, 2060: {},
            2070: {}, 2080: {}, 2090: {}, 2100: {}, 2110: {}, 2120: {},
        }
        first_names = {
            "male": empty_year_container,
            "female": copy.deepcopy(empty_year_container),
        }
        with open(self.fNamesFile) as f:
            f.readline()
            for line in f.readlines():
                data = line.split(",")
                year = int(data[0][:4])
                gender = data[1]
                name = data[2]
                frequency = float(data[3])
                first_names[gender][year][name] = frequency
        self.firstNameDict = first_names

    def _readLNames(self):
        """Read last_names.csv; produce dict with keys year, last name."""
        last_names = {
            1950: {}, 1960: {}, 1970: {}, 1980: {}, 1990: {}, 2000: {},
            2010: {}, 2020: {}, 2030: {}, 2040: {}, 2050: {}, 2060: {},
            2070: {}, 2080: {}, 2090: {}, 2100: {}, 2110: {}, 2120: {},
        }
        with open(self.lNamesFile) as f:
            f.readline()
            for line in f.readlines():
                data = line.split(",")
                year = int(data[0][:4])
                rank = int(data[1])
                last_name = data[2].strip()
                last_names[year][last_name] = rank
        self.lastNameDict = last_names

    def _readLifeExpec(self):
        """Read life_expectancy.csv; produce dict by year."""
        life_expectancy = {}
        with open(self.lifeExpectancyFile) as f:
            f.readline()
            for line in f.readlines():
                data = line.split(",")
                year = int(data[0])
                expectancy = float(data[1])
                life_expectancy[year] = expectancy
        self.expectancyDict = life_expectancy

    def _readRankToProb(self):
        """Read rank_to_probability.csv; return dict by rank."""
        with open(self.rankToProbFile) as f:
            all_data = f.readline().split(",")
        rank_to_probability = {}
        for i, d in enumerate(all_data, start=1):
            rank_to_probability[i] = float(d)
        self.rankDict = rank_to_probability

    def printFNames(self):
        """Print all first names by gender and decade."""
        print("MALE NAMES:")
        for year, info in self.firstNameDict["male"].items():
            print(f"\t{year}s:")
            for name, freq in info.items():
                print(f"\t\tName: {name}\tFrequency: {freq}")
        print("\nFEMALE NAMES:")
        for year, info in self.firstNameDict["female"].items():
            print(f"\t{year}s:")
            for name, freq in info.items():
                print(f"\t\tName: {name}\tFrequency: {freq}")

    def printLNames(self):
        """Print all last names by year."""
        for year, names in self.lastNameDict.items():
            print(f"{year}s:")
            for name, rank in names.items():
                print(f"name: {name}\trank:{rank}")

    def getYearDied(self, birth_year):
        """Return random year of death based on birth year."""
        birth_year = Person.validateYear(birth_year)
        expec = self.expectancyDict[birth_year]
        expec_year = expec + float(birth_year)
        return int(math.floor(random.uniform(expec_year - 10, expec_year + 10)))

    def getFName(self, birth_year, gender):
        """Return random first name based on birth year and gender."""
        birth_year = Person.validateYear(birth_year)
        decade = get_decade(birth_year)
        gender = Person.validateGender(gender)
        curr_dict = self.firstNameDict[gender][decade]
        return random.choices(
            list(curr_dict.keys()),
            weights=list(curr_dict.values()),
        )[0]

    def getLName(self, birth_year):
        """Return random last name based on birth year."""
        birth_year = Person.validateYear(birth_year)
        decade = get_decade(birth_year)
        curr_dict = self.lastNameDict[decade]
        return random.choices(
            list(curr_dict.keys()),
            weights=list(self.rankDict.values()),
        )[0]

    def getPartner(self, birth_year):
        """Return bool for having a partner based on birth year."""
        birth_year = Person.validateYear(birth_year)
        decade = get_decade(birth_year)
        marriage_rate = self.marriageDict[decade]
        single_rate = 1 - marriage_rate
        return random.choices(
            [True, False],
            weights=[marriage_rate, single_rate],
        )[0]

    def getChildren(self, birth_year):
        """Return number of children based on birth year."""
        birth_year = Person.validateYear(birth_year)
        decade = get_decade(birth_year)
        birth_rate = self.birthDict[decade]
        birth_high = birth_rate + 1.5
        birth_low = birth_rate - 1.5
        result = int(round(random.uniform(birth_low, birth_high)))
        return max(0, result)

    @staticmethod
    def getGender():
        """Return random gender (50/50)."""
        return random.choices(["male", "female"], weights=[1, 1])[0]

    def createPersonWOP(self, birth_year, gender=None):
        """Create person without parents, with randomized attributes."""
        birth_year = Person.validateYear(birth_year)
        if gender is None:
            gender = self.getGender()
        death_year = self.getYearDied(birth_year)
        first_name = self.getFName(birth_year, gender)
        last_name = self.getLName(birth_year)
        return Person(birth_year, death_year, first_name, last_name, gender)

    def createPersonWP(
        self,
        birth_year,
        parent1,
        parent2=None,
        lastName=None,
        siblings=None,
    ):
        """Create person with parents and randomized attributes."""
        birth_year = Person.validateYear(birth_year)
        parent1 = Person.validatePerson(parent1)
        parent2 = Person.validatePersonAllowsNone(parent2)

        gender = self.getGender()
        death_year = self.getYearDied(birth_year)

        first_name = self.getFName(birth_year, gender)
        if siblings:
            while first_name in siblings:
                first_name = self.getFName(birth_year, gender)

        if lastName is None:
            lastName = parent1.lName
            if parent2 is not None:
                lastName = random.choices(
                    [parent1.lName, parent2.lName],
                    weights=[1, 1],
                )[0]

        new_child = Person(
            birth_year,
            death_year,
            first_name,
            lastName,
            gender,
            None,
            None,
            parent1,
            parent2,
        )
        parent1.addChild(new_child)
        if parent2 is not None:
            parent2.addChild(new_child)

        return new_child

    def createPartner(self, existing):
        """Create a partner for the given person."""
        existing = Person.validatePerson(existing)
        existing_year = existing.yearBorn

        partner_year = random.randint(existing_year - 10, existing_year + 10)
        partner_year = max(Person.YEARSTART, min(Person.YEAREND, partner_year))
        new_person = self.createPersonWOP(partner_year)
        while new_person.fName == existing.fName:
            new_person.fName = self.getFName(
                new_person.yearBorn, new_person.gender
            )
        while new_person.lName == existing.lName:
            new_person.lName = self.getLName(new_person.yearBorn)

        existing.partner = new_person
        new_person.partner = existing
        return new_person

    def createChildren(self, parent1, parent2=None):
        """Create children for parent(s); return list of new children."""
        parent1 = Person.validatePerson(parent1)
        younger_parent = parent1
        if parent2 is not None:
            parent2 = Person.validatePerson(parent2)
            if parent2.yearBorn < parent1.yearBorn:
                younger_parent = parent2

        younger_year_born = younger_parent.yearBorn
        num_children = self.getChildren(younger_year_born)
        new_children = []

        if num_children == 1:
            new_children.append(
                self.createPersonWP(
                    younger_parent.yearBorn + 35, parent1, parent2
                )
            )
        elif num_children > 1:
            children_start = younger_parent.yearBorn + 25
            step = 20 / (num_children)
            current_year = children_start

            children_last_name = parent1.lName
            if parent2 is not None:
                children_last_name = random.choices(
                    [parent1.lName, parent2.lName],
                    weights=[1, 1],
                )[0]

            sibling_names = []
            for _ in range(num_children):
                new_child = self.createPersonWP(
                    current_year,
                    parent1,
                    parent2,
                    children_last_name,
                    sibling_names,
                )
                new_children.append(new_child)
                sibling_names.append(new_child.fName)
                current_year += step

        return new_children


def get_decade(year):
    """Return decade (e.g. 1985 -> 1980)."""
    return math.floor(year / 10) * 10
