from wa import license_search
from base_classes import Doctor

def main():
    lname = input("last name: ")
    fname = input("first name: ")
    mname = input("middle name or initial: ")

    results = license_search(Doctor(lname, fname, mname))
    print(results)

if __name__ == "__main__":
    main()