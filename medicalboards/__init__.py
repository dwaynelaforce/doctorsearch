import csv
from typing import Dict, List, NoReturn
from dataclasses import dataclass

from app_settings import ASSETS
from exceptions import NotFoundError
from medicalboards.states import State


@dataclass
class StateMedicalBoard:
    state = State # example: State.KS
    name = str # example: 'Kansas State Board of the Healing Arts'
    website = str # example: 'https://kansas.gov/boards/healingarts'
    api_uri = str # example: 'https://kansas.gov/api-portals/professional-licenses.json'


class BoardsDirectory:

    CSV_DIRECTORY_FILE = ASSETS / "boards-directory.csv"
    _boardlist: List[StateMedicalBoard] = []
    _boardmap: Dict[State, StateMedicalBoard] = {}

    def __init__(self, *_, **__) -> NoReturn:
        raise ValueError("This is a static class. Do not init.")

    @staticmethod
    def _populate_from_csv() -> None:
        with open(BoardsDirectory.CSV_DIRECTORY_FILE) as file:
            _csvdata: List[Dict[str, str]] = [e for e in csv.DictReader(file)]

        for entry in _csvdata:
            state_abbr: str = entry.pop('state').upper()
            state: State = getattr(State, state_abbr)
            smb = StateMedicalBoard(state, **entry)
            BoardsDirectory._boardlist.append(smb)
            BoardsDirectory._boardmap[state] = smb

    @staticmethod
    @property
    def boardlist() -> List[StateMedicalBoard]:
        if not BoardsDirectory._boardlist:
            BoardsDirectory._populate_from_csv()
        return BoardsDirectory._boardlist

    @staticmethod
    @property
    def boardmap() -> Dict[State, StateMedicalBoard]:
        if not BoardsDirectory._boardlist:
            BoardsDirectory._populate_from_csv()
        return BoardsDirectory._boardlist


def find_board(state_abbr: str) -> StateMedicalBoard:
    state: State = getattr(State, state_abbr)
    if state in BoardsDirectory.boardmap:
        return BoardsDirectory.boardmap[State]
    else:
        raise NotFoundError(f"couldn't find '{state_abbr}'")
