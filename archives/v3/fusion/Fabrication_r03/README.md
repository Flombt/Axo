# AURA-01 V3 r03 — Impression et montage à blanc

La structure se compose de **23 pièces imprimées** à partir de **11 modèles**. Le socle, la tourelle, chacun des trois segments, les deux éléments du poignet et la paume s’impriment chacun d’un bloc. Les trois formes de phalange sont répétées cinq fois. Les vis, axes, rondelles, paliers, servos et palonniers sont des pièces de quincaillerie et de motorisation.

## Quoi imprimer

Les projets 3MF de `Plateaux_PrusaSlicer/` incluent les placements, les orientations et un profil comparatif PETG. Les STL unitaires de `STL_orientes/` sont en millimètres avec leur face d’impression à plat. La pièce la plus large est le socle de 186 × 176 mm. La tourelle atteint 85 mm de haut.

| Projet 3MF | Pièces | Supports générés | PETG estimé | Temps estimé |
|---|---:|---|---:|---:|
| `01_Socle` | 1 | Non | 244,60 g | 23 h 32 min |
| `02_Trois_segments` | 3 | Segment distal | 349,40 g | 28 h 24 min |
| `03_Tourelle_et_poignet` | 3 | Non | 140,56 g | 13 h 01 min |
| `04_Paume` | 1 | Non | 106,17 g | 9 h 31 min |
| `05_Phalanges_proximales_et_moyennes` | 10 | Non | 115,97 g | 12 h 46 min |
| `06_Bouts_de_doigts` | 5 | Non | 45,09 g | 5 h 08 min |

PrusaSlicer 2.9.6 a retranché les six 3MF après réouverture sur une machine virtuelle de 220 × 220 × 250 mm. Le profil utilise une buse de 0,4 mm, des couches de 0,20 mm, cinq périmètres, 25 % de remplissage gyroïde et une bordure de 3 mm. Le total est d’environ **1 002 g et 92 h 22 min** avec ce profil. Le segment distal se pose sur le flanc. Son tranchage unitaire utilise environ 0,6 g de support, dans les premiers 2,2 mm au-dessus du plateau. Conserver les supports de ce segment à la réouverture du projet.

Sélectionner le profil de l’imprimante et du PETG réels avant un lancement. Pour une première vérification, charger un STL de chaque phalange et tester un seul doigt avant de lancer une série. [Guide Prusa sur les jeux et les orientations](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135)

## Montage à blanc

1. **Doigt** — Monter un KST X06 V6.0 par le dessous de la phalange, sortie engagée dans sa rainure. Les deux pattes, espacées de 24 mm, sont accessibles par les passages latéraux. Vérifier le centrage et choisir les vis M2 après mesure de l’épaisseur traversée et de la prise utile.
2. **Articulations des doigts** — Assembler de la phalange proximale à la distale. Le palonnier du côté moteur et l’axe passif opposé s’alignent sur le même pivot. Les joues laissent nominalement 0,80 mm par côté autour du corps imprimé. Contrôler les alésages nominaux de 3,40 mm pour l’axe passif de 3 mm. Garder une boucle de câble mobile, hors du passage des deux joues.
3. **Paume et poignet** — Monter les doigts à la paume, puis présenter le pivot de roulis sur l’élément de flexion. Vérifier que la paume passe entre les éléments voisins en déviation, flexion et roulis.
4. **Bras et socle** — Présenter les segments et la tourelle sur leurs axes métalliques. Contrôler la liberté de rotation après serrage et le maintien axial. Les quatre passages Ø6,9 mm permettent l’ancrage sur un support rigide. Les fixations définitives des servos du bras, les transmissions, les paliers et la retenue à la coupure restent à qualifier.

## Contrôles de la révision

- Fusion a rouvert l’archive r03 et retrouvé les 23 occurrences et les 22 pivots. Les 165 poses testées, dont des flexions isolées, la fermeture des cinq doigts et des gestes coordonnés, sont sans intersection volumique détectée entre les solides imprimés et les enveloppes moteur présentes.
- L’audit de la r02 a retrouvé 13 paires de corps en collision au repos entre composants, notamment épaule/longeron, segment distal/poignet et paume/pouce. Les 22 poses comparées présentaient au moins une interférence dans la r02. Les relevés sont dans `Verification_FDM_r03.json`.
- Les onze maillages sont fermés, en un seul tenant et à l’échelle du modèle. Le tranchage est numérique. Le montage, le passage des fils, la résistance des impressions et le comportement en charge restent à éprouver.
