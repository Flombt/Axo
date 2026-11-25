"""Rend démontables les appuis extérieurs du longeron J2 pour l’accès au MG996R J3."""
import json
from pathlib import Path

from compensation import segment
from controle_cao import write
from fin_routage import largest
from finitions import relief
from interfaces import ACCESS, collision, motor_access
from stabiliser import Model, boolean, box, cut, cylinder, get_attr, put_attr

OWNER="J2_Chape_Tangage"
REF="Support_Service_J3"
COUPE_Y=31.0
ATTACH=((37.0,131.0),(59.0,135.0))


def volume_in_world(model,key):
    part=model.copy(key)
    assert model.tmp.transform(part,model.occ[key].transform2)
    return part


def apply(model):
    if get_attr(model.root,"SupportService"):
        raise RuntimeError("Support démontable déjà présent")
    assert max(abs(model.angle(k)) for k in ("J1","J2","J3","J7"))<.02
    source=volume_in_world(model,OWNER)
    main=model.tmp.copy(source)
    side=model.tmp.copy(source)
    cut(main,box((49,(COUPE_Y+81)/2,117),(200,81-COUPE_Y,140)))
    cut(side,box((49,(-70+COUPE_Y)/2,117),(200,COUPE_Y+70,140)))
    brace=segment(model,(37,35,131),(59,35,135),3.4)
    boolean(side,brace)
    for x,z in ATTACH:
        l,h=10.5,7.8
        boolean(main,box((x,COUPE_Y-l/2,z),(15.6,l,12.4)))
        boolean(side,box((x,COUPE_Y+h/2,z),(15.6,h,12.4)))
        for index,u in enumerate((-4.2,4.2)):
            shaft=cylinder((x+u,COUPE_Y-l-1.5,z),(x+u,COUPE_Y+h+2,z),2.17)
            cut(main,shaft)
            cut(side,shaft)
    if side.lumps.count!=1:
        raise RuntimeError(f"Le support de service reste disjoint ({side.lumps.count}).")
    inverse=model.occ[OWNER].transform2.copy()
    assert inverse.invert() and model.tmp.transform(main,inverse)
    model.replace(OWNER,largest(model,main))
    component=model.place(REF,"Support démontable de compensation et de guidage · J3",OWNER,side,REF)
    put_attr(component.component,"Montage","Quatre M4 traversantes, accès extérieur")
    for i,(x,z) in enumerate(ATTACH,1):
        for j,u in enumerate((-4.2,4.2),1):
            screw=cylinder((x+u,18.5,z),(x+u,38.8,z),1.95)
            boolean(screw,cylinder((x+u,38.7,z),(x+u,41.7,z),3.35))
            model.place(f"Vis_Service_J3_{i}_{j}","Vis M4 du support de service",REF,screw)
    # Le carénage reste sur son ancien repère. Le chanfrein libère la
    # surface d’appui de la platine et l’accès aux écrous avant repose.
    finish_bolts(model)
    for key in (OWNER,REF):
        relief(model,"Coque_Bras",key)
    put_attr(model.root,"SupportService",{"coupe_y_mm":COUPE_Y,"vis":"4 M4 traversantes",
                                         "module":REF,"avant_depose":"retirer les deux ressorts et débrider le faisceau"})


def check(model,path):
    skip=ACCESS["Moteur_J3"][2]
    skip.update({REF,"Friction_J3_2","Ressort_J2","Ressort_J3","Boucle_J2","Boucle_J3",
                "Tige_Ressort_J3","Axe_Haut_Ressort_J3","Axe_Ressort_J2"})
    skip.update(k for k in model.occ if k.startswith("Vis_Service_J3_"))
    result=motor_access(model,"Moteur_J3")
    write(Path(path),result)
    print(json.dumps({"blocked":[[key,len(value)] for key,value in result["blocks"].items()],
                      "removed":result["removed"],"translations":61}))
    return result


def finish_bolts(model):
    for part in (OWNER,REF):
        base=volume_in_world(model,part)
        for x,z in ATTACH:
            for u in (-4.2,4.2):
                if part==OWNER:
                    cut(base,cylinder((x+u,15.5,z),(x+u,COUPE_Y+1.0,z),2.17))
                else:
                    cut(base,cylinder((x+u,38.62,z),(x+u,66,z),3.83))
        inv=model.occ[part].transform2.copy()
        assert inv.invert() and model.tmp.transform(base,inv)
        model.replace(part,largest(model,base))


def module_access(model,path):
    removed={"Coque_Bras","Ressort_J2","Ressort_J3","Boucle_J2","Boucle_J3",
             "Axe_Ressort_J2","Tige_Ressort_J3","Axe_Haut_Ressort_J3"}
    removed.update(k for k in model.occ if k.startswith("Vis_Service_J3"))
    ACCESS[REF]=(OWNER,(0,1,0),removed)
    module=motor_access(model,REF)
    hand=[]
    for i,(x,z) in enumerate(ATTACH,1):
        for j,u in enumerate((-4.2,4.2),1):
            name=f"Vis_Service_J3_{i}_{j}"
            tool=cylinder((x+u,41.71,z),(x+u,73,z),2.65)
            hits=[(key,round(v,5)) for key in model.occ if key not in removed|{name}
                  and not get_attr(model.occ[key].component,"Souple")
                  for body in model.solids(key) if (v:=collision(model,tool,body))>.03]
            hand.append({"screw":name,"tool_dia_mm":5.3,"overlap_mm3":hits})
    write(Path(path),{"path":module,"tools":hand})
    print(json.dumps({"module_blocks":list(module["blocks"]),"tool_conflicts":[a for a in hand if a["overlap_mm3"]]}))
