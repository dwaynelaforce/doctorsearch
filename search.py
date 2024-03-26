"""
This module intends to provide all the necessary classes for general search
functionality including standardization with dataclasses and enums.
"""

from pprint import pprint
from typing import List, Dict, Type
from importlib import import_module

from medicalboards import StateMedicalBoardInterface
from medicalboards.states import State, get_state
from enums_and_dataclasses import (
    Query, 
    QueryStatus,
    Result,
    Doctor
)

class InquiryManager:

    """
    Class for performing the main function of searching for a doctor across
    multiple state medical boards.
    """

    def __init__(self):
        self.queries: List[Query] = []
        self.results: List[Result] = []
        self.resultsmap: Dict[State, Result] = []

    @staticmethod
    def _get_state_interface(state: State) -> Type[StateMedicalBoardInterface]:
        """
        Given a state, imports and then returns the appropriate interface 
        class for the state's medical board.
        """ 
        module_name = f"medicalboards.stateboards.{state.name.casefold()}"
        module = import_module(module_name)
        return getattr(module, "MedicalBoardInterface")

    def exec_all_queries(self) -> None:
        """Executes all queries."""
        for query in self.queries:
            self.exec_query(query)

    def exec_query(self, query: Query) -> Result:
        
        interface = self._get_state_interface(query.state)
        result = interface.license_search(query.doctor)
        query.status = QueryStatus.COMPLETE
        result.query = query
        self.results.append(result)

    @staticmethod
    def _build_query(**params) -> Query:
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