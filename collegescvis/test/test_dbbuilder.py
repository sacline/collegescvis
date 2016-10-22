"""Unit tests for the dbbuilder module.

Classes:
    TestInitializeDatabase(unittest.TestCase): Test database init.
    TestSanitize(unittest.TestCase): Test sanitize function.
"""
import unittest
from dbbuilder import Dbbuilder


class TestInitializeDatabase(unittest.TestCase):
    """Contains tests for dbbuilder initialization.

    Methods:
        test_invalid_db_path(self): Test invalid database path input.
        test_invalid_data_types_path(self): Test invalid data types path.
        test_empty_data_types_path(self): Test empty data types path.
    """

    def test_invalid_db_path(self):
        """Test invalid database path input."""
        invalid_db_path = 100
        valid_data_types_path = './data_types.txt'
        self.assertRaises(
            TypeError, lambda: Dbbuilder(
                invalid_db_path, valid_data_types_path))

    def test_invalid_data_types_path(self):
        """Test invalid data types path."""
        valid_db_path = 'db.sqlite'
        invalid_data_types_path = 100
        self.assertRaises(
            TypeError, lambda: Dbbuilder(
                valid_db_path, invalid_data_types_path))

    def test_empty_data_types_path(self):
        """Test invalid data types file location."""
        valid_db_path = 'db.sqlite'
        empty_data_types_path = ''
        self.assertRaises(
            FileNotFoundError, lambda: Dbbuilder(
                valid_db_path, empty_data_types_path))


class TestSanitize(unittest.TestCase):
    """Contains tests for dbbuilder's sanitize function.

    Methods:
        test_valid_input(self): Test various valid inputs.
        test_invalid_input(self): Test non-string input.
        test_bad_characters(self): Test inputs containing invalid characters.
    """

    def test_valid_input(self):
        """Test various valid inputs."""
        valid_input_string = 'Table Name'
        self.assertEqual(
            valid_input_string, Dbbuilder.sanitize(valid_input_string))
        valid_input_string = '123_'
        self.assertEqual(
            valid_input_string, Dbbuilder.sanitize(valid_input_string))
        valid_input_string = '!@Table(3)'
        self.assertEqual(
            valid_input_string, Dbbuilder.sanitize(valid_input_string))

    def test_invalid_input(self):
        """Test invalid (nonstring) inputs."""
        invalid_input = 3859
        self.assertRaises(
            TypeError, lambda: Dbbuilder.sanitize(invalid_input))
        invalid_input = ['string']
        self.assertRaises(
            TypeError, lambda: Dbbuilder.sanitize(invalid_input))
        invalid_input = ('string1', 'string2')
        self.assertRaises(
            TypeError, lambda: Dbbuilder.sanitize(invalid_input))

    def test_bad_characters(self):
        """Test inputs containing invalid characters."""
        invalid_input_string = '"SELECT"'
        self.assertRaises(
            ValueError, lambda: Dbbuilder.sanitize(invalid_input_string))
        invalid_input_string = 'DELETE;'
        self.assertRaises(
            ValueError, lambda: Dbbuilder.sanitize(invalid_input_string))
        invalid_input_string = 'jf3\kfn3'
        self.assertRaises(
            ValueError, lambda: Dbbuilder.sanitize(invalid_input_string))


def main():
    """Launch unittest main method."""
    unittest.main()

if __name__ == '__main__':
    main()
