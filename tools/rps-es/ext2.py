import sys,re,json
f=sys.argv[1]; d=open(f,'rb').read()
out=[]
for m in re.finditer(rb'(?<=\x00)[\x20-\x7e\n\t]{2,}(?=\x00)',d):
    s=m.group().decode()
    out.append((m.start(),s))
json.dump(out,open(f+'.s2.json','w'))
