import pefile,re,struct,json,capstone,sys
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
def inline_strings(src,trf):
    pe=pefile.PE(src); d=pe.__data__; N=json.load(open(trf,encoding='utf-8'))
    leas={}
    for s in pe.sections:
        if not s.Characteristics&0x20000000: continue
        o=s.PointerToRawData; tb=d[o:o+s.SizeOfRawData]
        for m in re.finditer(rb'[\x48\x4c]\x8d[\x05\x0d\x15\x1d\x25\x2d\x35\x3d]',tb):
            i=m.start()+3; disp=struct.unpack_from('<i',tb,i)[0]
            leas.setdefault(s.VirtualAddress+i+4+disp,[]).append(o+m.start())
    out={}
    for en,es in N.items():
        eb=en.encode(); p=d.find(b'\0'+eb+b'\0')+1
        if p==0: continue
        rva=pe.get_rva_from_offset(p); L=len(eb)
        for st in leas.get(rva,[]):
            ins=list(md.disasm(d[st:st+40],0))[:5]
            if any(x.mnemonic=='mov' and x.op_str.startswith('byte ptr [') and (f'+ {hex(L)}]' in x.op_str) for x in ins):
                out[en]=es
            lea=list(md.disasm(d[st:st+7],0))
            if lea and any('xmmword ptr ['+lea[0].op_str.split(',')[0]+']' in x.op_str for x in ins[1:]) and struct.pack('<I',L) in d[st-28:st]:
                out[en]=es
            if d[st-6:st-4] in (b'\x41\xb8',b'\x41\xb9') and struct.unpack_from('<I',d,st-4)[0]==L and struct.pack('<I',L) in d[st-28:st-6]:
                out[en]=es
    return out
if __name__=='__main__':
    for src,trf in [('ROCK.dll','tr_rock_na.json'),('PAPER.dll','tr_paper_na.json'),('ROCK_Wall_Climbing.dll','tr_climb_na.json'),('wheelmenu.dll','tr_palm_na.json'),('RPS_UI_Framework.dll','tr_rpsui_na.json')]:
        o=inline_strings(src,trf)
        print(src,len(o))
        for en,es in o.items(): print('  %3d %3d %s | %s'%(len(en),len(es),en,es))
