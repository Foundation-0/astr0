import unittest
from kmos_inventory import summarize


def fixture():
    header = '#Name: J/ApJ/842/121/table3\nrecno\tSeq\tz\tlogM*\tlogMb\tVcirc\tsigma0\n\t\t\t[Msun]\t[Msun]\tkm/s\tkm/s\n---\t---\t---\t---\t---\t---\t---\n'
    return (header + ''.join(f'{i}\t{i}\t1.0\t10\t10.5\t200\t30\n' for i in range(1,136))).encode()


class KmosTests(unittest.TestCase):
    def test_synthetic_inventory(self):
        self.assertEqual(summarize(fixture())['rows'], 135)
        self.assertFalse(summarize(fixture())['adequacy']['joint_inference'])

    def test_timestamp_does_not_change_numeric_hash(self):
        first = summarize(b"#request_date: first\n" + fixture())
        second = summarize(b"#request_date: second\n" + fixture())
        self.assertNotEqual(first["sha256"], second["sha256"])
        self.assertEqual(first["numeric_rows_sha256"], second["numeric_rows_sha256"])

    def test_interior_value_changes_numeric_hash(self):
        first = summarize(fixture())
        second = summarize(fixture().replace(b"50\t50\t1.0", b"50\t50\t1.1", 1))
        self.assertNotEqual(first["numeric_rows_sha256"], second["numeric_rows_sha256"])

    def test_missing_row(self):
        with self.assertRaises(ValueError):
            summarize(fixture().replace(b'135\t135\t1.0\t10\t10.5\t200\t30\n', b''))

    def test_invalid_value(self):
        with self.assertRaises(ValueError):
            summarize(fixture().replace(b'\t200\t', b'\tnan\t', 1))

    def test_wrong_units(self):
        with self.assertRaises(ValueError):
            summarize(fixture().replace(b'km/s', b'm/s'))

    def test_wrong_catalogue(self):
        with self.assertRaises(ValueError):
            summarize(fixture().replace(b'842/121', b'842/122'))


if __name__ == '__main__':
    unittest.main()
