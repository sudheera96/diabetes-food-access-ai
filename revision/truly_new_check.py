# Best estimate: count only large stores at addresses with NO earlier SNAP record (truly new sites, not re-authorizations).
import warnings; warnings.filterwarnings('ignore')
exec(open('detroit_store_opening_check.py').read().split("METERS_MI = 1609.344")[0])
norm = lambda x: x.fillna('').str.upper().str.replace(r'\s+',' ',regex=True).str.strip()
st['addr'] = norm(st['Street Number'])+'|'+norm(st['Street Name'])+'|'+norm(st['City'])
first = st.groupby('addr').auth.min()
st['truly_new'] = st.new_large & (st.addr.map(first) >= '2019-01-01')
M = 1609.344; rows=[]
for metro, crs in [('Metro Detroit', 26917), ('Metro Los Angeles', 26911)]:
    h = tr.merge(df[(df.metro==metro) & df.hidden], on='GEOID').to_crs(crs)
    tn = st[st.truly_new].to_crs(crs)
    e = h.copy(); e['geometry']=h.buffer(M); je = gpd.sjoin(tn, e[['GEOID','geometry']], predicate='within').GEOID.unique()
    c = h.copy(); c['geometry']=h.centroid.buffer(M); jc = gpd.sjoin(tn, c[['GEOID','geometry']], predicate='within').GEOID.unique()
    for sub, lab in [(h,'All hidden'),(h[h.high_diab],'High-diabetes hidden')]:
        ad = sub.diab/100*sub.adults
        ge, gc = sub.GEOID.isin(je), sub.GEOID.isin(jc)
        rows.append({'Metro':metro,'Tracts':lab,'n':len(sub),'Truly new large store <=1 mi of edge':int(ge.sum()),
          'Remaining (edge rule)':int((~ge).sum()),'Adults w/ diabetes remaining (edge)':int(ad[~ge].sum()),
          'Truly new large store <=1 mi of centroid':int(gc.sum()),'Remaining (centroid rule)':int((~gc).sum()),
          'Adults w/ diabetes remaining (centroid)':int(ad[~gc].sum()),'Truly new large stores in metro area checked':int(len(set(tn.index)))})
r = pd.DataFrame(rows); r.to_csv('S5c_truly_new_stores_only.csv', index=False); print(r.drop(columns='Truly new large stores in metro area checked').to_string(index=False))
with pd.ExcelWriter('P2_Supplementary_Tables_S1-S6.xlsx', mode='a', engine='openpyxl') as w: r.to_excel(w, sheet_name='S5c Truly new stores', index=False)
