import unittest
from lab3 import IncomeManager, Rent, Salary

class TestIncomeManager(unittest.TestCase):

    def setUp(self):
        self.manager = IncomeManager()

    def test_add_and_delete_record(self):
        rent = Rent("Apartment", 5000, "Igor", "31.01.2025")
        self.manager.add(rent)
        self.assertEqual(len(self.manager.records), 1)
        self.assertEqual(self.manager.records[0].source, "Apartment")

        self.manager.delete(0)
        self.assertEqual(len(self.manager.records), 0)

    def test_valid_rent_line(self):
        line = "Rent Apartment 5000 Igor 01.01.2025"
        record = self.manager.parse_line(line)
        self.assertIsInstance(record, Rent)
        self.assertEqual(record.source, "Apartment")
        self.assertEqual(record.money, 5000)
        self.assertEqual(record.tenant, "Igor")

    def test_valid_salary_line(self):
        line = "Salary Office 10000 Rusal 12.02.2025"
        record = self.manager.parse_line(line)
        self.assertIsInstance(record, Salary)
        self.assertEqual(record.firm, "Rusal")

    def test_invalid_line(self):
        line = "Invalid data format"
        with self.assertRaises(ValueError):
            self.manager.parse_line(line)

    def test_empty_line(self):
        with self.assertRaises(ValueError):
            self.manager.parse_line("")

if __name__ == '__main__':
    unittest.main()
