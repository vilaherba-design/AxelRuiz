import json,re,sys
f=sys.argv[1]; lo=int(sys.argv[2],16); hi=int(sys.argv[3],16)
S=json.load(open(f+'.s2.json'))
bad=re.compile(r'(\{\}|\{:|::|__cdecl|\.cpp|\.h\b|std::|\bRE::|%s|%d|\(\)|failed|refused|unavailable|registered|threw|could not|Invalid|invalid)')
for k,s in S:
    if not(lo<=k<hi): continue
    if len(s)<2 or bad.search(s) or s.startswith(('[','##','.?A','?')): continue
    if not re.search('[A-Za-z]',s): continue
    if re.fullmatch(r'[a-z0-9_]+(-[a-z0-9_]+)*',s): continue
    if re.fullmatch(r'[A-Za-z0-9_]+',s) and not re.fullmatch(r'[A-Z][a-z]+([A-Z][a-z]+)?|[A-Z]+',s): continue
    print(hex(k),repr(s)[:160])
