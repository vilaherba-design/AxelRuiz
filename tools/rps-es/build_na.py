import json,sys
sys.path.insert(0,'.')
import dllpatch,inline
SHORT={
'controls known':'mandos leidos',
" ROCK's binding gives the game every button.":' El binding de ROCK da todos los botones.',
' is already set. Every action works.':' ya esta puesto. Todo funciona.',
". Your controllers keep SteamVR's binding.":'. Tus mandos usan el binding de SteamVR.',
'Inventory scan limit reached':'Limite de escaneo alcanzado',
'Category item limit reached':'Limite de la categoria',
'); controls apply to this session':'); controles para esta sesion',
'Numeric change was not queued; try again':'Cambio no aplicado; vuelve a intentarlo',
': console commands cannot contain %':': los comandos no pueden llevar %',
'ROCK configuration is not ready':'Config de ROCK todavia no lista',
'No item selected':'Ningun objeto',
'Player unavailable; nothing added':'Jugador no disponible; no anadido',
'boolean values must be true or false':'los valores deben ser true o false',
}
DROP={'Seconds','Multiplier','Scale','Degrees','Intensity','Strength'}
for f,src,dst in [('tr_rock','ROCK.dll','ROCK_es.dll'),('tr_paper','PAPER.dll','PAPER_es.dll'),('tr_climb','ROCK_Wall_Climbing.dll','Climb_es.dll'),('tr_palm','wheelmenu.dll','PALM_es.dll'),('tr_rpsui','RPS_UI_Framework.dll','RPS_UI_es.dll')]:
    T=json.load(open(f+'_na.json',encoding='utf-8'))
    if f=='tr_rpsui':
        for k in DROP: T.pop(k,None)
    for k,v in SHORT.items():
        if k in T: T[k]=v
    T={k:v.rstrip(' ') if not k.endswith(' ') else v for k,v in T.items()}
    fix=inline.inline_strings(src,f+'_na.json')
    for en in fix:
        es=T[en].rstrip(' ') if not en.endswith(' ') else T[en]
        assert len(es.encode())<=len(en.encode()),(src,en,es)
        T[en]=es+' '*(len(en.encode())-len(es.encode()))
    assert all(ord(c)<128 for v in T.values() for c in v)
    json.dump(T,open(f+'_na.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
    print(src,'fijos',len(fix))
    dllpatch.run(src,f+'_na.json',dst,'r_'+dst+'.json')
