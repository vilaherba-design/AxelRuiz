import json,re,sys
f=sys.argv[1]; lo=int(sys.argv[2],16); hi=int(sys.argv[3],16)
S=json.load(open(f+'.s2.json'))
bad=re.compile(r'(\{\}|\{:|::|__cdecl|\.cpp|\.h\b|std::|\bRE::|%s|%d|%u|%I64|\(\)|failed|refused|registered|threw|could not|[Ii]nvalid|faulted|installed|exception|D3D|0x)')
out=[]
for k,s in S:
    if not(lo<=k<hi): continue
    if len(s)<3 or bad.search(s) or s.startswith(('[','##','.?A','?','#','RPS UI Framework ','ROCK:','PAPER:','PALM:')): continue
    if '\t' in s or not re.search('[A-Za-z]{3}',s): continue
    if re.fullmatch(r'[a-z0-9_.]+(-[a-z0-9_.]+)*',s): continue
    if re.fullmatch(r'[A-Za-z0-9_]+',s) and not re.fullmatch(r'[A-Z][a-z]+',s): continue
    out.append((k,s))
for k,s in out: print(hex(k),repr(s)[:170])
print(len(out),file=sys.stderr)
