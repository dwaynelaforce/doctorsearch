from io import StringIO
from enum import Enum
from dataclasses import dataclass, field

from medicalboards import State


class LicenseStatus(Enum):
    ACTIVE = 0
    EXPIRED = 1
    SUSPENDED = 2
    SURRENDERED_OR_REVOKED = 3

@dataclass
class MedicalLicense:
    state: State
    status: LicenseStatus
    id: str
    discipline: bool

class MedicalDegree(Enum):
    MD = "M.D. - Medical Doctor"
    DO = "D.O. - Osteopathic Doctor"

@dataclass
class Doctor:
    lastname: str
    firstname: str
    middle: str | None = None
    degree: MedicalDegree | None = None
    specialty: str | None = None
    licenses: list[MedicalLicense] = field(default_factory=list)

    def active_licenses(self) -> list[MedicalLicense]:
        return [l for l in self.licenses if l.status is LicenseStatus.ACTIVE]
