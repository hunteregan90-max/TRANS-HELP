import json,sys
p='assets/questions/questions.json'; d=json.load(open(p,encoding='utf-8'))
expected={'trans_men':('TM',750),'trans_women':('TW',750),'mental_health':('MH',750)}
ids=set(); texts=set()
from collections import Counter
for key,(prefix,n) in expected.items():
    arr=d[key]; assert len(arr)==n,(key,len(arr))
    counts=Counter(q['category'] for q in arr); assert len(counts)==25,(key,len(counts)); assert set(counts.values())=={30},(key,counts)
    for i,q in enumerate(arr,1):
        assert q['id']==f'{prefix}-{i:03d}'
        assert q['id'] not in ids; ids.add(q['id'])
        assert q['question'] not in texts; texts.add(q['question'])
        for field in ['question','category','answer_type','answer_requirement','ai_estimate_eligible','especially_sensitive','prefer_not_to_answer','units','help_text','branching']:
            assert field in q,(q['id'],field)
assert len(ids)==2250
print('VALID: 750/750 TM, 750/750 TW, 750/750 MH; total 2250; unique IDs and question text; required metadata present.')
