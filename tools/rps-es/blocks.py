import json,re,sys
def tomlblocks(path):
    L=open(path,encoding='utf-8').read().split('\n'); out=[]; cur=[]
    for l in L:
        if l.startswith('## '): cur.append(l[3:])
        elif l.startswith('##'): cur.append(l[2:].lstrip())
        else:
            if cur: out.append('\n'.join(cur))
            cur=[]
    return out
dll,toml=sys.argv[1],sys.argv[2:]
S=json.load(open(dll+'.s2.json')); idx={s:k for k,s in S}
found=[];miss=[]
for t in toml:
    for b in tomlblocks(t):
        if b in idx: found.append((idx[b],b))
        else: miss.append(b[:80])
print(dll,len(found),'found',len(miss),'miss',sum(len(b) for k,b in found))
json.dump(sorted(set(found)),open(dll+'.blocks.json','w'))
for m in miss[:15]: print('  MISS',repr(m))
