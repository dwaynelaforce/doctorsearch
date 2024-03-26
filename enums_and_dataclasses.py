from enum import Enum
from dataclasses import dataclass, field

from medicalboards.states import State

class LicenseStatus(Enum):
    ACTIVE = 0
    EXPIRED = 1
    SUSPENDED = 2
    SURRENDERED_OR_REVOKED = 3
    OTHER = 4

class MedicalDegree(Enum):
    MD = "M.D. - Medical Doctor"
    DO = "D.O. - Osteopathic Doctor"
    DPM = "D.P.M. - Podiatrist" 

class QueryStatus(Enum):
    IN_PROGRESS = 0
    COMPLETE = 1

class ResultStatus(Enum):
    FOUND = 0
    ERROR = 1
    MULTIPLE_RESULTS = 2
    NOT_FOUND = 3
    PARTIAL_MATCH = 4
    INCOMPLETE = 5

class DatabaseType(Enum):
    SQLITE = "SQLite"
    CSV = "CSV"

@dataclass
class MedicalLicense:
    state: State
    status: LicenseStatus
    id: str
    discipline: bool

@dataclass
class Doctor:
    lastname: str
    firstname: str
    middle: str | None = None
    degree: MedicalDegree | None = None
    specialty: str | None = None
    licenses: list[MedicalLicense] = field(default_factory=list)

@dataclass
class Query: 
    doctor: Doctor
    state: State | None = None
    status: QueryStatus = QueryStatus.IN_PROGRESS

@dataclass
class Result:
    query: Query | None = None
    license: MedicalLicense | None = None
    notes: list[str] = field(default_factory=list)
    status: ResultStatus = ResultStatus.INCOMPLETE

