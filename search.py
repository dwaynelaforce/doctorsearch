from io import StringIO
from enum import Enum
from dataclasses import dataclass, field

import doctors

class QueryStatus(Enum):
    SUCCESS = 0
    ERROR = 1
    MULTIPLE_RESULTS = 2
    NOT_FOUND = 3

@dataclass
class Results:
    status: QueryStatus
    license: doctors.MedicalLicense | None = None
    notes: list[str] = field(default_factory=list)

    def __repr__(self) -> str:
        
        sio = StringIO()
        sio.write(f"<Results ({self.status})")
        if self.license:
            sio.write(": ")
            sio.write(str(self.license))
        if self.notes:
            sio.write(": ")
            sio.write(", ".join(self.notes[:3]))
            sio.write(f", ... ({len(self.notes) - 3 } more)")
        sio.write(">")
        return sio.getvalue()
    
    def __str__(self) -> str:
        return self.__repr__()