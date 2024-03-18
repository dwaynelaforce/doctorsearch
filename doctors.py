from io import StringIO
from enum import Enum
from dataclasses import dataclass, field

class State(Enum):
    # https://en.wikipedia.org/wiki/#v 
    # List_of_states_and_territories_of_the_United_States#States.
    AK = "Alaska"
    AL = "Alabama"
    AR = "Arkansas"
    AZ = "Arizona"
    CA = "California"
    CO = "Colorado"
    CT = "Connecticut"
    DE = "Delaware"
    FL = "Florida"
    GA = "Georgia"
    HI = "Hawaii"
    IA = "Iowa"
    ID = "Idaho"
    IL = "Illinois"
    IN = "Indiana"
    KS = "Kansas"
    KY = "Kentucky"
    LA = "Louisiana"
    MA = "Massachusetts"
    MD = "Maryland"
    ME = "Maine"
    MI = "Michigan"
    MN = "Minnesota"
    MO = "Missouri"
    MS = "Mississippi"
    MT = "Montana"
    NC = "North Carolina"
    ND = "North Dakota"
    NE = "Nebraska"
    NH = "New Hampshire"
    NJ = "New Jersey"
    NM = "New Mexico"
    NV = "Nevada"
    NY = "New York"
    OH = "Ohio"
    OK = "Oklahoma"
    OR = "Oregon"
    PA = "Pennsylvania"
    RI = "Rhode Island"
    SC = "South Carolina"
    SD = "South Dakota"
    TN = "Tennessee"
    TX = "Texas"
    UT = "Utah"
    VA = "Virginia"
    VT = "Vermont"
    WA = "Washington"
    WI = "Wisconsin"
    WV = "West Virginia"
    WY = "Wyoming"
    # https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States#Federal_district.
    DC = "District of Columbia",
    # https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States#Inhabited_territories.
    AS = "American Samoa",
    GU = "Guam GU",
    MP = "Northern Mariana Islands",
    PR = "Puerto Rico PR",
    VI = "U.S. Virgin Islands",

class LicenseStatus(Enum):
    ACTIVE = 0
    EXPIRED = 1
    SUSPENDED = 2
    SURRENDERED_OR_REVOKED = 3

class MedicalDegree(Enum):
    MD = "M.D. - Medical Doctor"
    DO = "D.O. - Osteopathic Doctor"

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
