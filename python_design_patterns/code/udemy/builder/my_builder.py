from unittest import TestCase


class ClassStructure:
    indentation = 4 * ' '

    def __init__(self, name: str):
        self.name = name
        self.fields: list[FieldStructure] = []

    def __str__(self):
        lines = [f'class {self.name}:']
        if not self.fields:
            lines.append(f'{self.indentation}pass')
        else:
            lines.append(f'{self.indentation}def __init__(self):')
            for field in self.fields:
                lines.append(f'{self.indentation}{self.indentation}{field}')
        return '\n'.join(lines)


class FieldStructure:
    def __init__(self, type: str, name: str):
        self.type = type
        self.name = name

    def __str__(self):
        return f'self.{self.type} = {self.name}'


# type and name are name and value.
# Just there since given code example is setup this way.
# Also root_name is hideous.
class CodeBuilder:
    def __init__(self, root_name: str):
        self._root_class = ClassStructure(root_name)

    def add_field(self, type: str, name: str):
        self._root_class.fields.append(FieldStructure(type, name))
        return self

    def __str__(self):
        return self._root_class.__str__()


class TestBuilder(TestCase):
    def setUp(self) -> None:
        self.indentation = 4
        self.space = ' '

    def test_empty(self):
        code_builder = CodeBuilder('Foo')
        self.assertEqual(
            str(code_builder),
            f'class Foo:\n{self.indentation * self.space}pass'
        )

    def test_person(self):
        code_builder = CodeBuilder('Person')\
            .add_field(type='name', name='""')\
            .add_field(type='age', name='0')

        self.assertEqual(
            str(code_builder),
            """class Person:
    def __init__(self):
        self.name = \"\"
        self.age = 0"""
        )
