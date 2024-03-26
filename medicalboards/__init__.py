from abc import ABC, abstractclassmethod

from medicalboards.states import State
from enums_and_dataclasses import Result, Doctor


class StateMedicalBoardInterface(ABC):
    state: State

    @abstractclassmethod
    def license_search(doctor: Doctor) -> Result: ...
