class Journal:
    def __init__(self):
        self.entries = []
        self.count = 0

    def add_entry(self, text):
        self.entries.append(f"{self.count}: {text}")
        self.count += 1

    def remove_entry(self, pos):
        del self.entries[pos]

    def __str__(self):
        return "\n".join(self.entries)

    # break SRP
    def save(self, filename):
        file = open(filename, "w")
        file.write(str(self))
        file.close()

    def load(self, filename):
        pass

    def load_from_web(self, uri):
        pass


class PersistenceManager:
    def __init__(self, input):
        self.input = input

    # This can be achieved by single function, no need for class.
    def save_to_file(self, filename):
        file = open(filename, "w")
        file.write(str(self.input))
        file.close()


j = Journal()
j.add_entry("I cried today.")
j.add_entry("I ate a bug.")
print(f"Journal entries:\n{j}\n")

p = PersistenceManager(input=j)
file = r'c:\temp\journal.txt'
p.save_to_file(file)

# verify!
with open(file) as fh:
    print(fh.read())
