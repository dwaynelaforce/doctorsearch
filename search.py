from typing import List, Dict
from enum import Enum
from io import StringIO
from importlib import import_module
from dataclasses import dataclass, field
from pprint import pprint

from doctors import Doctor, MedicalLicense
from medicalboards import BoardsDirectory
from medicalboards.states import State, get_state


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

class InquiryManager:

    def __init__(self):
        self.queries: List[Query] = []
        self.results: List[Result] = []
        self.resultsmap: Dict[State, Result] = []

    def exec_all_queries(self):
        for query in self.queries:
            self.exec_single_state_query(query)

    def exec_single_state_query(self, query: Query) -> Result:
        state_abbr: str = query.state.name
        modname = f"medicalboards.stateboards.{state_abbr.casefold()}"
        module = import_module(modname)
        result: Result = module.license_search(query.doctor)
        query.status = QueryStatus.COMPLETE
        result.query = query
        self.results.append(result)

    def _build_query(self, **params) -> Query:
        state = get_state(params.pop("state"))
        lastname = params.pop("lastname")
        firstname = params.pop("firstname")
        doctor = Doctor(lastname, firstname)
        if middle := params.pop('middle', None):
            doctor.middle = middle
        return Query(doctor, state)

    def add_query(self, query: Query=None, **params) -> None:
        if not query:
            query = self._build_query(**params)
        self.queries.append(query)

    def display_results(self) -> None:
        for result in self.results:
            pprint(result)