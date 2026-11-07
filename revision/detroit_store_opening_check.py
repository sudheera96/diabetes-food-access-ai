# Journal revision (Nov 5 2026): did "hidden" food-desert tracts gain a large store between 2019 and 2025?
# LRAM uses 2019 stores; SRAM uses 2025 stores. Using the USDA FNS Historical SNAP Retailer Locator (2005-2025),
# count LARGE SNAP stores (Supermarket, Super Store, Large Grocery Store) that were first authorized
# 2019-01-01..2025-12-31 and still active at end of 2025, within 1 mile of each hidden tract (tract edge, straight line).
# Also: for the 10 hidden AI-pilot tracts, which SNAP store types are actually within 1 mile (for Score B rule choice).
import warnings; warnings.filterwarnings('ignore')
import pandas as pd, geopandas as gpd, numpy as np, zipfile, re
from pathlib import Path
BASE = Path(__file__).resolve().parent.parent; RAW = BASE/'data'/'raw'; CLEAN = BASE/'data'/'clean'
df = pd.read_csv(CLEAN/'tracts_ca_mi_with_lram.csv', dtype={'GEOID':str})
df['hidden'] = (df.lram_1_10==1) & (df.lila_1_10==0)
with zipfile.ZipFile(RAW/'snap-retailer-locator-data2005-2025.zip') as z:
    s = pd.read_csv(z.open(z.namelist()[0]), dtype=str, encoding='utf-8-sig')
s = s[s.State.isin(['MI','CA'])].copy()
s['auth'] = pd.to_datetime(s['Authorization Date'], errors='coerce'); s['end'] = pd.to_datetime(s['End Date'].str.strip().replace('', None), errors='coerce')
s['active_2025'] = s.end.isna() | (s.end >= '2025-12-31')
s['active_2019'] = (s.auth <= '2019-12-31') & (s.end.isna() | (s.end >= '2019-01-01'))
s['large'] = s['Store Type'].isin(['Supermarket','Super Store','Large Grocery Store'])
s['dollar'] = s['Store Name'].str.upper().str.contains(r'DOLLAR GENERAL|FAMILY DOLLAR|DOLLAR TREE|99 CENTS|99 CENT ONLY|DOLLAR STORE', regex=True, na=False)
s['new_large'] = s.large & ~s.dollar & s.active_2025 & (s.auth >= '2019-01-01')
s = s.dropna(subset=['Latitude','Longitude'])
st = gpd.GeoDataFrame(s, geometry=gpd.points_from_xy(s.Longitude.astype(float), s.Latitude.astype(float)), crs=4326)
tr = pd.concat([gpd.read_file(RAW/'cb_2020_06_tract_500k.zip'), gpd.read_file(RAW/'cb_2020_26_tract_500k.zip')])[['GEOID','geometry']]
METERS_MI = 1609.344
def near(tracts, stores, crs):
    t = tracts.to_crs(crs).copy(); t['geometry'] = t.buffer(METERS_MI)
    j = gpd.sjoin(stores.to_crs(crs), t[['GEOID','geometry']], predicate='within')
    return j
rows = []; detail = []
for metro, crs in [('Metro Detroit', 26917), ('Metro Los Angeles', 26911)]:
    h = tr.merge(df[(df.metro==metro) & df.hidden], on='GEOID')
    j = near(h, st, crs)
    nl = j[j.new_large].groupby('GEOID').size()
    for sub, lab in [(h, 'All hidden tracts'), (h[h.high_diab], 'High-diabetes hidden tracts')]:
        g = sub.GEOID; k = nl.reindex(g).fillna(0)
        adults_diab = (sub.diab/100*sub.adults)
        gained = k.values > 0
        rows.append({'Metro':metro,'Tracts':lab,'n':len(sub),
            'Tracts with >=1 large store newly authorized 2019-2025 within 1 mi':int(gained.sum()),
            'Share':f"{gained.mean():.0%}",
            'Tracts with no new large store':int((~gained).sum()),
            'Adults with diabetes in tracts with no new large store':int(adults_diab[~gained].sum()),
            'Adults with diabetes, all':int(adults_diab.sum())})
    dj = j[j.new_large].drop_duplicates(['Record ID','GEOID'])
    dj = dj.assign(metro=metro)[['metro','GEOID','Store Name','Store Type','Street Number','Street Name','City','auth']]
    detail.append(dj)
res = pd.DataFrame(rows); res.to_csv('S5_store_opening_check.csv', index=False)
pd.concat(detail).to_csv('S5_new_large_stores_detail.csv', index=False)
print(res.to_string(index=False))
d = pd.concat(detail); print('\nDistinct new large stores near Detroit hidden tracts:', d[d.metro=='Metro Detroit']['Store Name'].nunique())
print(d[d.metro=='Metro Detroit'].drop_duplicates('Store Name')[['Store Name','Store Type','City','auth']].head(40).to_string(index=False))

# ---- pilot hidden tracts: what store types are actually within 1 mile (active 2025)? ----
pil = pd.read_csv(CLEAN/'ai_pilot_tracts.csv', dtype={'GEOID':str})
out=[]
for metro, crs in [('Metro Detroit', 26917), ('Metro Los Angeles', 26911)]:
    p = tr.merge(pil[(pil.metro==metro)], on='GEOID')
    j = near(p, st[st.active_2025], crs)
    j['cat'] = np.select([j.large & ~j.dollar, j.dollar, j['Store Type'].isin(['Medium Grocery Store','Small Grocery Store','Combination Grocery/Other']), j['Store Type']=='Convenience Store'],
                         ['Large store','Dollar store','Small/medium grocery or combination','Convenience'], 'Other/specialty')
    c = j.groupby(['GEOID','cat']).size().unstack(fill_value=0)
    c = p[['GEOID','grp','zip']].set_index('GEOID').join(c).fillna(0)
    c.insert(0,'metro',metro); out.append(c)
o = pd.concat(out); o.to_csv('S6_pilot_tract_store_mix_1mi.csv'); print('\n', o.to_string())
