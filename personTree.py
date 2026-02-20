from person import Person, YearEndError
from personData import PersonData


class PersonTree:
    """
    PersonTree represents the family tree.
    Uses PersonData to generate roots and populate the tree.
    """

    pd = PersonData()

    def __init__(self):
        person_root1 = self.pd.createPersonWOP(Person.YEARSTART, Person.MALE)
        person_root2 = self.pd.createPersonWOP(Person.YEARSTART, Person.FEMALE)

        person_root1.partner = person_root2
        person_root2.partner = person_root1

        new_children = self.pd.createChildren(person_root1, person_root2)

        self.root1 = person_root1
        self.root2 = person_root2
        self.actionQueue = new_children

        self.generateTree()
        self.numPeople = self._countPeople()

    def generateTree(self):
        """Generate partners and children for everyone in the action queue."""
        while self.actionQueue:
            try:
                current = pop(self.actionQueue)

                has_partner = self.pd.getPartner(current.yearBorn)
                c_partner = None
                if has_partner:
                    c_partner = self.pd.createPartner(current)

                new_children = self.pd.createChildren(current, c_partner)
                self.actionQueue.extend(new_children)

            except YearEndError:
                continue

        print("finished generation!")

    def _countPeople(self):
        """Count unique people in tree via BFS from root1."""
        visited = set()
        queue = [self.root1]
        while queue:
            current = pop(queue)
            if id(current) in visited:
                queue.extend(current.children)
                continue
            visited.add(id(current))
            if (
                current.partner is not None
                and id(current.partner) not in visited
            ):
                visited.add(id(current.partner))
                queue.append(current.partner)
            queue.extend(current.children)
        return len(visited)

    def __str__(self):
        last_gen = 0
        rval = []
        search_queue = [(self.root1, 1)]
        while search_queue:
            current, gen = pop(search_queue)
            if gen > last_gen:
                last_gen = gen
                rval.append(
                    f"********** GENERATION {gen} **********\n"
                )
            rval.append(f"{current}\n")
            if current.partner is not None:
                rval.append(f"{current.partner}\n")
            for child in current.children:
                search_queue.append((child, gen + 1))
        return "".join(rval)

    def writeToFile(self):
        """Write tree string to output.txt."""
        with open("output.txt", "w") as file:
            file.write(str(self))


def pop(lst):
    """Remove and return first element of list; modifies in place."""
    if not lst:
        return
    rval = lst[0]
    del lst[0]
    return rval
