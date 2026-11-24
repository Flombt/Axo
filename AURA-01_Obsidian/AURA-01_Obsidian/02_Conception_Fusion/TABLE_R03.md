# AURA-009 · V3 de table r03

**État au 23 novembre 2026.** Conception enregistrée dans Autodesk Fusion sous **AURA-01 — V3 de table — AURA-009 r03**, version v2. La [[02_Conception_Fusion/MONTAGE_V3|r02]] sert de référence. L’onglet récupéré r02 a fait l’objet d’une archive locale préalable.

## Architecture

- J1 indexable avec quatre ancrages M5 et une interface d’entraînement réservée. J2 MG996R traversant et J3 XC330-M288-T sur deux arbres portés Ø5. Retenues et butées indépendantes des commandes.
- Poignet J7 en cassette avec arbre Ø10 et deux roulements. Main à cinq doigts, quinze pivots, ligaments renforcés et cinq réglages tendon-ressort.
- Quatre guides articulés natifs, huit attaches et six colliers. Les 25 raccords restent alignés dans les 59 poses échantillonnées. Nano et interface TTL sur platine fixe. [[05_Electronique/README_MOTEURS_V3|Moteurs, bus et alimentation]].

## Preuves

59 poses globales et 72 poses ciblées du pouce, six corridors et 149 positions de démontage. Avec 20 g, le modèle de masse plein sans lest donne jusqu’à 0,234 N·m à J2 et 0,154 N·m à J3. Le maintien hors tension, la résistance du PETG, le courant et la commande restent à qualifier.

- [Archive Fusion r03](../../../archives/r03/fusion/AURA-009_Table_r03.f3d) · [STEP](../../../archives/r03/fusion/AURA-009_Table_r03.step) · [Réimport et sauvegarde](../../../archives/r03/fusion/Verification_Sauvegarde_r03.json)
- [Rapport r03](../../../archives/r03/RAPPORT_AMELIORATIONS_R03.md) · [Audit r02](../../../archives/r02/DIAGNOSTIC_ROBOT.md) · [Coupes et inspection de tous les angles](../../../archives/r03/wireframes/08_controle_tous_les_angles.png)
- [Notice de montage](../../../archives/r03/ASSEMBLAGE.md) · [Nomenclature](../../../archives/r03/fusion/Nomenclature_r03.csv) · [Plateaux PETG](../../../archives/r03/fusion/Plateaux_PrusaSlicer)
- [[09_Gestion/TACHES#AURA-009 de table r03 — Reconcevoir et qualifier le kit|Suivi des essais]] · [[09_Gestion/ADR#AURA-009 de table r03 — Articulations portées et banc ancré|Décision d’architecture]]

[Publication de la r03 sur GitHub](https://github.com/Flombt/bras-robotique/commit/ec2abbde9c5103ec50d0bb93d371c3885fdda637).

## Démonstration cinématique

Le film du 24 novembre 2026 reprend cette révision et son faisceau. [[04_Animation_Emotion/ANIMATIONS#AURA-009 r03 v2 — Démonstration cinématique|Démonstration r03 v2]] · [Rapport cinématique](../../../archives/r03/animations/RAPPORT_CINEMATIQUE.md) · [Film, extraits et projet Blender sur GitHub](https://github.com/Flombt/Axo/releases/tag/aura-009-r03-v2-cinematique).

## Archives

[Sauvegarde de l’onglet r02 récupéré](../../../archives/r02/reprise-fusion/AURA-009_Table_r02_recuperee_2026-11-23.f3d). Empreinte SHA-256 c54555e81389761f1c933c1d4709a241b1a440ab593edf91a66e290e9270420e.
