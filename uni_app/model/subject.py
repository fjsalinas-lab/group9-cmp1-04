from dataclasses import dataclass, field
import random

GRADES = {85: "HD", 75: "D", 65: "C", 50: "P", 0: "F"}

@dataclass
class Subject:

    id: str = field(init=False)
    mark: int = field(init=False)
    grade: str = field(init=False)

    def __post_init__(self):
       
        self.id = f"{random.randint(1, 999):03}"
        self.mark = random.randint(25, 100)
        for cutoff, g in GRADES.items():
            if self.mark >= cutoff:
                self.grade = g
                break
