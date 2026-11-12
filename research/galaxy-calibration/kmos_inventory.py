"""Validate a separately downloaded CDS KMOS table and report input adequacy."""
import argparse
import hashlib
import json
import math
from pathlib import Path

URL = 'https://vizier.cfa.harvard.edu/viz-bin/asu-tsv?-source=J/ApJ/842/121/table3&-out.all&-out.max=unlimited'
COLUMNS = ['recno', 'Seq', 'z', 'logM*', 'logMb', 'Vcirc', 'sigma0']


def summarize(payload):
    lines = payload.decode('utf-8').splitlines()
    if '#Name: J/ApJ/842/121/table3' not in lines:
        raise ValueError('wrong catalogue')
    table = [line for line in lines if line.strip() and not line.startswith('#')]
    if table[0].split('\t') != COLUMNS:
        raise ValueError('unexpected columns')
    if [cell.strip() for cell in table[1].split('\t')] != ['', '', '', '[Msun]', '[Msun]', 'km/s', 'km/s']:
        raise ValueError('unexpected units')
    rows = []
    for line in table[3:]:
        cells = line.split('\t')
        if len(cells) != len(COLUMNS):
            raise ValueError('bad row width')
        row = dict(zip(COLUMNS, map(float, cells)))
        if not all(math.isfinite(x) for x in row.values()):
            raise ValueError('nonfinite value')
        if row['z'] <= 0 or row['Vcirc'] <= 0 or row['sigma0'] < 0 or row['logMb'] < row['logM*']:
            raise ValueError('invalid physical input')
        rows.append(row)
    if len(rows) != 135 or {r['Seq'] for r in rows} != set(range(1, 136)):
        raise ValueError('unexpected sample membership')
    return {'catalogue': 'J/ApJ/842/121/table3', 'rows': len(rows), 'bytes': len(payload), 'sha256': hashlib.sha256(payload).hexdigest(), 'numeric_rows_sha256': hashlib.sha256(json.dumps(rows, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')).hexdigest(), 'numeric_rows_serialization': 'UTF-8 JSON list in received row order; parsed floats; sorted object keys; compact separators; no NaN', 'ranges': {c: [min(r[c] for r in rows), max(r[c] for r in rows)] for c in COLUMNS[2:]}, 'adequacy': {'tully_fisher_diagnostic': True, 'radial_acceleration_relation': False, 'joint_inference': False}, 'missing': ['measurement uncertainty columns', 'radius profiles', 'joint posterior or covariance'], 'no_new_fit': True}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('table', type=Path)
    args = parser.parse_args()
    print(json.dumps(summarize(args.table.read_bytes()), indent=2))
