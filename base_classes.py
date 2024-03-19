from enum import Enum
from io import StringIO
from dataclasses import dataclass, field

from enums import LicenseStatus, MedicalDegree, QueryStatus, State


@dataclass
class MedicalLicense:
    state: State
    status: LicenseStatus
    id: str
    discipline: bool

    def __repr__(self) -> str:
        buf = StringIO()
        buf.write(f"Medical License: {self.state}")
        buf.write(f", {self.status} | {self.id}")
        buf.write(f", disciplined: {self.discipline}")
        return buf.getvalue()
    
    def __str__(self) -> str:
        return self.__repr__()


@dataclass
class Doctor:
    lastname: str
    firstname: str
    middle: str | None = None
    degree: MedicalDegree | None = None
    licenses: list[MedicalLicense] = field(default_factory=list)

    def active_licenses(self) -> list[MedicalLicense]:
        return [l for l in self.licenses if l.status is LicenseStatus.ACTIVE]

    def __repr__(self) -> str:
        buf = StringIO()
        buf.write(f"Doctor: {self.lastname.title()}")
        if self.firstname:
            buf.write(f", {self.firstname.title()}")
            if self.middle:
                buf.write(f" {self.middle.title()}")
        if self.degree:
            buf.write(f", {self.degree}")
        if lics := self.active_licenses():
            buf.write(f" ({len(lics)}) active licenses.")
        return buf.getvalue()
    
    def __str__(self) -> str:
        return self.__repr__()


@dataclass
class Results:
    status: QueryStatus
    license: MedicalLicense | None = None
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
