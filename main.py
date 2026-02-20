import sys

from person import Person
from personTree import PersonTree, pop


class PersonTreeCLI:
    """
    PersonTreeCLI generates a person tree and provides a command-line menu
    to interact with it.
    """

    def __init__(self):
        self.tree = PersonTree()
        self.menu()

    def menu(self):
        """Display menu and handle user selection."""
        options = (
            "To select an option, enter its number:\n"
            "        1. View total people in tree\n"
            "        2. View total number of people by decade\n"
            "        3. View duplicate names\n"
            "        4. Write tree to file\n"
            "        5. Exit\n"
            "Please enter the number of your selection: "
        )
        user_input = input(options).strip()
        while user_input == "" or (
            user_input < "1" and user_input > "5"
        ):
            print("ERROR: INVALID INPUT")
            user_input = input(options).strip()
        else:
            match user_input:
                case "1":
                    self.totalPeople()
                case "2":
                    self.totalByDecade()
                case "3":
                    self.duplicateNames()
                case "4":
                    self.writeToFile()
                case "5":
                    sys.exit(0)

    def totalPeople(self):
        """Print total number of people in tree."""
        print(f"Total people in tree: {self.tree.numPeople}")
        self.menu()

    def totalByDecade(self):
        """Print number of people by birth decade."""
        by_decade = {
            decade: []
            for decade in range(
                Person.YEARSTART, Person.YEAREND + 1, 10
            )
        }
        visited = set()
        search_queue = [self.tree.root1]
        while search_queue:
            current = pop(search_queue)
            if id(current) in visited:
                continue
            visited.add(id(current))
            current_decade = (current.yearBorn // 10) * 10
            if current_decade in by_decade:
                by_decade[current_decade].append(current)

            if current.partner is not None:
                partner = current.partner
                if id(partner) not in visited:
                    visited.add(id(partner))
                    partner_decade = round(partner.yearBorn, -1)
                    if partner_decade in by_decade:
                        by_decade[partner_decade].append(partner)
                search_queue.append(partner)

            search_queue.extend(current.children)

        for decade in sorted(by_decade.keys()):
            print(f"{decade}s: {len(by_decade[decade])}")

        self.menu()

    def duplicateNames(self):
        """Print duplicate full names in the tree."""
        search_queue = [self.tree.root1]
        seen = {}
        while search_queue:
            current = pop(search_queue)
            full_name = current.fName + " " + current.lName
            if full_name not in seen:
                seen[full_name] = {current}
            else:
                seen[full_name].add(current)

            if current.partner is not None:
                p_full_name = (
                    current.partner.fName + " " + current.partner.lName
                )
                if p_full_name not in seen:
                    seen[p_full_name] = {current.partner}
                else:
                    seen[p_full_name].add(current.partner)

            search_queue.extend(current.children)

        dupe_names = []
        total_dupes = 0
        for name, p_set in seen.items():
            if len(p_set) > 1:
                dupe_names.append(name)
                total_dupes += 1

        if total_dupes == 0:
            print("there are no duplicate names.")
        else:
            print(f"There are {total_dupes} duplicates in this tree:")
            for dn in dupe_names:
                print(f"* {dn}")

        self.menu()

    def writeToFile(self):
        """Write tree to output.txt."""
        self.tree.writeToFile()
        self.menu()


def main():
    PersonTreeCLI()


if __name__ == "__main__":
    main()
