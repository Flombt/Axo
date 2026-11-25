# Version active · V5-stabilisation

**25 novembre 2026 · Dossier numérique de mise au point**

| Domaine | Référence active |
|---|---|
| CAO | **AURA-01 V5 · Stabilisation**, Fusion v2. ID `urn:adsk.wipprod:dm.lineage:eFBLfdyfT4-U_TPXc36Ulg`. 143 occurrences, 18 liens de mouvement et zéro référence externe. Archive F3D réimportée. [Modèle](fusion/AURA-01.f3d) · [Preuve](docs/diagnostic/corrections/fusion_sauvegarde.json) |
| Cinématique | Quatre axes de bras J1 ±88°, J2 ±21°, J3 ±32° et J7 ±30° en commande. Cinq voies de doigts 0–92°. Les deux liaisons longitudinales intermédiaires sont fixes. [Limites de commande](firmware/enveloppe.py) |
| Fabrication | STEP, 49 références de robot pour 62 pièces, cinq éprouvettes dédiées et plateaux de qualification PETG. [Paquet](manufacturing/README.md) |
| Commande | Pico 2, neuf PWM, capteurs de tangage à qualifier, rail externe, trois modules compilés et neuf essais hôte. [Firmware](firmware/README.md) · [Électronique](electronics/README.md) |
| Montage | Quatre rehausses de 90 mm, deux ressorts et roulements 6000-ZZ à éprouver sur support ancré. [Notice](assembly/README.md) |
| Budget | **150 € maximum**. Filament fourni à **0 €**. Scénario **188,74 € TTC provisionnés**, avant devis d’intégration. [Nomenclature](purchases/NOMENCLATURE.md) |

**SHA-256 du F3D**

`6b2daefa8f79067125ac4b9171f718c69cf002c466cc288441623480150a8709`

Les essais physiques, la retenue en charge et la distribution 5 V conditionnent la qualification. Le point de reprise V5 roulis v1 est conservé au tag `aura-01-v5-roulis-v1`. [Contexte](docs/architecture/PROJECT_CONTEXT.md) · [Corrections](RAPPORT_CORRECTIONS.md) · [Manifeste](docs/architecture/revision.json) · [Restauration](archives/README.md)
