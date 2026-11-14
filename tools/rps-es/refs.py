import pefile,struct,sys,capstone,re
pe=pefile.PE(sys.argv[1]); data=pe.__data__
base=pe.OPTIONAL_HEADER.ImageBase
text=[s for s in pe.sections if s.Name.startswith(b'.text')][0]
t0=text.PointerToRawData; tr=text.VirtualAddress; tb=data[t0:t0+text.SizeOfRawData]
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
def off2rva(o): return pe.get_rva_from_offset(o)
def refs(off):
    rva=off2rva(off); out=[]
    # rip-rel: disp at i, insn end = i+4(+imm)
    for i in range(len(tb)-4):
        disp=struct.unpack_from('<i',tb,i)[0]
        if tr+i+4+disp==rva: out.append(('rip',i))
    va=base+rva
    for m in re.finditer(re.escape(struct.pack('<Q',va)),data): out.append(('abs',m.start()))
    return out
def ctx(i):
    s=max(0,i-8)
    for ins in md.disasm(bytes(tb[s:s+60]),base+tr+s):
        pass
if __name__=='__main__':
    for o in sys.argv[2:]:
        o=int(o,16); r=refs(o); print(hex(o),r[:5])
        for kind,i in r[:3]:
            if kind=='rip':
                s=i-3
                for k in range(s-2,s+1):
                    insns=list(md.disasm(bytes(tb[k:k+64]),base+tr+k))
                    if insns and insns[0].size==(i+4-k): break
                for ins in insns[:7]: print('   ',hex(ins.address),ins.mnemonic,ins.op_str)
