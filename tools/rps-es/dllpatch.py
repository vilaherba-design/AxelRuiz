# Traduce literales de un dll x64 moviéndolos a una sección nueva .rdes y repuntando referencias.
import pefile,struct,sys,json,capstone,re,hashlib
def align(x,a): return (x+a-1)//a*a
def run(src,trfile,dst,report=None):
    T=json.load(open(trfile,encoding='utf-8'))
    pe=pefile.PE(src); d=bytearray(pe.__data__); base=pe.OPTIONAL_HEADER.ImageBase
    FA=pe.OPTIONAL_HEADER.FileAlignment; SA=pe.OPTIONAL_HEADER.SectionAlignment
    # relocs
    relset=set()
    if hasattr(pe,'DIRECTORY_ENTRY_BASERELOC'):
        for b in pe.DIRECTORY_ENTRY_BASERELOC:
            for e in b.entries:
                if e.type==10: relset.add(e.rva)
    execs=[s for s in pe.sections if s.Characteristics & 0x20000000]
    md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64); md.detail=False
    last=pe.sections[-1]
    newrva=align(last.VirtualAddress+last.Misc_VirtualSize,SA)
    newraw=align(len(d),FA)
    blob=bytearray(); log=[]; plan=[]
    # index all rip-rel lea targets once
    leas={}
    for s in execs:
        o=s.PointerToRawData; tb=bytes(d[o:o+s.SizeOfRawData]); r=s.VirtualAddress
        for m in re.finditer(rb'[\x48\x4c]\x8d[\x05\x0d\x15\x1d\x25\x2d\x35\x3d]',tb):
            i=m.start()+3
            if i+4>len(tb): continue
            disp=struct.unpack_from('<i',tb,i)[0]; tgt=r+i+4+disp
            leas.setdefault(tgt,[]).append((o+i,r+i+4))
    abs_={}
    for s in pe.sections:
        if s in execs: continue
        o=s.PointerToRawData; r=s.VirtualAddress
        for k in range(0,s.SizeOfRawData-7,8):
            v=struct.unpack_from('<Q',d,o+k)[0]
            if base<=v<base+newrva and (r+k) in relset: abs_.setdefault(v-base,[]).append(o+k)
    for en,es in T.items():
        eb=en.encode(); sb=es.encode('utf-8')
        pos=[m.start()+1 for m in re.finditer(re.escape(b'\0'+eb+b'\0'),d)]
        if not pos: log.append(('NOTFOUND',en)); continue
        nl=0; na=0; nimm=0
        off_new=len(blob); blob+=sb+b'\0'
        nva=newrva+off_new
        for p in pos:
            rva=pe.get_rva_from_offset(p)
            for fo,iend in leas.get(rva,[]):
                struct.pack_into('<i',d,fo,nva-iend); nl+=1
                # buscar mov imm == len en las 4 instrucciones siguientes
                code=bytes(d[fo+4:fo+4+40])
                for ins in list(md.disasm(code,0))[:4]:
                    if ins.mnemonic=='mov' and ins.op_str.split(', ')[-1] in (hex(len(eb)),str(len(eb))) and ins.size>=5:
                        # imm32 al final
                        st=fo+4+ins.address; immo=st+ins.size-4
                        if struct.unpack_from('<I',d,immo)[0]==len(eb):
                            struct.pack_into('<I',d,immo,len(sb)); nimm+=1
                # mov r8d/edx/r9d, imm32 justo antes del lea (hasta 24 bytes)
                lea_st=fo-3
                # mov qword [rsp+X], imm32 justo antes (args de format: string_view en pila)
                k=lea_st-9
                if d[k:k+4]==b'\x48\xc7\x44\x24' and struct.unpack_from('<I',d,k+5)[0]==len(eb):
                    struct.pack_into('<I',d,k+5,len(sb)); nimm+=1
                for op in (b'\x41\xb8',b'\xba',b'\x41\xb9',b'\x49\xc7\xc0'):
                    for k in range(lea_st-24,lea_st):
                        if d[k:k+len(op)]==op and k+len(op)+4<=lea_st and struct.unpack_from('<I',d,k+len(op))[0]==len(eb) and k+len(op)+4==lea_st:
                            struct.pack_into('<I',d,k+len(op),len(sb)); nimm+=1
            for fo in abs_.get(rva,[]):
                struct.pack_into('<Q',d,fo,base+nva); na+=1
                if struct.unpack_from('<Q',d,fo+8)[0]==len(eb): struct.pack_into('<Q',d,fo+8,len(sb)); nimm+=1
        if nl+na==0:
            # en sitio si cabe
            done=False
            for p in pos:
                j=p+len(eb)
                while j<len(d) and d[j]==0: j+=1
                cap=j-p-1
                if len(sb)<=cap: d[p:p+cap+1]=sb+b'\0'*(cap+1-len(sb)); done=True
            log.append(('INPLACE' if done else 'NOREF',en))
        else: log.append(('OK',en,nl,na,nimm))
    # añadir sección
    hdr_end=pe.sections[-1].get_file_offset()+40
    assert hdr_end+40<=pe.OPTIONAL_HEADER.SizeOfHeaders, 'sin hueco de cabecera'
    rawsz=align(len(blob),FA); vsz=len(blob)
    d+=b'\0'*(newraw-len(d)); d+=blob+b'\0'*(rawsz-len(blob))
    sh=struct.pack('<8sIIIIIIHHI',b'.rdes\0\0\0',vsz,newrva,rawsz,newraw,0,0,0,0,0x40000040)
    d[hdr_end:hdr_end+40]=sh
    fh=pe.FILE_HEADER.get_file_offset(); struct.pack_into('<H',d,fh+2,pe.FILE_HEADER.NumberOfSections+1)
    oh=pe.OPTIONAL_HEADER.get_file_offset()
    struct.pack_into('<I',d,oh+56,align(newrva+vsz,SA))  # SizeOfImage
    struct.pack_into('<I',d,oh+64,0) # checksum
    open(dst,'wb').write(d)
    c={};[c.__setitem__(x[0],c.get(x[0],0)+1) for x in log]
    print(dst,hashlib.md5(d).hexdigest(),c)
    for x in log:
        if x[0]!='OK': print(' ',x)
    if report: json.dump(log,open(report,'w'),ensure_ascii=False,indent=0)
if __name__=='__main__': run(*sys.argv[1:])
