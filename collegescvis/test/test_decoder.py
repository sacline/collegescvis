"""Unit tests for the decoder module.

Classes:
    TestDataPaths(unittest.TestCase): Tests for raw data path processing.
    TestReadValues(unittest.TestCase): Tests for read_values function.
    TestFindType(unittest.TestCase): Tests for find_type function.
"""
import unittest
import decoder


class TestDataPaths(unittest.TestCase):
    """Contains tests for raw data path processing.

    Methods:
        test_empty_path(self): Test an empty data path input.
        test_nonstring_path(self): Test a non-string data path input.
    """

    def test_empty_path(self):
        """Test an empty data path input.

        The glob function used in decoder will return an empty list when an
        empty string is passed to it. This test simulates any case in which
        the glob function returns an empty list (including passing a path
        containing no files).
        """
        empty_path = ''
        self.assertRaises(
            FileNotFoundError, lambda: decoder._validate_data_path(empty_path))

    def test_nonstring_path(self):
        """Test non-string data file paths.

        Non-string paths should raise a TypeError in the decoder validation
        function.
        """
        nonstring_int_path = 5
        self.assertRaises(
            TypeError, lambda: decoder._validate_data_path(nonstring_int_path))

        nonstring_list_path = ['path']
        self.assertRaises(
            TypeError, lambda: decoder._validate_data_path(nonstring_list_path))


class TestReadValues(unittest.TestCase):
    """Contains tests for the decoder module's read_values function.

    Methods:
        test_valid_entry(self): Test valid input to read_values.
        test_invalid_entry(self): Test invalid input to read_values.
    """

    def test_valid_entry(self):
        """Test valid entries (arguments) to read_values."""
        valid_entry = ['Category', '5', '8']
        valid_counts = [2, 0, 0]
        self.assertEqual(decoder._read_values(valid_entry), valid_counts)

        valid_entry = ['Category', '5.323', 'PrivacySuppressed', 'NULL']
        valid_counts = [1, 1, 1]
        self.assertEqual(decoder._read_values(valid_entry), valid_counts)

    def test_invalid_entry(self):
        """Test invalid entries (arguments) to read_values."""
        invalid_int_entry = [3, 5]
        self.assertRaises(
            TypeError, lambda: decoder._read_values(invalid_int_entry))

        invalid_tuple_entry = (3, 5)
        self.assertRaises(
            TypeError, lambda: decoder._read_values(invalid_tuple_entry))

        invalid_empty_entry = []
        self.assertRaises(
            ValueError, lambda: decoder._read_values(invalid_empty_entry))

        invalid_str_entry = 'String'
        self.assertRaises(
            TypeError, lambda: decoder._read_values(invalid_str_entry))


class TestFindType(unittest.TestCase):
    """Contains tests for decoder find_type function.

    Methods:
        test_integer_entry(self): Test an entry containing integer data.
        test_real_entry(self): Test an entry containing real number data.
        test_text_entry(self): Test an entry containing text data.
    """

    def test_integer_entry(self):
        """Test an entry containing integer data."""
        valid_integer_entry = ['Category', '5', '2', '6', '873', 'NULL']
        self.assertEqual('INTEGER', decoder._find_type(valid_integer_entry))

    def test_real_entry(self):
        """Test an entry containing real number data."""
        valid_real_entry = ['Category', '8.32', '7.2345', 'NULL', '5']
        self.assertEqual('REAL', decoder._find_type(valid_real_entry))

    def test_text_entry(self):
        """Test an example entry containing text data."""
        valid_text_entry = ['Category', '8.32', 'text', '5', 'NULL']
        self.assertEqual('TEXT', decoder._find_type(valid_text_entry))


def main():
    """Launch the unittest main function."""
    unittest.main()

if __name__ == '__main__':
    main()
