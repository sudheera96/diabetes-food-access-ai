# Stricter version of the store checks: distance from tract CENTROID (not tract edge).
import warnings; warnings.filterwarnings('ignore')
exec(open('detroit_store_opening_check.py').read().split("METERS_MI = 1609.344")[0])
METERS_MI = 1609.344
rows=[]; pil = pd.read_csv(CLEAN/'ai_pilot_tracts.csv', dtype={'GEOID':str}); prow=[]
for metro, crs in [('Metro Detroit', 26917), ('Metro Los Angeles', 26911)]:
    big = st[st.large & ~st.dollar].to_crs(crs)
    def dist_to(sel, pts):
        from shapely.strtree import STRtree
        g = list(sel.geometry); tree = STRtree(g)
        idx = tree.nearest(list(pts.geometry)); return np.array([pts.geometry.iloc[i].distance(g[j]) for i,j in enumerate(idx)])/METERS_MI
    h = tr.merge(df[(df.metro==metro) & df.hidden], on='GEOID').to_crs(crs); c = h.copy(); c['geometry']=h.centroid
    d19 = dist_to(big[big.active_2019], c); d25 = dist_to(big[big.active_2025], c); dnew = dist_to(big[big.new_large], c)
    c['nearest_large_2019_mi']=d19; c['nearest_large_2025_mi']=d25; c['nearest_new_large_mi']=dnew
    for sub, lab in [(c,'All hidden'),(c[c.high_diab],'High-diabetes hidden')]:
        gained = sub.nearest_new_large_mi<=1
        ad = sub.diab/100*sub.adults
        rows.append({'Metro':metro,'Tracts':lab,'n':len(sub),'New large store <=1 mi of centroid':int(gained.sum()),
                     'Remaining hidden':int((~gained).sum()),'Adults w/ diabetes remaining':int(ad[~gained].sum()),
                     'Median mi to nearest large store 2019':round(sub.nearest_large_2019_mi.median(),2),
                     'Median mi to nearest large store 2025':round(sub.nearest_large_2025_mi.median(),2)})
    p = tr.merge(pil[pil.metro==metro], on='GEOID').to_crs(crs); pc=p.copy(); pc['geometry']=p.centroid
    pc['nearest_large_2025_mi']=dist_to(big[big.active_2025], pc)
    prow.append(pc[['GEOID','metro','grp','zip','nearest_large_2025_mi']])
r=pd.DataFrame(rows); r.to_csv('S5b_store_opening_check_centroid.csv',index=False); print(r.to_string(index=False))
pp=pd.concat(prow).round(2); pp.to_csv('S6b_pilot_nearest_large_store_2025.csv',index=False); print(pp.sort_values(['grp','metro']).to_string(index=False))
