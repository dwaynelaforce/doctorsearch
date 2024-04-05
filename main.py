from medicalboards.states import State
from search import InquiryManager

SUPPORTED_STATES = [
    State.AK, # only partial support, API does not return license action data (manual search only)
    State.WA,
    State.OR, # no public dataset available, planned for release in 2 years
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