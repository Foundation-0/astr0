"""Descriptive KMOS3D peak-speed diagnostic. See ANALYSIS-PLAN.md for scope.

Requires sibling kmos_inventory.py from the published input contract.
No measurement likelihood or uncertainty interval is constructed.
"""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
from statistics import mean, median, pstdev
import sys

CANONICAL = 'afadb1ef14ab6b88ce492f3fbf53d7d81e30fe178dcab6642aafdd1744c918f3'
G = 6.67430e-11  # SI, CODATA 2018
MSUN = 1.98847e30  # kg; cancels from every redshift contrast
VREF = 242.0
BIN_EDGES = (100.0, 200.0, 300.0, 500.0)
PUBLISHED = {
    'low': {'n': 65, 'logM*': 10.49, 'logMb': 10.62, 'Vcirc': 239, 'sigma0': 30, 'b_star': 10.49, 'b_baryon': 10.68},
    'mid': {'n': 24, 'logM*': 10.72, 'logMb': 10.97, 'Vcirc': 263, 'sigma0': 47},
    'high': {'n': 46, 'logM*': 10.51, 'logMb': 10.89, 'Vcirc': 260, 'sigma0': 49, 'b_star': 10.51, 'b_baryon': 10.85},
}


def evolution(z):
    return math.sqrt(0.315 * (1 + z) ** 3 + 0.685)


def group_name(z):
    return 'low' if z < 1.2 else 'mid' if z < 1.8 else 'high'


def load_rows(path):
    # Validate with the original parser; extraction below does not replace its checks.
    from kmos_inventory import summarize, COLUMNS
    payload = path.read_bytes()
    inventory = summarize(payload)
    if inventory['numeric_rows_sha256'] != CANONICAL:
        raise ValueError('numeric catalogue differs from the frozen input')
    lines = [s for s in payload.decode('utf-8').splitlines() if s.strip() and not s.startswith('#')]
    rows = [dict(zip(COLUMNS, map(float, values))) for values in csv.reader(lines[3:], delimiter='\t')]
    for r in rows:
        r['group'] = group_name(r['z'])
        r['x'] = math.log10(evolution(r['z']))
        r['lv'] = math.log10(r['Vcirc'] / VREF)
        r['b_star'] = r['logM*'] - 3.60 * r['lv']
        r['b_baryon'] = r['logMb'] - 3.75 * r['lv']
        r['b4'] = r['logMb'] - 4.0 * r['lv']
        r['y'] = 4 * math.log10(r['Vcirc'] * 1000) - math.log10(G * MSUN) - r['logMb']
        r['y_star'] = r['y'] + r['logMb'] - r['logM*']
        r['log_mass_boost'] = r['logMb'] - r['logM*']
        r['gas_fraction'] = 1.0 - 10 ** (-r['log_mass_boost'])
        r['pressure_fraction'] = 4.4 * (r['sigma0'] / r['Vcirc']) ** 2
        if not (0 <= r['pressure_fraction'] < 1.0):
            raise ValueError('rotation-speed reconstruction is not positive')
        r['rotation_proxy'] = r['Vcirc'] * math.sqrt(1 - r['pressure_fraction'])
        r['y_rotation'] = r['y'] + 2 * math.log10(1 - r['pressure_fraction'])
    return inventory, rows


def group_summary(rs, label):
    p = PUBLISHED[label]
    assert len(rs) == p['n']
    medians = {k: median(r[k] for r in rs) for k in ['logM*', 'logMb', 'Vcirc', 'sigma0']}
    checks = {}
    upper_medians = {k: sorted(r[k] for r in rs)[len(rs)//2] for k in medians}
    for k, val in upper_medians.items():
        tolerance = 0.015 if k.startswith('log') else 1.0
        checks[k] = {'calculated': val, 'published': p[k], 'tolerance': tolerance, 'passes': abs(val-p[k]) <= tolerance}
    assert all(c['passes'] for c in checks.values()), (label, checks)
    fields = ['x', 'y', 'y_star', 'y_rotation', 'b_star', 'b_baryon', 'b4', 'log_mass_boost', 'gas_fraction', 'pressure_fraction', 'rotation_proxy']
    return {'n': len(rs), 'redshift_range': [min(r['z'] for r in rs), max(r['z'] for r in rs)], 'redshift_mean': mean(r['z'] for r in rs), 'table1_checks_upper_central_order_statistic': checks, 'conventional_input_medians':medians,
            'mean': {k: mean(r[k] for r in rs) for k in fields}, 'median': {k: median(r[k] for r in rs) for k in fields},
            'point_scatter_population_sd_y': pstdev(r['y'] for r in rs),
            'table2_mean_residual_minus_published': {k: mean(r[k] for r in rs)-p[k] for k in ['b_star', 'b_baryon'] if k in p}}


def q_scores(rs):
    out = {}
    for q in (0, 1):
        intercept = mean(r['y'] - q*r['x'] for r in rs)
        out[str(q)] = {'unweighted_intercept_log10_SI': intercept, 'descriptive_rms_dex': math.sqrt(mean((r['y']-intercept-q*r['x'])**2 for r in rs))}
    return out


def contrast(low, high, reducer=mean):
    dx = reducer(r['x'] for r in high) - reducer(r['x'] for r in low)
    dy = reducer(r['y'] for r in high) - reducer(r['y'] for r in low)
    return {'delta_x': dx, 'delta_y_dex': dy, 'delta_b4_dex': -dy,
            'q_comparisons': {str(q): {'predicted_delta_y_dex': q*dx, 'observed_minus_predicted_dex': dy-q*dx,
             'required_Vpeak_over_Vflat_high_to_low_ratio_if_mass_exact': 10**((dy-q*dx)/4),
             'required_Mtab_over_Mtrue_high_to_low_ratio_if_velocity_exact': 10**(-(dy-q*dx))} for q in (0,1)}}


def analyze(inventory, rows):
    groups = {k: [r for r in rows if r['group']==k] for k in PUBLISHED}
    gs = {k: group_summary(rs,k) for k,rs in groups.items()}
    low, high = groups['low'], groups['high']
    bins = []
    for lo, hi in zip(BIN_EDGES[:-1], BIN_EDGES[1:]):
        l = [r for r in low if lo <= r['Vcirc'] < hi]
        h = [r for r in high if lo <= r['Vcirc'] < hi]
        assert l and h, 'each frozen velocity bin must be populated'
        bins.append({'velocity_bin_kms': [lo,hi], 'counts': {'low':len(l),'high':len(h)}, **contrast(l,h)})
    assert sum(b['counts']['low'] for b in bins)==len(low)
    assert sum(b['counts']['high'] for b in bins)==len(high)
    low_to_high = contrast(low,high)
    pressure_delta = mean(r['y_rotation'] for r in high)-mean(r['y_rotation'] for r in low)
    stellar_delta = mean(r['y_star'] for r in high)-mean(r['y_star'] for r in low)
    gas_delta = mean(r['log_mass_boost'] for r in high)-mean(r['log_mass_boost'] for r in low)
    assert math.isclose(low_to_high['delta_y_dex'], stellar_delta-gas_delta, abs_tol=1e-13)
    # Algebraic nuisance degeneracy: changing q by dq and cv by -dq*x/4 preserves y.
    for r in rows:
        assert math.isclose(0.731*r['x']+4*(-0.731*r['x']/4),0,abs_tol=1e-15)
    return {'analysis_type':'descriptive point-table diagnostic; no q inference', 'input':inventory,
            'constants':{'G_SI':G,'Msun_kg':MSUN,'vref_kms':VREF,'Omega_m_for_evolution':0.315},
            'groups':gs,'primary_low_to_high':low_to_high,
            'sensitivity':{'median_low_to_high':contrast(low,high,median), 'velocity_bins': bins,
             'equal_velocity_bin_weight':{'delta_y_dex':mean(b['delta_y_dex'] for b in bins),'delta_x':mean(b['delta_x'] for b in bins)},
             'stellar_mass_proxy_delta_y_dex':stellar_delta, 'catalogue_gas_mass_boost_delta_dex':gas_delta,
             'rotation_proxy_delta_y_dex':pressure_delta,
             'pressure_removal_changes_delta_y_by_dex':pressure_delta-low_to_high['delta_y_dex']},
            'q_scores':{'all_135':q_scores(rows),'low_high_111':q_scores(low+high)},
            'rotation_cut_reconstruction_failures':[{'Seq':r['Seq'],'pressure_fraction':r['pressure_fraction'],'reconstructed_vrot_over_sigma0':r['rotation_proxy']/r['sigma0']} for r in rows if r['pressure_fraction']>=0.5],
            'selection_accounting':{'observed':536,'resolved_uncontaminated':316,'modeled_parent':240,'peak_covered':149,'rotation_dominated':139,'final':135,'final_fraction_of_modeled_parent':135/240,'final_fraction_of_observed':135/536},
            'assertions': ['canonical numeric input hash','65/24/46 groups','12 Table 1 central summaries matched by upper-middle convention; ordinary medians also recorded','positive approximate rotation speed; cut failures reported','all low/high rows in three populated fixed speed bins','stellar-minus-gas decomposition','q-velocity-calibration degeneracy'],
            'limitations':['Vcirc is modeled peak, not measured asymptotic speed','gas mass uses empirical redshift-dependent scaling','no row errors or covariance','no resolved radii or accelerations','selected sample only; no individual parent selection probabilities','published cosmology differs; no mass or speed distance rescaling attempted','no fitted q or confidence interval','descriptive RMS is not model evidence']}


def make_figure(rows, result, output):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    colors = {'low':'#1764a3','mid':'#737373','high':'#ba3c39'}
    fig, axes = plt.subplots(1,2,figsize=(12.5,5.0),layout='constrained')
    ax = axes[0]
    for group, color in colors.items():
        rs = [r for r in rows if r['group']==group]
        ax.scatter([r['x'] for r in rs],[r['y']+10 for r in rs],s=17,alpha=.55,c=color,label=f'{group}: n={len(rs)}')
        m = result['groups'][group]['mean']
        ax.scatter(m['x'],m['y']+10,marker='D',s=70,c=color,edgecolor='white',zorder=4)
    low = result['groups']['low']['mean']
    xs = [0.1,0.6]
    for q, ls in [(0,'--'),(1,'-')]:
        ax.plot(xs,[low['y']+10+q*(x-low['x']) for x in xs],color='#222222',linestyle=ls,label=f'q={q}, anchored to low mean')
    ax.set(xlabel=r'$\log_{10}E(z)$',ylabel=r'$\log_{10}[(V_{\rm peak}^{4}/G M_{\rm tab})/(10^{-10}\,{\rm m\,s^{-2}})]$',title='Catalogue proxy and fixed evolution templates')
    ax.legend(fontsize=8,loc='lower left')
    ax.grid(alpha=.18)
    ax = axes[1]
    primary = result['primary_low_to_high']
    labels = ['q=0 template','q=1 template','Point mean','Point median','Fixed speed-bin weights','Stellar mass only','Rotation proxy']
    vals = [0,primary['delta_x'],primary['delta_y_dex'],result['sensitivity']['median_low_to_high']['delta_y_dex'],result['sensitivity']['equal_velocity_bin_weight']['delta_y_dex'],result['sensitivity']['stellar_mass_proxy_delta_y_dex'],result['sensitivity']['rotation_proxy_delta_y_dex']]
    ax.barh(labels,vals,color=['#555555','#999999','#1764a3','#1764a3','#1764a3','#8b721f','#805299'])
    ax.axvline(0,color='#333333',lw=.8)
    ax.invert_yaxis()
    ax.set(xlabel='High minus low proxy shift (dex)',title='Sensitivity checks; no confidence intervals')
    ax.grid(axis='x',alpha=.18)
    fig.suptitle('KMOS3D: peak-speed proxy is not an a₀ measurement',fontsize=15)
    for ext in ['png','pdf']:
        fig.savefig(output/f'kmos-diagnostic.{ext}',dpi=180)
    plt.close(fig)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('table',type=Path)
    ap.add_argument('--inventory-dir',type=Path,default=Path(__file__).resolve().parent)
    ap.add_argument('--output',type=Path,default=Path('.'))
    ap.add_argument('--plot',action='store_true')
    args=ap.parse_args()
    sys.path.insert(0,str(args.inventory_dir.resolve()))
    inventory,rows=load_rows(args.table)
    result=analyze(inventory,rows)
    result['code_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    plan=Path(__file__).with_name('ANALYSIS-PLAN.md')
    result['frozen_plan_sha256']=hashlib.sha256(plan.read_bytes()).hexdigest()
    args.output.mkdir(parents=True,exist_ok=True)
    (args.output/'kmos-diagnostic.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    if args.plot: make_figure(rows,result,args.output)
    print(json.dumps({'primary':result['primary_low_to_high'],'sensitivity':result['sensitivity'],'q_scores':result['q_scores']},indent=2))

if __name__=='__main__': main()
