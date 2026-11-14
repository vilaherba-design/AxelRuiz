import sys,re,json
f=sys.argv[1]; d=open(f,'rb').read()
out=[]
for m in re.finditer(rb'(?<=\x00)[\x20-\x7e]{2,}(?=\x00)',d):
    s=m.group().decode()
    k=m.start(); j=m.end()
    while j<len(d) and d[j]==0: j+=1
    cap=j-k-1
    out.append((k,cap,s))
json.dump(out,open(f+'.all.json','w'))
print(len(out))
