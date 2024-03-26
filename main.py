from medicalboards.states import State
from search import InquiryManager

SUPPORTED_STATES = [
    State.AK,
    State.WA
]

def main():
    lname = input("last name: ")
    fname = input("first name: ")
    # mname = input("middle name or initial: ")

    manager = InquiryManager()
    queries = [{
        'lastname': lname,
        'firstname': fname,
        'state': state.name
    } for state in SUPPORTED_STATES]
    for query in queries:
        manager.add_query(**query)
    manager.exec_all_queries()
    manager.display_results()

if __name__ == "__main__":
    main()