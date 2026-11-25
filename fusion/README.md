# CAO modifiable · V5-stabilisation

Le montage à blanc à socle plat utilise le [F3D V5 Roulis de montage manuel](AURA-01_V5_Roulis_Montage_Manuel.f3d) et son [dossier de qualification](../docs/diagnostic/montage_manuel/README.md).

Le modèle éditable est [AURA-01.f3d](AURA-01.f3d). Le STEP issu des mêmes solides est dans la fabrication. Le dossier de preuves conserve les matrices Fusion, les maillages et l’état des liaisons. [Version](../VERSION.md) · [Inventaire des exports](../manufacturing/inventaire.json) · [Preuves](../docs/diagnostic/corrections/)

## Ordre des corrections sur une copie

La source de la reprise est le F3D de la V5 roulis v1 au tag **aura-01-v5-roulis-v1**, SHA-256 `55d3f7964cd04625a4f9062db03c406900fc6acf57cedec86a5bfd5b46495361`. L’importer dans un document Fusion neuf. Les scripts travaillent sur ses repères natifs et ses Base Features. Charger ces modules Python dans l’environnement Autodesk Fusion, où le paquet `adsk` existe. L’historique exact des retouches se trouve dans le F3D actif.

| Étape | Commandes et résultats |
|---|---|
| A | `stabiliser.run(context)` rigidifie J2R/J3R, fusionne les deux longerons et retire moteurs, tambours et gaines associés. |
| B | `interfaces.hollow_base(Model())` reprend les logements, le tube et les bagues. `interfaces.thumb(Model())` vérifie et intègre le sabot. `deposes.run(context, chemin_json)` dégage les couloirs. |
| C | `compensation.run(context)` installe les supports et gabarits. `routage.run(context)` dégage la montée du faisceau et place les trois boucles. |
| D | `butees.run(context, chemin_json)` reprend les lumières et quatre rehausses. `finitions.run(context, chemin_json)` détourne les capots et ajoute les peignes. |
| E | Écrire les données neutres avec `controle_cao.neutral_data(Model(), dossier_preuves)`. Appliquer `fin_routage.run(context, dossier_preuves)`, réécrire la géométrie neutre, puis appliquer `fin_routage.wrist_ends(Model(), dossier_preuves)` et relever à nouveau les données neutres. Exécuter `fin_routage.verify`. |
| E bis | Appliquer `support_service_j3.apply(Model())`. Tester `check` et `module_access`, et régénérer les données neutres. |
| F | `controle_cao.campaign` reçoit le générateur `unique_samples()` de la [campagne auditée](../docs/diagnostic/latest/scripts/campagne_fusion.py). `rejouer_limites.run` reprend les cibles refusées à l’aide des pignons et de plusieurs ordres de commande. |
| G | `livrer.step_and_f3d`, `livrer.coupons`, `livrer.visuals` et `livrer.samples_animation` produisent les exports et la preuve visuelle. Vérifier et actualiser les empreintes à toute réexécution. |

## Preuves de révision

La campagne finale, les contre-poses BRep, les déposes du module J3 et la réimportation documentent la version cloud 2. La première campagne et les reprises au solveur précèdent le support démontable. Les calculs utilisent les maillages de la version 2 et conservent les mêmes cibles. [Manifeste](../docs/architecture/revision.json) · [Campagne finale](../docs/diagnostic/corrections/campagne_finale.json) · [Rapport des corrections](../RAPPORT_CORRECTIONS.md)

Les ressorts et gaines dynamiques ont des gabarits natifs à leur forme de repos. Les volumes de service aux poses évaluées sont reconstruits temporairement à partir des points d’ancrage, des courses et des longueurs libres. La scène Blender reprend les matrices des solides mesurées dans Fusion.
