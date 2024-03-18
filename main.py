
from doctors import Doctor, MedicalDegree
from wa import license_search

def main():
    lname = input("last name: ")
    fname = input("first name: ")
    mname = input("middle name or initial: ")

    doctor = Doctor(lname, fname, mname)
    
    # loop over each state
    results = license_search(doctor)

    print(results)

if __name__ == "__main__":
    main()