# AURA-01 V5 — Revue design

**24 novembre 2026 · En attente de validation visuelle.** Variante Fusion « AURA-01 V5 — Revue design » dérivée de « AURA-01 r05 — Budget Edition » v2. La phase 0 a contrôlé les 105 occurrences de l’archive source et sa copie de sauvegarde locale. L’archive de revue a été rouverte dans Fusion. [Modèle F3D](../../../archives/v5-revue/fusion/AURA-01_V5_Revue_Design.f3d) · [Liste d’achats](../../../archives/v5-revue/ACHATS.md)

## Forme et implantation

- Socle à pivot sur deux 608 et paume à quinze phalanges issus de la V5. Carénages galbés, garde du coude plus basse et servo du coude aligné dans le longeron. Le module des dentures d’épaule et de coude passe de 1 à 0,8. Les rapports restent de 3:1 et 2:1.
- Cinq SG90 et cinq bobines à gorge unique en rangées de trois et deux. La cassette fait **45,8 mm** de large contre **76,4 mm** en r05. La coque d’avant-bras mesure **50,6 mm** de large. Pour loger les deux rangées et le roulis, les entraxes épaule–coude et coude–poignet sont de **72 et 93 mm**.
- Roulis J7 avec un SG90 couché et un palier coaxial. Le faisceau électrique et les cinq brins de traction passent sous carénages avec des sorties courtes. Les formes de câbles représentent le routage au neutre. Leur déformation, le rayon de courbure et le réglage des tensions relèvent du montage à blanc.
- Dans Fusion, masquer la coque supérieure, le capot inférieur et la joue arrière de l’avant-bras pour examiner les cinq bobines. La pose d’ouverture met en valeur l’épaule et le poignet. Les angles ci-dessous sont exprimés par rapport à la pose neutre de calcul.

## Contrôles Fusion

- **116 occurrences, 27 liaisons pivot et 18 liens de mouvement.** Un essai natif à 75° sur chacune des cinq bobines a fléchi les trois phalanges correspondantes. Les angles des douze autres phalanges sont restés à 0°.
- Quatorze poses contrôlées au noyau solide, dont le neutre, les deux extrémités de chaque axe, quatre poses composées et une flexion simultanée des doigts. Aucune intersection structurale supérieure à 0,03 mm³ dans cet échantillon. Le contrôle final de la quincaillerie au neutre retrouve les deux engagements filetés prévus des butées J1.
- Courses CAO relatives à la pose neutre de **±88° en lacet, ±21° à l’épaule, ±32° au coude et ±32° en roulis**. Les butées basses de l’épaule et du coude atteintes ensemble placent la main à **−59,1 mm** par rapport au plan de pose de la platine dans le cas testé. La commande de table devra tenir compte de la combinaison J2/J3.

Positions de contrôle avec roulis à −32°, 0° et +32° et cinq doigts à 0, 46 ou 92° de commande de bobine.

| J2 relatif | J3 relatif | Point bas de la main observé |
|---:|---:|---:|
| −21° | +1° | +9,4 mm |
| −14° | −9° | +11,0 mm |
| −7° | −18° | +14,8 mm |
| 0° | −32° | +5,8 mm |

Le calcul couvre ces poses. La tenue sous charge, le frottement des paliers, les câbles et la limite continue au-dessus de la table seront à mesurer sur prototype après validation du design.

## Achat et traçabilité

Panier cible **148,98 € TTC** livré selon les hypothèses de port, hors impression. Neuf servos de position. Le rail moteur prévu est de 5 V / 10 A avec mesure du courant du lot avant essais sous charge. [[05_Electronique/README_MOTEURS_V3#AURA-01 V5 · Revue design|Implantation des moteurs]] · [Prix et visserie](../../../archives/v5-revue/ACHATS.md)

SHA-256 de l’archive revue `d44b5dbafedf1d7ecbb4df91b2020320680f58dc70f29f906f79b77b0ccff923`. SHA-256 de l’archive r05 utilisée `52577a58dd3bef691e3a3afa414f1e7c608a2f1b84afc44ca2b98914a6c21fd8`.
