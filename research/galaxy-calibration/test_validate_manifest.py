import hashlib
from pathlib import Path
import tempfile
import unittest
from validate_manifest import ROLES, validate


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        (self.root / 'input.txt').write_bytes(b'synthetic fixture\n')
        payload = (self.root / 'input.txt').read_bytes()
        self.manifest = {'artifacts': [dict(role=role, path='input.txt', source_url='https://example.org/data', bytes=len(payload), sha256=hashlib.sha256(payload).hexdigest(), schema={'columns': ['fixture'], 'units': {'fixture': 'dimensionless'}}) for role in sorted(ROLES)]}

    def test_complete_byte_inventory(self):
        self.assertEqual(validate(self.manifest, self.root), [])

    def test_absent_data_blocks(self):
        self.assertTrue(validate({'artifacts': []}, self.root))

    def test_modified_bytes_block(self):
        (self.root / 'input.txt').write_bytes(b'changed')
        self.assertIn('SHA256 mismatch', validate(self.manifest, self.root))

    def test_escape_blocks(self):
        self.manifest['artifacts'][0]['path'] = '../outside.txt'
        self.assertTrue(validate(self.manifest, self.root))

    def test_duplicate_role_blocks(self):
        self.manifest['artifacts'][0]['role'] = self.manifest['artifacts'][1]['role']
        self.assertIn('unknown or repeated product role', validate(self.manifest, self.root))

    def test_missing_schema_blocks(self):
        self.manifest['artifacts'][0]['schema'] = {}
        self.assertIn('original columns and units must be declared', validate(self.manifest, self.root))

    def test_nonpublic_source_blocks(self):
        self.manifest['artifacts'][0]['source_url'] = 'file:///private/data'
        self.assertIn('a declared HTTP(S) source URL is required', validate(self.manifest, self.root))


if __name__ == '__main__':
    unittest.main()
