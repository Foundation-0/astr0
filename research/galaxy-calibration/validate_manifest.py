"""Check local input bytes. This does not validate science or original schemas."""
import argparse
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urlparse

ROLES = {'photometry', 'halo_fit', 'selection', 'joint_uncertainty'}


def validate(manifest, root):
    errors = []
    roles = set()
    for item in manifest.get('artifacts', []):
        role = item.get('role')
        if role not in ROLES or role in roles:
            errors.append('unknown or repeated product role')
        roles.add(role)
        source = urlparse(item.get('source_url', ''))
        if source.scheme not in ('http', 'https') or not source.netloc:
            errors.append('a declared HTTP(S) source URL is required')
        relative = Path(item.get('path', ''))
        target = (root / relative).resolve()
        if relative.is_absolute() or not target.is_relative_to(root.resolve()) or not target.is_file():
            errors.append('input must be an existing file under the data directory')
            continue
        payload = target.read_bytes()
        digest = item.get('sha256', '')
        if not isinstance(digest, str) or not re.fullmatch('[a-f0-9]{64}', digest) or hashlib.sha256(payload).hexdigest() != digest:
            errors.append('SHA256 mismatch')
        if type(item.get('bytes')) is not int or len(payload) != item['bytes']:
            errors.append('byte count mismatch')
        if not isinstance(item.get('schema'), dict) or not item['schema'].get('columns') or not item['schema'].get('units'):
            errors.append('original columns and units must be declared')
    missing = ROLES - roles
    if missing:
        errors.append('missing product roles: ' + ', '.join(sorted(missing)))
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('--data-dir', type=Path, required=True)
    args = parser.parse_args()
    errors = validate(json.loads(args.manifest.read_text()), args.data_dir)
    print(json.dumps({'byte_inventory_complete': not errors, 'science_ready': False, 'errors': errors}, indent=2))
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
