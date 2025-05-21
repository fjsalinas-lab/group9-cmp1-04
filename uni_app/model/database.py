import pickle
from pathlib import Path
from .student import Student

class Database:
 
    _FILE = Path("students.data")

    def __init__(self):
        self._FILE.touch(exist_ok=True)

    def load(self) -> list[Student]:

        with self._FILE.open("rb") as fh:
            try:
                return pickle.load(fh)
            except EOFError:
                return []

    def save(self, students: list[Student]):
        with self._FILE.open("wb") as fh:
            pickle.dump(students, fh)

    def add(self, student: Student):
        data = self.load()
        data.append(student)
        self.save(data)

    def update(self, student: Student):

        data = self.load()
        for i, s in enumerate(data):
            if s.id == student.id:
                data[i] = student
                break
        self.save(data)

    def remove_by_id(self, student_id: str):

        data = [s for s in self.load() if s.id != student_id]
        self.save(data)

    def clear(self):
        
        self.save([])
