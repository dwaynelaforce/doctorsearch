import unittest

import search
from doctors import Doctor, MedicalDegree
from wa import license_search


class TestDoctorSearch(unittest.TestCase):

    def test_wa(self):
        searchdoctor = Doctor("Lai", "Kin", degree=MedicalDegree.MD)
        results = license_search(searchdoctor)
        self.assertEqual(results.status, search.QueryStatus.SUCCESS)

if __name__ == "__main__":
    unittest.main()