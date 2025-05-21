import re
import random
from dataclasses import dataclass, field
from typing import List
from .subject import Subject


# Starting with lowercase letters, followed by optional dot and lowercase letters. Ends with @university.com
EMAIL_RE = re.compile(r"^[a-z]+(?:\.[a-z]+)*@university\.com$", re.I)
# Starting with uppercase letter, followed by at least 4 letters, then 3+ digits
PASS_RE = re.compile(r"^[A-Z][A-Za-z]{4,}\d{3,}$")

@dataclass
class Student:

    name: str
    email: str
    password: str
    id: str = field(init=False)
    subjects: List[Subject] = field(default_factory=list)

    def __post_init__(self):

        self.id = f"{random.randint(1, 999_999):06}"
        self._validate_credentials()

    def _validate_credentials(self):
        """
        Validates the student's email and password using regex patterns.
        Raises ValueError if validation fails.
        """
        if not EMAIL_RE.fullmatch(self.email):
            raise ValueError("Invalid email format")
        if not PASS_RE.fullmatch(self.password):
            raise ValueError("Invalid password format")

    def enrol(self, subject: Subject):

        if len(self.subjects) == 4:
            raise ValueError("Max 4 subjects")
        if any(s.id == subject.id for s in self.subjects):
            raise ValueError("Already enrolled in that subject")
        self.subjects.append(subject)

    def drop(self, subject_id: str):

        self.subjects = [s for s in self.subjects if s.id != subject_id]

    def change_password(self, new_pwd: str):
   
        if not PASS_RE.fullmatch(new_pwd):
            raise ValueError("Password format invalid")
        self.password = new_pwd

    def average(self) -> float:

        return round(sum(s.mark for s in self.subjects) / len(self.subjects), 2) if self.subjects else 0
    
    def average_label(self) -> str:
        mark = round(sum(s.mark for s in self.subjects) / len(self.subjects), 2) if self.subjects else 0
        if   mark >= 85: return 'HD'
        elif mark >= 75: return 'D'
        elif mark >= 65: return 'C'
        elif mark >= 50: return 'P'
        else:            return 'F'


    def has_passed(self) -> bool:

        return self.average() >= 50
