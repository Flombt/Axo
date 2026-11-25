"""Rejoue les cibles distinctes après un ajout de pièces solidaires."""
import json
from pathlib import Path

from controle_cao import COMMANDS, DRIVEN, case, write
from interfaces import bounding
from stabiliser import Model


def run(_context,folder):
    m=Model()
    m.require_copy()
    out=Path(folder)
    cases=json.loads((out/"campagne_fusion.json").read_text(encoding="utf-8"))
    neutral=json.loads((out/"geometrie_neutre.json").read_text(encoding="utf-8"))
    existing=json.loads((out/"poses_reperes.json").read_text(encoding="utf-8"))
    confirmed=[]
    for row in existing:
        confirmed.append(case(m,neutral,row["label"],row["target"],True,True))
    write(out/"poses_reperes.json",confirmed)

    accepted={}
    results=[]
    try:
        for old in cases:
            q=old["target"]
            key=tuple(q.items())
            if key not in accepted:
                m.pose({})
                actual=m.pose(q)
                error=max(abs(actual[k]-v) for k,v in q.items())
                if error>.02 and old["error_deg"]<=.02:
                    for i in range(1,9):
                        actual=m.pose({k:round(value*i/8,1) for k,value in q.items()})
                    error=max(abs(actual[k]-v) for k,v in q.items())
                proof=dict(actual={k:round(actual[k],5) for k in (*COMMANDS,*DRIVEN)},error_deg=round(error,6))
                if error<=.02:
                    fingers=("11_Paume",*(k+str(n) for k in "PIMAU" for n in (1,2,3)))
                    proof["hand_z_mm"]=min(bounding(b)[0][2] for k in fingers for b in m.solids(k))
                accepted[key]=proof
            results.append(dict(source_case=old["source_case"],label=old["label"],target=q,
                                **accepted[key]))
            if len(results)%25==0:
                write(out/"campagne_finale.json",results)
    finally:
        m.pose({})
    write(out/"campagne_finale.json",results)
    print(json.dumps({"identifiants":len(results),"poses_distinctes":len(accepted),
                      "confirme":sum("hand_z_mm" in r for r in results)}))
