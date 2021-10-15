class Person:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class PersonFactory:

    persons = []

    def create_person(self, name):
        if not self.persons:
            person = Person(id=0, name=name)
            self.persons.append(person)
            return person

        person = Person(id=self.persons.index(self.persons[-1]) + 1, name=name)
        self.persons.append(person)
        return person


if __name__ == '__main__':
    factory = PersonFactory()
    person1 = factory.create_person('John')
    person2 = factory.create_person('Ana')

    print(person1.id)
    print(person2.id)
    print(factory.persons)