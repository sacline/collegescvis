"""Unit tests for the decoder module."""
import unittest
import decoder

class TestDataPaths(unittest.TestCase):
    """Contains tests related to the raw data path processing."""

    def test_empty_path(self):
        """Tests an empty data path.

        The glob function used in decoder will return an empty list when an
        empty string is passed to it. This test simulates any case in which
        the glob function returns an empty list (including passing a path
        containing no files).
        """
        empty_path = ''
        self.assertRaises(
            FileNotFoundError, lambda: decoder.validate_data_path(empty_path))

    def test_nonstring_path(self):
        """Tests non-string data file paths.

        Non-string paths should raise a TypeError in the decoder validation
        function.
        """
        nonstring_int_path = 5
        self.assertRaises(
            TypeError, lambda: decoder.validate_data_path(nonstring_int_path))

        nonstring_list_path = ['path']
        self.assertRaises(
            TypeError, lambda: decoder.validate_data_path(nonstring_list_path))

class TestReadValues(unittest.TestCase):
    """Contains tests for the decoder module's read_values function."""

    def test_valid_entry(self):
        """Tests valid entries (arguments) to read_values."""
        valid_entry = ['Category', '5', '8']
        valid_counts = [2, 0, 0]
        self.assertEqual(decoder.read_values(valid_entry), valid_counts)

        valid_entry = ['Category', '5.323', 'PrivacySuppressed', 'NULL']
        valid_counts = [1, 1, 1]
        self.assertEqual(decoder.read_values(valid_entry), valid_counts)

    def test_invalid_entry(self):
        """Tests invalid entries (arguments) to read_values."""
        invalid_int_entry = [3, 5]
        self.assertRaises(
            TypeError, lambda: decoder.read_values(invalid_int_entry))

        invalid_tuple_entry = (3, 5)
        self.assertRaises(
            TypeError, lambda: decoder.read_values(invalid_tuple_entry))

        invalid_empty_entry = []
        self.assertRaises(
            ValueError, lambda: decoder.read_values(invalid_empty_entry))

        invalid_str_entry = 'String'
        self.assertRaises(
            TypeError, lambda: decoder.read_values(invalid_str_entry))

class TestFindType(unittest.TestCase):
    """Contains tests for decoder find_type method."""

    def test_integer_entry(self):
        """Tests an example entry containing integer data."""
        valid_integer_entry = ['Category', '5', '2', '6', '873', 'NULL']
        self.assertEqual('INTEGER', decoder.find_type(valid_integer_entry))

    def test_real_entry(self):
        """Tests an example entry containing real number data."""
        valid_real_entry = ['Category', '8.32', '7.2345', 'NULL', '5']
        self.assertEqual('REAL', decoder.find_type(valid_real_entry))

    def test_text_entry(self):
        """Tests an example entry containing text data."""
        valid_text_entry = ['Category', '8.32', 'text', '5', 'NULL']
        self.assertEqual('TEXT', decoder.find_type(valid_text_entry))

def main():
    """Launches the unittest main function."""
    unittest.main()

if __name__ == '__main__':
    main()
