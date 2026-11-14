import json,sys,re
f=sys.argv[1]; a=json.load(open(f+'.all.json'))
def ui(s):
    if not re.search(r'[a-z]',s) and not re.search(r'[A-Z]{3,} [A-Z]',s): return False
    if s.startswith(('[','.?A','?','@','\\')) or '::' in s or '{}' in s or '{:' in s: return False
    if re.fullmatch(r'[A-Za-z0-9_.]+',s) and not re.fullmatch(r'[A-Z][a-z]+',s): return False
    if re.search(r'\.(dll|cpp|h|hpp|toml|ini|nif|json|log|pex|esp|dds)\b',s,re.I): return False
    if s.startswith('## '): return False
    return True
c=[x for x in a if ui(x[2])]
json.dump(c,open(f+'.ui.json','w'))
print(f,len(c),sum(len(x[2]) for x in c))
