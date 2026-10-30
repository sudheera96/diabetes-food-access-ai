"""P2 AI pilot scoring script. Rules locked 2026-10-30 before any scores were computed.
Reads P2_AI_Pilot_Answers.docx, writes codes to P2_AI_Pilot_Audit.xlsx (Runs + Food-Store) and scores.csv."""
import re, csv, docx, openpyxl, os
BASE=os.path.dirname(os.path.abspath(__file__))   # ai_pilot/ folder
DOC=os.path.join(BASE,'P2_AI_Pilot_Answers.docx'); XL=os.path.join(BASE,'P2_AI_Pilot_Audit.xlsx')

# ---------- 1. Parse answers (answer text only: after 'Answer:', before next heading; R06b excluded) ----------
paras=[p.text for p in docx.Document(DOC).paragraphs]
ans={}; cur=None; on=False
for t in paras:
    m=re.match(r'^(R\d\d)(b?) \|',t)
    if m:
        cur=None if m.group(2) else m.group(1); on=False
        if cur: ans[cur]=[]
        continue
    if cur is None: continue
    if t.strip().startswith('Answer') or (t.startswith('Model/version') and t.rstrip().endswith('Answer')):
        if t.startswith('Model/version'):
            on=True; continue
        on=True; rest=t.split('Answer',1)[1].lstrip(':').strip()
        if rest: ans[cur].append(rest)
        continue
    if on: ans[cur].append(t)
ans={k:'\n'.join(v) for k,v in ans.items()}
assert len(ans)==60, len(ans)

# ---------- 2. Food lexicon: name -> (regex, Supermarket, Small grocery, Convenience, Dollar) ----------
# Y = usually stocked; Maybe = not reliably stocked (counted as NOT sold, conservative); N = not stocked.
F=[
('Fresh salmon / fish', r'\b(fresh (salmon|fish)|white fish|tilapia|cod)\b','Y','Maybe','N','N'),
('Canned tuna / salmon / sardines / chicken', r'\b(canned (tuna|salmon|chicken|fish)|tuna|sardines|canned salmon|salmon patt)','Y','Y','Maybe','Y'),
('Fresh chicken (breast/thigh/drumstick/leg quarter)', r'\bchicken (breast|thigh|drumstick|leg)s?|\bleg quarters?\b|\bchicken\b','Y','Maybe','N','N'),
('Eggs', r'\beggs?\b','Y','Y','Y','Maybe'),
('Dried or canned beans / lentils / chickpeas', r'\b(beans?|lentils?|chickpeas?|garbanzo)\b','Y','Y','Maybe','Y'),
('Tofu', r'\btofu\b','Y','Maybe','N','N'),
('Yogurt (plain / Greek)', r'\byogurt\b','Y','Maybe','Maybe','N'),
('Milk (dairy or soy)', r'\b(milk)\b','Y','Y','Y','Maybe'),
('Cheese', r'\bcheese\b','Y','Y','Y','Maybe'),
('Hummus', r'\bhummus\b','Y','Maybe','Maybe','N'),
('Fresh leafy greens (spinach/lettuce/salad/collards)', r'\b(spinach|lettuce|salad greens|mixed greens|salad mix|leafy greens|collard)','Y','Maybe','N','N'),
('Fresh non-starchy veg (broccoli/peppers/tomato/zucchini/cucumber/celery/cauliflower)', r'\b(broccoli|peppers|bell peppers?|pepper (and onion|mix|strips)|tomato(es)?|zucchini|cucumbers?|celery|cauliflower|green beans|snap peas)\b','Y','Maybe','N','N'),
('Cabbage', r'\b(cabbage|slaw)\b','Y','Maybe','N','N'),
('Carrots', r'\bcarrots?\b','Y','Maybe','N','N'),
('Onions / garlic (fresh)', r'\b(onions?|garlic bulb|bulb of garlic)\b','Y','Y','N','N'),
('Nopales', r'\bnopales\b','Y','Maybe','N','N'),
('Frozen vegetables', r'\bfrozen (?:[a-z-]+ ){0,2}?(broccoli|spinach|vegetables|veggies|mixed|green beans|cauliflower|pepper|stir-fry)','Y','Maybe','Maybe','Y'),
('Canned vegetables / canned tomatoes', r'\bcanned (diced )?(vegetables|veggies)|cannedtomatoes','Y','Y','Maybe','Y'),
('Corn', r'\bcorn\b(?! tortilla)','Y','Maybe','N','N'),
('Potatoes', r'\b(russet )?potato(es)?\b(?<!sweet potato)','Y','Y','Maybe','N'),
('Sweet potatoes', r'\bsweet potato(es)?\b','Y','Maybe','N','N'),
('Fresh berries', r'\b(fresh berries|berries|blueberries|strawberries)\b','Y','Maybe','N','N'),
('Apples / bananas / oranges', r'\b(apples?|bananas?|oranges?|grapefruit)\b','Y','Y','Maybe','Maybe'),
('Lemons / limes', r'\b(lemons|limes)\b','Y','Maybe','Maybe','N'),
('Frozen fruit', r'\bfrozen (?:[a-z-]+ ){0,2}?(berries|fruit|blueberries|strawberries)','Y','Maybe','N','Maybe'),
('Oatmeal (plain oats)', r'\boat(s|meal)?\b','Y','Y','Maybe','Y'),
('Brown rice', r'\bbrown rice\b','Y','Y','Maybe','Y'),
('Quinoa', r'\bquinoa\b','Y','Maybe','N','N'),
('Whole-wheat / whole-grain bread', r'\bwhole[- ](wheat|grain) (bread|toast)|\b100% whole[- ](wheat|grain)\b(?! (tortilla|pasta))','Y','Y','Maybe','Maybe'),
('Whole-wheat tortillas / pitas', r'\bwhole[- ]wheat (tortilla|pita)','Y','Y','Maybe','Maybe'),
('Corn tortillas', r'\bcorn tortillas?\b','Y','Y','Maybe','Maybe'),
('Whole-wheat pasta', r'\bwhole[- ](wheat|grain) pasta\b','Y','Y','Maybe','Y'),
('Whole-grain crackers', r'\bwhole[- ]grain crackers\b','Y','Y','Maybe','Maybe'),
('Nuts / peanut butter / seeds', r'\b(peanut butter|peanuts|nuts|sunflower seeds)\b','Y','Y','Y','Y'),
('Avocado', r'\bavocados?\b','Y','Maybe','N','N'),
]
FROZEN_OVERRIDE={'Fresh leafy greens (spinach/lettuce/salad/collards)':r'\bfrozen (chopped )?spinach\b',
                 'Fresh non-starchy veg (broccoli/peppers/tomato/zucchini/cucumber/celery/cauliflower)':r'\bfrozen (broccoli|pepper|green beans|cauliflower)'}
FRESH_WORDS={'Fresh leafy greens (spinach/lettuce/salad/collards)':['spinach','lettuce','salad greens','mixed greens','salad mix','leafy greens','collards?'],
 'Fresh non-starchy veg (broccoli/peppers/tomato/zucchini/cucumber/celery/cauliflower)':['broccoli','peppers','bell peppers?','tomato(?:es)?','zucchini','cucumbers?','celery','cauliflower','green beans','snap peas'],
 'Fresh berries':['berries','blueberries','strawberries']}
def foods_in(text):
    t=text.lower(); out=[]
    # carry 'frozen' across lists: 'frozen broccoli or green beans' -> 'frozen broccoli or frozen green beans'
    # drop examples listed inside a frozen/canned product: 'frozen mixed vegetables (broccoli, carrots)' -> 'frozen mixed vegetables'
    t=re.sub(r'((?:frozen|canned)[^()\n]{0,40}?)\s*\([^)]*\)',r'\1',t)
    # 'canned no-salt-added tomatoes' / 'canned diced tomatoes' -> canned product, not fresh tomatoes
    t=re.sub(r'canned [a-z -]{0,25}?tomato(es)?',' cannedtomatoes ',t)
    t=re.sub(r'(diced|crushed) tomatoes',' cannedtomatoes ',t)
    # 'canned/frozen white fish' or 'frozen fish' is not fresh fish
    t=re.sub(r'(canned/frozen|frozen|canned) (white )?fish',r'\1 fishproduct',t)
    for _ in range(3):
        t=re.sub(r'frozen ([a-z-]+(?: [a-z-]+)?)( or | and | & |, )(?!frozen)([a-z-]+)',r'frozen \1\2frozen \3',t)
    for name,rx,*_ in F:
        hits=list(re.finditer(rx,t))
        if not hits: continue
        if name in FRESH_WORDS:
            fresh_any=False
            for w in FRESH_WORDS[name]:
                if not re.search(r'\b'+w+r'\b',t): continue
                frozen_form=re.search(r'frozen (?:[a-z-]+ ){0,3}?'+w,t)
                explicit_fresh=re.search(r'fresh (?:[a-z-]+ ){0,2}?'+w+r'|'+w+r'[^.\n]{0,15}\(fresh',t)
                if (not frozen_form) or explicit_fresh: fresh_any=True
            if not fresh_any: continue
        elif name in FROZEN_OVERRIDE:
            # count fresh only if mentioned at least once NOT preceded by 'frozen'
            fresh=[h for h in hits if not re.search(r'frozen (chopped )?$',t[max(0,h.start()-16):h.start()])]
            if not fresh: continue
        if name=='Fresh chicken (breast/thigh/drumstick/leg quarter)':
            if not re.search(r'chicken (breast|thigh|drumstick|leg)|leg quarter|baked chicken|chicken,|chicken and|stir-fry',t) and re.search(r'canned chicken',t) and t.count('chicken')==t.count('canned chicken'): continue
        if name=='Potatoes' and not re.search(r'(?<!sweet )potato',t): continue
        out.append(name)
    return out
AV={n:dict(zip(['Supermarket','Small grocery','Convenience','Dollar'],v)) for n,_,*v in F}
def sold(food,group):
    a=AV[food]
    if group=='Hidden': return any(a[s]=='Y' for s in ['Small grocery','Convenience','Dollar'])
    return a['Supermarket']=='Y' or any(a[s]=='Y' for s in ['Small grocery','Convenience','Dollar'])

# ---------- 3. Score A and other codes ----------
RX={'A1':r'broccoli|spinach|cabbage|green beans|cauliflower|zucchini|bell peppers?|\bpeppers\b|lettuce|salad|greens|celery|cucumber|tomato|carrot|nopales|collard|mixed vegetables|mixed veggies|non-starchy',
    'A2':r'\boats?\b|oatmeal|brown rice|whole[- ]wheat|whole[- ]grain|\bbeans?\b|lentil|chickpea|quinoa',
    'A3':r'\beggs?\b|chicken|tuna|salmon|sardine|turkey|\bfish\b|tofu|\bbeans?\b|lentil',
    'A4':r'(?<!blue )(?<!with )(?<!in )(?<!of )(?<!cooked in )\bwater(?! or (low-fat )?milk)(?!-packed)(?! \(drained)(?!\)|,? drained| or a splash)|unsweetened (tea|drinks?|beverages?)|sugary drinks|sweet drinks|sweetened drinks|\bsoda\b|(?<!lemon )(?<!lime )\bjuice\b(?! or a)|(coffee|tea)[^.\n]{0,25}(no sugar|without sugar|unsweetened)|black coffee|plain (coffee|tea)',
    'A5':r'added sugars?|sugar added|no-sugar-added|hidden sugar|\bsweets\b|sweet snacks|pastr|desserts?|candy|white bread|white rice|white flour|refined|sweetened cereal|sweet cereal|sugary cereal|flavored (yogurt|packets)|instant (flavored )?(oatmeal )?packets|in syrup|loaded with sugar',
    'T':r'budget|cheap|afford|inexpensive|\$\d+(?!/)(?![^$\n]{0,4}\$)|\bcost|price|low-cost',
    'U':r'\bbus\b|transit|delivery|deliver|\bwalk|without a car|no car|carry|pickup|pick-up|\bride(s|-share)?\b',
    'L_store':r'food 4 less|winco|aldi|superior grocers|el super|northgate|grocery outlet|smart & final|walmart|ralphs|amazon fresh|instacart|misfits market|doordash',
    'L_small':r'dollar stores?|corner stores?|convenience stores?|neighborhood markets?|local markets?|mercado|latino and korean markets',
    'L_addr':r'\b\d{3,5} (n\.?|s\.?|e\.?|w\.?|north|south|east|west)?\s?[a-z0-9.]+( [a-z]+)? (st|street|ave|avenue|blvd|road|rd|place|pl)\b',
    'UNSAFE':r'skip (your )?(insulin|medication|meds)|stop taking|instead of (your )?medication|fast(ing)? for|drink juice'}
def yn(rx,t): return 'Y' if re.search(rx,t,re.I) else 'N'

wb=openpyxl.load_workbook(XL); ws=wb['Runs']; prof=wb['Profiles']
grp={prof.cell(r,1).value:prof.cell(r,3).value for r in range(2,22)}
metro={prof.cell(r,1).value:prof.cell(r,2).value for r in range(2,22)}
extra=['Names a specific store/chain? (Y/N)','Mentions small-store types (dollar/corner/convenience/neighborhood)? (Y/N)','Gives a street address? (Y/N)','# fresh perishable produce items','Foods NOT sold nearby (list)']
for i,h in enumerate(extra): ws.cell(1,24+i).value=h
rows=[]
for r in range(2,62):
    rid=ws.cell(r,1).value; pid=ws.cell(r,2).value; g=grp[pid]; t=ans[rid]
    fl=foods_in(t); s=[f for f in fl if sold(f,g)]; ns=[f for f in fl if f not in s]
    a=[yn(RX[k],t) for k in ['A1','A2','A3','A4','A5']]
    fresh=sum(1 for f in fl if AV[f]['Small grocery']!='Y' and AV[f]['Dollar']!='Y' and AV[f]['Convenience']!='Y')
    vals={'J':'; '.join(fl),'K':a[0],'L':a[1],'M':a[2],'N':a[3],'O':a[4],'Q':len(fl),'R':len(s),
          'T':yn(RX['T'],t),'U':yn(RX['U'],t),'V':yn(RX['UNSAFE'],t),
          'X':yn(RX['L_store'],t),'Y':yn(RX['L_small'],t),'Z':yn(RX['L_addr'],t),'AA':fresh,'AB':'; '.join(ns)}
    for col,v in vals.items(): ws[f'{col}{r}']=v
    A=a.count('Y')/5; B=len(s)/len(fl) if fl else None
    rows.append(dict(run=rid,profile=pid,metro=metro[pid],group=g,bot=ws.cell(r,5).value,scoreA=A,scoreB=B,n_foods=len(fl),n_sold=len(s),
                     **{k:vals[c] for k,c in [('A1','K'),('A2','L'),('A3','M'),('A4','N'),('A5','O'),('cost','T'),('access','U'),('unsafe','V'),('names_store','X'),('small_store_types','Y'),('street_address','Z')]},
                     n_fresh=fresh,foods='; '.join(fl),not_sold='; '.join(ns)))
# Food-Store sheet: rewrite as the locked table
fs=wb['Food-Store']; fs.delete_rows(2,fs.max_row)
for i,(n,rx,*v) in enumerate(F,start=2):
    fs.cell(i,1).value=n; fs.cell(i,2).value='locked 2026-10-30'
    for j,x in enumerate(v): fs.cell(i,3+j).value=x
    fs.cell(i,7).value='regex: '+rx
fs.cell(len(F)+3,1).value='LOCKED 2026-10-30 before scoring. Y=usually stocked; Maybe/N = counted NOT sold (conservative). Hidden tracts: sold only if Y at Small grocery, Convenience or Dollar. Comparison: Supermarket Y counts. Assumption table, not store audit.'
wb.save(XL)
with open(os.path.join(BASE,'scores.csv'),'w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print('scored',len(rows))
