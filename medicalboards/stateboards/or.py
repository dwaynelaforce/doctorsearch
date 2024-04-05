import requests

from medicalboards import StateMedicalBoardInterface
from medicalboards.states import State
from enums_and_dataclasses import (
    Doctor, 
    LicenseStatus, 
    Result,
    ResultStatus,
    MedicalLicense
)

# according to https://data.oregon.gov/stories/s/y49e-7s6y
# the OMB is planning on making a dataset public in the next 2 years
# right now only way to check any doc is manual search.

class MedicalBoardInterface(StateMedicalBoardInterface):
    state = State.OR

    def license_search(cls, doctor: Doctor) -> Result:
        res = Result()
        res.notes.append(
            "No developer API or dataset is available from Oregon Medical Board as of April 2024. "
            "According to the Oregon Open Data Progress Report, this is planned to be released "
            "in the next 2 years."
            "You can manually search for the doctor at https://omb.oregon.gov/search. "
        )
        return res