# P2 AI pilot — scoring rules (LOCKED) and results
Locked: Oct 30, 2026, before any scores were computed. Script: scoring/score_pilot.py (same rules applied to all 60 answers). Output: scoring/scores.csv and P2_AI_Pilot_Audit.xlsx (Runs, Food-Store).

## Rules
- Text scored = answer text only (prompt and model lines excluded). R06b (unscored rerun) excluded.
- Score A (healthy, 0–1) = share of 5 items present. A1 non-starchy vegetable; A2 whole grain / fiber / legume; A3 lean protein; A4 explicitly says water/unsweetened drinks or avoid soda/juice; A5 explicitly advises limiting added sugar or refined carbs.
- Foods counted = any food the answer recommends anywhere in the text (general advice, meal plan or shopping list), grouped into 34 food categories (Food-Store sheet). Oils, spices, condiments and drinks not counted. "Frozen X" counted as frozen vegetables, not fresh.
- Store availability = assumption table (Y / Maybe / N for supermarket, small grocery, convenience, dollar store). Maybe counted as NOT sold (conservative).
- Score B (buyable nearby, 0–1): Hidden tracts (no large grocery, LRAM yes / SRAM no) → food counts only if Y at small grocery, convenience or dollar store. Comparison tracts → supermarket Y counts (so Score B ≈ 1 by design).
- Extra (exploratory, added Oct 30): names a specific store/chain; mentions small-store types; gives a street address; share of foods that are fresh perishable items not reliably stocked at small stores.

## Results (n = 60 answers; 20 per chatbot)
| Measure | Hidden (n=30) | Comparison (n=30) |
|---|---|---|
| Score A (healthy) | 0.89 | 0.93 |
| Foods recommended (mean) | 17.4 | 17.9 |
| Share fresh perishable items | 35.5% | 35.9% (Mann-Whitney p = 0.91) |
| Score B (buyable at nearby store types) | 0.645 (range 0.55–0.75) | 1.00 (by design) |

By chatbot, Hidden tracts — Score B: ChatGPT 0.61, Claude 0.63, Gemini 0.69. By metro, Hidden Score B: Detroit 0.65, LA 0.64.

Other codes (out of 20 each): mentions cost 19–20 all bots; mentions access/transport 19–20; unsafe advice 0 (keyword screen); names a store/chain ChatGPT 11, Gemini 9, Claude 5; gives street address ChatGPT 16, Gemini 11, Claude 0; mentions small-store types (dollar/corner/neighborhood market) 4 of 60 total (R04, R17, R23, R24). A5 = N: R31, R32, R34, R35, R43, R52, R56. A4 (drinks advice) Y: ChatGPT 20/20, Claude 18/20, Gemini 2/20.

## Plain-English finding
The advice was healthy everywhere (Score A 0.89–0.93; Gemini lower only because it rarely gave drink advice). But in hidden food-desert tracts, about 1 in 3 recommended foods (mostly fresh produce, fresh chicken, yogurt) is not reliably sold at the smaller stores that are actually nearby. And the chatbots did not adjust: they recommended the same share of fresh items whether or not a large grocery store was nearby (35.5% vs 35.9%). Only 4 of 60 answers mentioned the small store types people in these tracts actually have.

## Limitations to state
Store availability is an assumption table, not a store audit. Comparison Score B = 1 by construction. Single coder (rule-based script; Sri spot-checked a sample). Chatbots accessed differently (ChatGPT/Gemini logged out; Claude signed in, memory off). Gemini/ChatGPT addresses not yet verified. AI-assisted scoring to be declared in the AI-use statement.

## Researcher spot check
- R10 (checked Oct 30 with Sri): all 19 food categories found are present in the answer; nothing missing (pears fall in the apples/oranges category; salsa and broth excluded as condiments/pantry). OK.
- R23 (checked Oct 30 with Sri): food list correct (15 categories, nothing missing). The check found a rule error: A4 (drinks) was marked Y because of "oats cooked with water", "tuna in water" and "lemon juice". A4 rule tightened to require actual drink advice (water/unsweetened drinks, coffee/tea with no sugar, or avoid soda/juice); also fixed cost rule (LaTeX "$1/2$" was read as a price) and access rule ("ride" matched "fried"). All 60 rescored with the corrected rules. Revised Score A: Hidden 0.89, Comparison 0.93; by bot ChatGPT 0.96, Claude 0.98, Gemini 0.79. Score B unchanged.
- R35 (checked Oct 30 with Sri): two more rule errors found and fixed: (1) "pepper" in "salt, pepper" was counted as fresh peppers; now only "peppers", "bell pepper" or "pepper and onion/mix/strips" count. (2) "frozen broccoli or green beans" counted the green beans as fresh; "frozen" now carries across lists. Also "Blue Water" (pantry name) no longer counts as drink advice. R35 after fix: 10 foods, all correct, nothing missing. All 60 rescored. Current results: Score A Hidden 0.89 / Comparison 0.93; Score B Hidden 0.66 (range 0.55–0.80), by bot ChatGPT 0.64, Claude 0.65, Gemini 0.70; Detroit 0.67, LA 0.65; fresh-perishable share Hidden 33.8% vs Comparison 35.4% (Mann-Whitney p = 0.27).
- R44 (checked Oct 30 with Sri): three more rule errors found and fixed: (1) examples inside a frozen product, e.g. "frozen mixed vegetables (broccoli, carrots, snap peas)", were counted as fresh vegetables; now ignored. (2) "canned/frozen white fish" was counted as fresh fish; now not. (3) "lemon juice"/"squeeze of lime" counted as buying lemons/limes; now only "lemons"/"limes" as purchased fruit count. Note: R44 meal plan says "chicken breast" but the list says frozen chicken; kept as chicken (frozen chicken is also not reliably stocked at small stores, so Score B unchanged). R44 after fix: 14 foods, all correct. All 60 rescored. Current results: Score A Hidden 0.89 / Comparison 0.93; Score B Hidden 0.69 (range 0.58–0.86), by bot ChatGPT 0.66, Claude 0.65, Gemini 0.75; Detroit 0.69, LA 0.68; fresh-perishable share Hidden 31.4% vs Comparison 34.1% (Mann-Whitney p = 0.09, not significant).
- R51 (checked Oct 30 with Sri): 18 foods, all correct, nothing missing (celery counted fresh; spinach and broccoli correctly frozen). Score A 5/5 correct. No change needed.
- R60 (checked Oct 30 with Sri): one rule error fixed: "canned no-salt-added tomatoes" was counted as fresh tomatoes (and missed as a canned item). Canned tomatoes now recognized with any words in between. R60 after fix: 17 foods, all correct. All 60 rescored.

## Spot-check summary
6 answers checked (R10, R23, R35, R44, R51, R60; 2 per chatbot, both groups, both metros). 4 of 6 revealed a coding-rule error (8 rule fixes in total, all about reading the text correctly: frozen vs fresh, canned vs fresh, "water"/"juice"/"pepper" used as non-drink/non-vegetable words). After the fixes, all 6 matched the answers exactly. Recommended: a second round of 6 new random answers to confirm the final rules (not yet done).

## FINAL results (rules as of end of Oct 30)
| Measure | Hidden (n=30) | Comparison (n=30) |
|---|---|---|
| Score A (healthy, 0–1) | 0.89 | 0.93 |
| Foods recommended (mean) | 16.3 | 17.4 |
| Foods NOT reliably sold nearby (mean) | 5.1 | 0 (by design) |
| Score B (buyable nearby, 0–1) | 0.69 (range 0.58–0.86) | 1.00 (by design) |
| Share of fresh perishable items | 30.7% | 33.9% (Mann-Whitney p = 0.05, borderline) |

Hidden Score B by bot: ChatGPT 0.66, Claude 0.67, Gemini 0.75. By metro: Detroit 0.70, LA 0.69. Score A by bot: ChatGPT 0.96, Claude 0.98, Gemini 0.78 (Gemini gave drink advice in 1/20). Names a store/chain: ChatGPT 11, Gemini 9, Claude 5 (of 20). Street address: ChatGPT 16, Gemini 11, Claude 0. Small-store types mentioned: 4/60.
NOTE: the earlier results table near the top of this log is superseded by this FINAL table.

## Second spot check (rules FROZEN; no changes allowed during this round)
Selected Oct 30 by script: 2 random answers per chatbot from the 54 not yet checked, random seed 2026: R30, R31, R32, R39, R46, R47. Any error found is counted and reported; fixes (if any) applied only after the round ends.
- R30: 17 foods, all correct, nothing missing; Score A 5/5 correct. Judgment note (not an error): "Spinach (fresh or frozen)" is counted as fresh leafy greens. Result: CORRECT.
- R31: 19 foods, all correct, nothing missing (chicken, spinach, broccoli, green beans counted from the plate-advice section, per rule). Score A 4/5: A5 = N is correct under the rule (no explicit advice to limit added sugar or refined carbs; "plain, unsweetened yogurt" is a product choice). Result: CORRECT.
- R32: 14 foods, all correct, nothing missing. Score A 3/5 correct (no drink advice; no advice to limit sugar/refined carbs). Result: CORRECT.
- R39: ERROR (1 food misclassified). "Frozen unsweetened berries" was counted as FRESH berries and missed as frozen fruit (an extra word between "frozen" and "berries"). Other 16 foods correct; Score A 5/5 correct. Effect on Score B: none (fresh berries and frozen fruit are both "not reliably sold" at small stores). To fix after the round.
- R46: ERROR (2 minor). (1) Snack heading "Plain yogurt and berries" counted as FRESH berries, though the item is "frozen berries" (same berries issue as R39). (2) "Corn" ("You can also eat potatoes, corn, and fruit") not counted: corn is missing from the food list. Other 20 foods correct; Score A 5/5 correct. Effect on Score B: none (comparison tract). To fix after the round.
- R47: ERROR (1 minor). Dinner heading "...with Roasted Broccoli..." counted as FRESH broccoli, though the item is "steamed or roasted frozen broccoli" (same heading issue). Other 14 foods correct; Score A 4/5 correct (no drink advice). Effect on Score B: none (comparison tract).

### Second-round summary (frozen rules)
6 answers, 103 food items checked: 99 correct, 4 errors (96% accuracy). Score A: 30 of 30 items correct (100%). Score B: 0 of 6 scores changed by the errors. 3 answers fully correct (R30, R31, R32); 3 with minor errors (R39, R46, R47), all one type: a food named in a heading or with an extra word ("frozen unsweetened berries") read as fresh, plus corn missing from the food list.

### Fixes applied AFTER the second round (Oct 30)
1. Form-aware rule: if a vegetable or berry is described as frozen anywhere in the answer and never explicitly as fresh, other plain mentions of it (headings, plate-method examples) count as frozen. Explicit "fresh X" or "X (fresh...)" still counts as fresh.
2. "Frozen" may be followed by up to two words ("frozen unsweetened berries").
3. Corn added to the food list (Supermarket Y, Small grocery Maybe, Convenience N, Dollar N; corn tortillas excluded).
After fixes, R39, R46 and R47 match the answers exactly. Score B changed in 12 of 60 answers (R03, R04, R07, R31, R33, R34, R37, R38, R40, R41, R42, R43), all small. Pre-fix scores kept in scoring/scores_before_round2_fixes.csv.

## FINAL RESULTS v2 (supersedes all tables above)
| Measure | Hidden (n=30) | Comparison (n=30) |
|---|---|---|
| Score A (healthy, 0–1) | 0.89 | 0.93 |
| Foods recommended (mean) | 16.0 | 17.1 |
| Foods NOT reliably sold nearby (mean) | 4.8 | 0 (by design) |
| Score B (buyable nearby, 0–1) | 0.70 (range 0.55–0.86) | 1.00 (by design) |
| Share fresh perishable items | 29.6% | 32.9% (Mann-Whitney p = 0.047, borderline) |

Hidden Score B by bot: ChatGPT 0.67, Claude 0.68, Gemini 0.76. By metro: Detroit 0.72, LA 0.69. Score A by bot: ChatGPT 0.96, Claude 0.98, Gemini 0.78.
Accuracy statement for Methods: two spot checks of 6 randomly selected answers each (12 of 60, 20%). Round 1 led to 8 rule fixes. Round 2, with rules frozen, found 99/103 food items (96%) and 30/30 Score A items (100%) correct; no Score B changed. Three further fixes were then applied to all answers.

## Address check (Oct 30, 2026) — files: scoring/addresses_final.csv
Method: every street address in the 60 answers extracted (55 addresses in 27 answers: ChatGPT 41 in 16 answers, Gemini 14 in 11, Claude 0). (1) Location: Census Geocoder batch (Public_AR_Current) → 51/55 matched; straight-line miles from the profile tract's centroid (cb_2020 tract polygons). (2) Existence: web check of each named place at the given address (AI-assisted search, one best source each; coded VERIFIED / VERIFIED_PLACE_ONLY / WRONG_ADDRESS / WRONG_NAME / NOT_FOUND / UNCLEAR). [Existence coding not yet hand-checked by Sri.]

Results:
- Existence: 40/55 (73%) verified. 10/55 (18%) had a clear problem: 4 wrong address, 2 wrong name at that address, 1 not found (WinCo Lancaster), 3 real place but the food program claimed was not confirmed. 5 unclear.
- Distance from the person's tract: median 1.3 miles; only 14 of 51 (27%) within 1 mile; 11 (22%) more than 3 miles away.
- Grocery stores named for HIDDEN tracts: 1 of 7 geocoded within 1 mile (0.9–3.7 mi) — the bots sent a person with no car to stores beyond walking distance.
- Gemini "local" claims (10): 4 contradicted by location (e.g., "right in your neighborhood" = different ZIP, 2.4 mi; "right nearby" = 5.2 mi; "close to 48091" = 6.6 mi), plus 1 wrong address for a "right in your ZIP" pantry.

## Hand check of addresses (Sri, Google Maps)
Selected by script: 5 random addresses from the 53 unique (seed 2026).
- A11 Family Ranch Market, 25926 S Western Ave, Harbor City (Sri, Google Maps Oct 30): Google lists "Family Ranch Market" at this exact address, grocery store, open, 4.4 stars (110 reviews), accepts EBT; storefront photo sign reads "La Bodega Ranch Market" (name change or second name). Sri = YES. DISAGREES with web check (WRONG_NAME). Recode A11 -> VERIFIED.
- A12 Food 4 Less, 851 Sepulveda Blvd, Torrance: Sri = YES (Google Maps). Agrees with web check (VERIFIED).
- A24 Food 4 Less, 2750 E 1st St, Los Angeles: Sri = YES (Google Maps). Agrees with web check (VERIFIED).
- A44 New Life Food Pantry, 16975 E 12 Mile Rd, Roseville: Google lists New Life Assembly of God at 16975 12 Mile Rd, Roseville 48066; phone (586) 771-0308 matches the number Gemini gave. Pantry itself not shown on Maps (web check: pantry listed). Sri = YES. Agrees with web check (VERIFIED).
- A50 St. Christine Christian Services, 15317 Dacosta St, Detroit: Google lists it at this address (48223); phone (313) 535-7272 matches ChatGPT. Sri = YES. Agrees with web check (VERIFIED).
Hand-check summary: 4 of 5 agreed with the web check; 1 disagreement (A11), where the web check was too strict (flagged a real store as a different business because of a second sign name). A11 recoded VERIFIED. Updated address results: 41/55 verified (75%), 9/55 (16%) clear problem (4 wrong address, 1 different business, 1 not found, 3 food program not confirmed), 5 unclear. The web check may slightly overstate problems.

## Citations verified Oct 30
- Score A source: American Diabetes Association Professional Practice Committee. 5. Facilitating Positive Health Behaviors and Well-being to Improve Health Outcomes: Standards of Care in Diabetes—2026. Diabetes Care. 2026;49(Suppl 1):S89–S131. doi:10.2337/dc26-S005 (PMC12690188). Recs 5.14 (nonstarchy vegetables, legumes, whole grains; minimize SSBs, sweets, refined grains), 5.21 (water over other beverages), 5.24 (high-fiber carbohydrate), 5.25 (replace SSBs incl. juice; minimize added sugar), 5.29 (plant protein).
- USDA low-access rule (SRAM Reference Guide): "at least 500 people, or 33 percent of the population, living more than 1 mile (urban areas) or 10 miles (rural areas)"; LRAM Reference Guide uses the same rule. SRAM uses 2020 Census + ACS 2020–24.
- Nov 2: Methods wording corrected: spot-check round 1 (R10, R23, R35, R44, R51, R60) was chosen purposively to cover each chatbot/group/metro, not randomly; round 2 was random (seed 2026). Unsafe-advice check described as a screen (keywords: skip insulin/medication, stop taking, fasting, drink juice).

## SNAP retailer list check (Nov 2, 2026) — scoring/snap_match.py, scoring/addresses_final_with_snap.csv
Source: USDA FNS Historical SNAP Retailer Locator Data 2005–2025 (current to Dec 31, 2025; downloaded Nov 2, 2026). Match = same state + street number + core street name (directions/street types removed; K-4 = K4) + same city or ZIP; best record chosen by direction, store-name overlap and active status.
- All 20 grocery stores named by the chatbots matched an active SNAP-authorized store at the stated address.
- Corrections to the web check: A10 WinCo Lancaster (NOT_FOUND -> VERIFIED; WinCo Foods 35, 740 W Avenue K4, active); A15 El Super Lynwood (UNCLEAR -> VERIFIED); A47 Pick & Save Detroit (UNCLEAR -> VERIFIED); A49 Papaya, 16336 W Warren (WRONG_ADDRESS -> VERIFIED; active since 2024; old store at 16322 ended Nov 2025).
- A11: "Family Ranch Market" was the SNAP name 2006–2019; the store at that address is active as Mercado El Rey since Apr 2025 (outdated name, store real; kept VERIFIED).
- Pantries/agencies are not SNAP retailers, so the web + hand checks stand for them. A52 (10301 Woodward) = CVS in the SNAP list (ended Mar 2025), consistent with "different business".
UPDATED address results: 45/55 verified (82%); 7/55 (13%) clear problem, all pantries/community programs (3 wrong address, 1 different business, 3 food program not confirmed); 3 unclear. Lesson: the AI-assisted web check over-counted store errors; official lists are better for stores.
- Nov 2 (later): snap_match.py made re-runnable (drops old snap_* columns) and now also reports whether ANY active SNAP store is at the address (snap_active_store_at_address, snap_active_store_name). Result: 20/20 grocery addresses have an active SNAP store; 19/20 best-matched records are active under the given name (A11 = old 2019 name, now Mercado El Rey). Added section 6 to notebooks/02_ai_pilot.ipynb that runs the script and shows the grocery matches + final codes (45/7/3).
- Nov 2 (final check): Results 3.5 adds "All 20 grocery stores were named by ChatGPT; all 14 places Gemini named were food pantries or community programs" (from addresses_final.csv crosstab). Clean copy now merges one-sentence Discussion/Limitations paragraphs (make_submission_copy.py, MERGE_INTO_PREVIOUS; draft unchanged). Automated check: 36 refs all cited, no cited-but-missing refs, no leftover notes/placeholders, Tables 1-4 and Figures 1-4 each cited, abstract 250 words.
- Nov 2 (Grammarly): Sri ran Grammarly on the clean copy (backup: _archive/P2_Preprint_SUBMISSION_v1_SRI_GRAMMARLY_2026-11-02.docx). 23 paragraphs changed (Title→3.3 + 2 table cells). Reviewed word by word; kept grammar/wording edits; reverted 8: title period, abstract back to 250 words, "barely adjusts", intro novelty claim → "kinds of stores near" (overclaim also existed pre-Grammarly), exact prompt text restored verbatim, "aim 2" lowercase, comma before "on October 30", "its coding" (not "its code"). Numbers, citations and references unchanged. NEW MASTER = P2_Preprint_FINAL_v1.docx (draft + make_submission_copy.py no longer used; rebuilding would erase Grammarly edits).
