from search import InquiryManager

def main():
    lname = input("last name: ")
    fname = input("first name: ")
    mname = input("middle name or initial: ")

    manager = InquiryManager()
    query = {
        'lastname': lname,
        'firstname': fname,
        'state': "WA"
    }
    manager.add_query(**query)
    manager.exec_all_queries()
    manager.display_results()

if __name__ == "__main__":
    main()