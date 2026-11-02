"""Match chatbot-named addresses to the USDA FNS SNAP Retailer Locator list (2005-2025, current to Dec 31, 2025).
Match rule: same state, same street number, and the core street name matches after normalizing
(directions, street types, number words like EIGHT->8 removed/normalized). Active = no End Date."""
import zipfile, re, os, pandas as pd
HERE=os.path.dirname(os.path.abspath(__file__))          # ai_pilot/
REPO=os.path.dirname(HERE)
RAW=os.path.join(REPO,'data','raw','snap-retailer-locator-data2005-2025.zip')
z=zipfile.ZipFile(RAW); s=pd.read_csv(z.open(z.namelist()[0]),encoding='utf-8-sig',dtype=str,low_memory=False)
s.columns=[c.strip() for c in s.columns]; s=s[s.State.isin(['CA','MI'])].copy()
NUM={'ONE':'1','TWO':'2','THREE':'3','FOUR':'4','FIVE':'5','SIX':'6','SEVEN':'7','EIGHT':'8','NINE':'9','TEN':'10','ELEVEN':'11','TWELVE':'12','FIRST':'1ST','SECOND':'2ND','THIRD':'3RD','FOURTH':'4TH'}
DROP={'N','S','E','W','NORTH','SOUTH','EAST','WEST','ST','STREET','AVE','AVENUE','BLVD','BOULEVARD','RD','ROAD','DR','DRIVE','PL','PLACE','HWY','HIGHWAY','WAY','LN','LANE','SUITE','STE','UNIT','A'}
def core(name):
    t=re.sub(r'(?<=[A-Z0-9])-(?=[A-Z0-9])','',str(name).upper())   # K-4 -> K4
    t=re.sub(r'[^A-Z0-9 ]',' ',t).split()
    t=[NUM.get(x,x) for x in t]
    t=[x for x in t if x not in DROP and not re.fullmatch(r'\d{3,}',x)]
    return ' '.join(t)
s['num']=s['Street Number'].fillna('').str.strip().str.upper()
s['core']=s['Street Name'].map(core)
s['active']=s['End Date'].isna() | (s['End Date'].fillna('').str.strip()=='')
a=pd.read_csv(os.path.join(HERE,'addresses_final.csv'),dtype=str)
a=a.drop(columns=[c for c in a.columns if c.startswith('snap_')])   # re-runnable: drop old SNAP columns
out=[]
for _,r in a.iterrows():
    m=re.match(r'\s*(\d+[A-Z\-]*)\s+(.*)',r['street'].upper())
    num,rest=(m.group(1),m.group(2)) if m else ('',r['street'])
    c=core(rest)
    cand=s[(s.State==r['state'])&(s.num==num)]
    mask=cand.core.apply(lambda x: bool(x) and bool(c) and (x==c or c in x or x in c)).astype(bool) if len(cand) else pd.Series(dtype=bool)
    hit=cand.loc[mask] if len(cand) else cand
    # same city or same ZIP (5-digit) as the address the chatbot gave / the Census geocoder returned
    zips={z for z in [str(r.get('zip_given','')).split('.')[0], str(r.get('census_zip','')).split('.')[0]] if z and z!='nan'}
    hit=hit[(hit.City.str.upper().str.strip()==str(r['city']).upper().strip()) | (hit['Zip Code'].str[:5].isin(zips))]
    if len(hit):
        d0=(re.match(r'(N|S|E|W)\b',rest.strip()) or [None])[0]
        nm=set(re.sub(r'[^A-Z ]',' ',str(r['place_name']).upper()).split())-{'THE','OF','AND','FOOD','MARKET','CENTER'}
        def score(h):
            sc=0
            if d0 and str(h['Street Name']).upper().startswith(d0+' '): sc+=1
            sc+=2*len(nm & set(re.sub(r'[^A-Z ]',' ',str(h['Store Name']).upper()).split()))
            sc+=1 if h['active'] else 0
            return sc
        hit=hit.assign(_s=hit.apply(score,axis=1)).sort_values('_s',ascending=False)
        h=hit.iloc[0]
        out.append(dict(id=r['id'],snap_match='Y',snap_store_name=h['Store Name'],snap_store_type=h['Store Type'],snap_active_2025='Y' if h['active'] else 'N (ended '+str(h['End Date'])+')',snap_records=len(hit),snap_active_store_at_address='Y' if hit['active'].any() else 'N',snap_active_store_name=(hit[hit['active']]['Store Name'].iloc[0] if hit['active'].any() else '')))
    else:
        out.append(dict(id=r['id'],snap_match='N',snap_store_name='',snap_store_type='',snap_active_2025='',snap_records=0,snap_active_store_at_address='',snap_active_store_name=''))
res=a.merge(pd.DataFrame(out),on='id')
res.to_csv(os.path.join(HERE,'addresses_final_with_snap.csv'),index=False)
pd.set_option('display.width',250); pd.set_option('display.max_colwidth',45)
print(res[['id','bot','place_type','place_name','street','code','snap_match','snap_store_name','snap_store_type','snap_active_2025']].to_string(index=False))
