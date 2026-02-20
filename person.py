

class Person:
    """Person class representing an individual in the family tree."""

    MALE = "male"
    FEMALE = "female"
    YEARSTART = 1950
    YEAREND = 2120

    def __init__(
        self,
        yearBorn,
        yearDied,
        fName,
        lName,
        gender,
        partner=None,
        children=None,
        parent1=None,
        parent2=None,
    ):
        yearBorn = self.validateYearAllowOver(yearBorn)
        yearDied = self.validateYearAllowOver(yearDied)
        fName = self.validateName(fName)
        lName = self.validateName(lName)
        gender = self.validateGender(gender)
        self._yearBorn = yearBorn
        self._yearDied = yearDied
        self.fName = fName
        self.lName = lName
        self.gender = gender
        self.partner = partner
        self.children = children if children is not None else []
        self.parent1 = parent1
        self.parent2 = parent2

    @property
    def yearBorn(self):
        return self._yearBorn

    @property
    def yearDied(self):
        return self._yearDied

    @property
    def fName(self):
        return self._fName

    @property
    def lName(self):
        return self._lName

    @property
    def partner(self):
        return self._partner

    @property
    def children(self):
        return self._children

    @property
    def gender(self):
        return self._gender

    @property
    def parent1(self):
        return self._parent1

    @property
    def parent2(self):
        return self._parent2

    @yearBorn.setter
    def yearBorn(self, val):
        intVal = int(val)
        if intVal < Person.YEARSTART:
            raise ValueError(
                f"ERROR VALIDATING YEAR: year in range "
                f"{Person.YEARSTART}-{Person.YEAREND} expected"
            )
        self._yearBorn = intVal
        if intVal > Person.YEAREND:
            raise YearEndError("ERROR VALIDATING YEAR: year above 2120")

    @yearDied.setter
    def yearDied(self, val):
        intVal = int(val)
        if intVal < Person.YEARSTART:
            raise ValueError(
                f"ERROR VALIDATING YEAR: year in range "
                f"{Person.YEARSTART}-{Person.YEAREND} expected"
            )
        self._yearDied = intVal
        if intVal > Person.YEAREND:
            raise YearEndError("ERROR VALIDATING YEAR: year above 2120")

    @fName.setter
    def fName(self, val):
        checked = Person.validateName(val)
        self._fName = checked

    @lName.setter
    def lName(self, val):
        checked = Person.validateName(val)
        self._lName = checked

    @partner.setter
    def partner(self, val):
        if val is None:
            self._partner = None
            return
        self._partner = Person.validatePerson(val)

    @children.setter
    def children(self, val):
        if val is None:
            self._children = []
            return
        if isinstance(val, Person):
            self._children = [val]
            return
        if isinstance(val, list):
            if all(isinstance(child, Person) for child in val):
                self._children = val
                return
            raise ValueError("children list must contain only Person instances")
        raise ValueError("person, [person], or None expected for set children")

    def addChild(self, val):
        val = self.validatePerson(val)
        self._children.append(val)

    @gender.setter
    def gender(self, val):
        checked = self.validateGender(val)
        self._gender = checked

    @parent1.setter
    def parent1(self, val):
        val = self.validatePersonAllowsNone(val)
        self._parent1 = val

    @parent1.setter
    def parent2(self, val):
        val = self.validatePersonAllowsNone(val)
        self._parent2 = val

    @classmethod
    def validateYear(cls, value):
        """Validate year is in range YEARSTART-YEAREND."""
        try:
            int_val = int(value)
            if int_val < cls.YEARSTART:
                raise ValueError(
                    f"ERROR VALIDATING YEAR: year in range "
                    f"{cls.YEARSTART}-{cls.YEAREND} expected"
                )
            elif int_val > cls.YEAREND:
                raise YearEndError("ERROR VALIDATING YEAR: year above 2120")
            return int_val
        except ValueError:
            raise ValueError("ERROR VALIDATING YEAR: expected int input")

    @classmethod
    def validateYearAllowOver(cls, value):
        """Validate year >= YEARSTART; allows > YEAREND."""
        try:
            int_val = int(value)
            if int_val < cls.YEARSTART:
                raise ValueError(
                    f"ERROR VALIDATING YEAR: year >= {cls.YEARSTART} expected"
                )
            return int_val
        except ValueError:
            raise ValueError("ERROR VALIDATING YEAR: expected int input")

    @staticmethod
    def validateName(value):
        """Validate first/last name."""
        if isinstance(value, str) and value.strip() != "":
            return value.strip()
        raise ValueError("ERROR VALIDATING NAME: expected string input")

    @staticmethod
    def validatePerson(value):
        """Validate input is a Person instance."""
        if isinstance(value, Person):
            return value
        raise ValueError("ERROR VALIDATING PERSON: expected person input")

    @staticmethod
    def validatePersonAllowsNone(value):
        """Validate input is Person or None."""
        if value is None or isinstance(value, Person):
            return value
        raise ValueError(
            "ERROR VALIDATING PERSON: expected person or None input"
        )

    @classmethod
    def validateGender(cls, value):
        """Validate and normalize gender input."""
        if isinstance(value, str):
            value = value.upper()
            if value in ("MALE", "M"):
                return "male"
            elif value in ("FEMALE", "F"):
                return "female"
            raise ValueError(
                "ERROR VALIDATING GENDER: expected MALE/M or FEMALE/F "
                "string values"
            )
        raise ValueError(
            "ERROR VALIDATING GENDER: expected int or string value"
        )

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        partner_str = None
        if self.partner is not None:
            partner_str = f"{self.partner.fName} {self.partner.lName}"

        children_str = []
        for child in (self.children or []):
            if isinstance(child, Person):
                children_str.append(f"{child.fName} {child.lName}")
            else:
                children_str.append(str(child))

        return (
            f"{self.fName} {self.lName}:\n"
            f"gender: {self.gender}\n"
            f"born: {self.yearBorn}\n"
            f"died: {self.yearDied}\n"
            f"partner: {partner_str}\n"
            f"children ({len(children_str)}): {children_str}\n"
        )


class YearEndError(Exception):
    """Raised when a year exceeds YEAREND (2120)."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
