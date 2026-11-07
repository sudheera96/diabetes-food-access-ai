# (a) How many "new" large stores are really re-authorizations (an older SNAP record at the same address)?
# (b) Bundle S1-S6 into one supplementary workbook.
import warnings; warnings.filterwarnings('ignore')
import pandas as pd, zipfile
from pathlib import Path
RAW = Path(__file__).resolve().parent.parent/'data'/'raw'
with zipfile.ZipFile(RAW/'snap-retailer-locator-data2005-2025.zip') as z:
    s = pd.read_csv(z.open(z.namelist()[0]), dtype=str, encoding='utf-8-sig')
s = s[s.State.isin(['MI','CA'])].copy()
s['auth'] = pd.to_datetime(s['Authorization Date'], errors='coerce')
norm = lambda x: x.fillna('').str.upper().str.replace(r'\s+',' ',regex=True).str.strip()
s['addr'] = norm(s['Street Number'])+'|'+norm(s['Street Name'])+'|'+norm(s['City'])
first = s.groupby('addr').auth.min()
d = pd.read_csv('S5_new_large_stores_detail.csv', dtype=str); d['auth']=pd.to_datetime(d.auth)
d['addr'] = norm(d['Street Number'])+'|'+norm(d['Street Name'])+'|'+norm(d['City'])
d['earlier_record_same_address'] = d.addr.map(first) < d.auth
d['first_snap_record_at_address'] = d.addr.map(first).dt.date
d.drop(columns='addr').to_csv('S5_new_large_stores_detail.csv', index=False)
u = d.drop_duplicates(['metro','Store Name','Street Number','Street Name'])
print(u.groupby('metro').earlier_record_same_address.agg(['sum','count']))
xl = 'P2_Supplementary_Tables_S1-S6.xlsx'
with pd.ExcelWriter(xl) as w:
    for f, sh in [('S1_regression_table.csv','S1 Regression'),('S1_model_fit.csv','S1 Model fit'),('S2_all_55_named_places.csv','S2 Named places'),
                  ('S3_scoreB_sensitivity.csv','S3 Score B sensitivity'),('S4_fresh_share_clustered_test.csv','S4 Fresh share test'),
                  ('S5_store_opening_check.csv','S5 Store opening (edge)'),('S5b_store_opening_check_centroid.csv','S5b Store opening (centroid)'),
                  ('S5_new_large_stores_detail.csv','S5d New stores detail'),('S6_pilot_tract_store_mix_1mi.csv','S6 Pilot store mix'),
                  ('S6b_pilot_nearest_large_store_2025.csv','S6b Pilot nearest large')]:
        pd.read_csv(f).to_excel(w, sheet_name=sh[:31], index=False)
print('saved', xl)
