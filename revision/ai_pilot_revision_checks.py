# Journal revision checks for the AI pilot (Nov 5 2026):
import warnings; warnings.filterwarnings("ignore")
#  (1) Score B sensitivity analyses using the frozen food-to-store table in score_pilot.py
#  (2) Fresh-perishable comparison that respects clustering (3 answers per tract/profile)
import re, itertools, numpy as np, pandas as pd, statsmodels.formula.api as smf
from scipy.stats import mannwhitneyu
from pathlib import Path
_HERE = Path(__file__).resolve().parent
# Folder holding score_pilot.py + scores.csv: the repo's ai_pilot/ folder (v1.1), else the author's local folder.
SC = next(p for p in [_HERE.parent/'ai_pilot', _HERE.parents[1]/'PhD Paper Notes'/'scoring'] if (p/'score_pilot.py').exists())
src = open(SC/'score_pilot.py', encoding='utf-8').read()
F = eval(src[src.index('F=[')+2: src.index(']\nFROZEN_OVERRIDE')+1])   # frozen table, read only
AV = {n: dict(zip(['Sup','Small','Conv','Dollar'], v)) for n, _, *v in F}
d = pd.read_csv(SC/'scores.csv')
d['food_list'] = d['foods'].fillna('').apply(lambda s: [x.strip() for x in s.split(';') if x.strip()])
SMALL = ['Small','Conv','Dollar']
rules = {
 'B_main (Y only; maybe = not buyable)':     lambda a: any(a[s]=='Y' for s in SMALL),
 'B_maybe_buyable (Y or Maybe = buyable)':   lambda a: any(a[s] in ('Y','Maybe') for s in SMALL),
 'B_small_grocery_present (Y at small grocery only)': lambda a: a['Small']=='Y',
 'B_convenience_dollar_only (no small grocery)':      lambda a: any(a[s]=='Y' for s in ['Conv','Dollar']),
}
h = d[d.group=='Hidden'].copy()
rows=[]
for name, f in rules.items():
    sc = h['food_list'].apply(lambda L: np.mean([f(AV[x]) for x in L]) if L else np.nan)
    chk = ''
    if name.startswith('B_main'): chk = f" (max diff vs scores.csv: {np.nanmax(abs(sc-h.scoreB)):.4f})"
    rows.append({'Rule':name,'Mean':round(sc.mean(),3),'Min':round(sc.min(),3),'Max':round(sc.max(),3),
                 'ChatGPT':round(sc[h.bot=='ChatGPT'].mean(),3),'Claude':round(sc[h.bot=='Claude'].mean(),3),
                 'Gemini':round(sc[h.bot=='Gemini'].mean(),3),'Check':chk})
# three-way split: clearly buyable / uncertain (maybe) / not stocked
def split(L):
    c={'yes':0,'maybe':0,'no':0}
    for x in L:
        a=AV[x]
        if any(a[s]=='Y' for s in SMALL): c['yes']+=1
        elif any(a[s]=='Maybe' for s in SMALL): c['maybe']+=1
        else: c['no']+=1
    n=len(L); return pd.Series({k:v/n for k,v in c.items()})
sp = h['food_list'].apply(split).mean().round(3)
sb = pd.DataFrame(rows); sb.to_csv('S3_scoreB_sensitivity.csv', index=False)
print(sb.drop(columns='Check').to_string(index=False)); print(rows[0]['Check'])
print('Hidden tracts, share of recommended foods: buyable', sp['yes'], '| uncertain (maybe)', sp['maybe'], '| not stocked', sp['no'])

# ---------- (2) fresh perishable share, clustered by profile ----------
d['share_fresh'] = d.n_fresh/d.n_foods
hh, cc = d[d.group=='Hidden'].share_fresh, d[d.group=='Comparison'].share_fresh
p_mw = mannwhitneyu(hh, cc).pvalue
prof = d.groupby(['profile','metro','group'], as_index=False).share_fresh.mean()
obs = prof[prof.group=='Hidden'].share_fresh.mean() - prof[prof.group=='Comparison'].share_fresh.mean()
# exact permutation: shuffle hidden/comparison labels among the 10 profiles WITHIN each metro (all 252 x 252 splits)
parts = {}
for m, g in prof.groupby('metro'):
    v = g.share_fresh.values; parts[m] = [(v[list(c)].sum(), v.sum()-v[list(c)].sum()) for c in itertools.combinations(range(len(v)),5)]
nh = (prof.group=='Hidden').sum(); nc = len(prof)-nh
(m1, m2) = parts.keys()
diffs = np.array([(a1+a2)/nh - (b1+b2)/nc for (a1,b1) in parts[m1] for (a2,b2) in parts[m2]])
p_perm = np.mean(np.abs(diffs) >= abs(obs)-1e-12)
# mixed model: answer-level, chatbot + metro fixed, random intercept per profile (tract)
mm = smf.mixedlm('share_fresh ~ C(group, Treatment("Comparison")) + C(bot) + C(metro)', d, groups=d['profile']).fit(reml=True)
k = [i for i in mm.params.index if 'group' in i][0]; ci = mm.conf_int().loc[k]
# cluster bootstrap (resample profiles within metro x group)
rng = np.random.default_rng(2026); bs=[]
for _ in range(5000):
    # resample tracts with replacement within each metro x group (written without groupby.apply so it runs on pandas 2 and 3)
    idx = [i for _, g in prof.groupby(['metro','group']) for i in rng.choice(g.index.to_numpy(), len(g), replace=True)]
    s = prof.loc[idx]
    bs.append(s[s.group=='Hidden'].share_fresh.mean()-s[s.group=='Comparison'].share_fresh.mean())
lo, hi = np.percentile(bs,[2.5,97.5])
small = d.groupby('group').small_store_types.apply(lambda s:(s=='Y').sum())
res = pd.Series({'Hidden mean (answers)':round(hh.mean(),4),'Comparison mean (answers)':round(cc.mean(),4),
 'Original Mann-Whitney p (60 answers treated as independent)':round(p_mw,4),
 'Difference, profile level (hidden - comparison)':round(obs,4),
 'Exact stratified permutation p (labels shuffled within metro, 63,504 splits)':round(p_perm,4),
 'Mixed model difference':round(mm.params[k],4),'Mixed model 95% CI':f"{ci[0]:.4f} to {ci[1]:.4f}",'Mixed model p':round(mm.pvalues[k],4),
 'Cluster bootstrap 95% CI (5,000 resamples of tracts)':f"{lo:.4f} to {hi:.4f}",
 'Answers mentioning small store types: Hidden / Comparison':f"{small.get('Hidden',0)} of 30 / {small.get('Comparison',0)} of 30"})
res.to_csv('S4_fresh_share_clustered_test.csv', header=['value']); print(res.to_string())
