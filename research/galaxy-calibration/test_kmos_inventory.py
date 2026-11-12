import unittest
from kmos_inventory import summarize


def fixture():
    header = '#Name: J/ApJ/842/121/table3\nrecno\tSeq\tz\tlogM*\tlogMb\tVcirc\tsigma0\n\t\t\t[Msun]\t[Msun]\tkm/s\tkm/s\n---\t---\t---\t---\t---\t---\t---\n'
    return (header + ''.join(f'{i}\t{i}\t1.0\t10\t10.5\t200\t30\n' for i in range(1,136))).encode()


class KmosTests(unittest.TestCase):
    def test_synthetic_inventory(self):
        self.assertEqual(summarize(fixture())['rows'], 135)
        self.assertFalse(summarize(fixture())['adequacy']['joint_inference'])

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
