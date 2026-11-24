# AURA-007 — Bras V3 de table à trois moteurs

Cette maquette de présentation précède la [[02_Conception_Fusion/MAIN_POIGNET_ECO|version de table à main et poignet articulés]], qui constitue la priorité actuelle.

**Premier objectif** — Appuyer sur un bouton, voir le bras faire un geste lent, puis le voir revenir à sa pose de repos. Le programme tourne sur l’Arduino dès qu’il est alimenté.

## Maquette de présentation r01

Version 1 enregistrée dans le projet **Robotic Arm — V1** et laissée ouverte dans Fusion. [Document Fusion](https://epitech619.autodesk360.com/g/projects/202611211172950976/data/dXJuOmFkc2sud2lwcHJvZDpmcy5mb2xkZXI6Y28uS0w2NDZueTlSV3VLYXF5Z2ZkN196UQ/dXJuOmFkc2sud2lwcHJvZDpkbS5saW5lYWdlOlhxMVQ3NXBHUUk2eUNOWFJSZUpxQmc) · [Archive F3D rouverte](../../../archives/aura-007/fusion/AURA-01_V3_de_table_r01.f3d) · [Fiche de présentation et plateaux](../../../archives/aura-007/fusion/Fiche_presentation.md).

- Trois segments de 47, 44 et 40 mm. Platine de 126 × 100 mm, neuf pièces FDM, capots démontables, main monobloc à cinq doigts avec phalanges dessinées. Les deux raccords fixes ont une languette guidée et une vis transversale provisoire M3.
- Trois MG90S représentés dans leurs logements. L’épaule et le coude ont un axe passif coaxial côté opposé au palonnier. Entraxe modélisé des pattes du MG90S de 27,9 mm et jeu de boîtier de 0,35 mm par côté. Contrôler ces valeurs et la visserie du palonnier sur la pièce reçue. Prévoir de dégager les cosses du bouton sous la platine avec des entretoises aux quatre fixations.
- Les trois liaisons Fusion ont été pilotées séparément. 62 poses échantillonnées avec les pièces et les enveloppes matériel, seuil volumique 0,006 mm³. Pas d’interférence détectée sur ces poses. [Vérification et limites](../../../archives/aura-007/fusion/Verification_Fusion.json).
- Neuf STL fermés et trois 3MF tranchés dans PrusaSlicer. Profil virtuel PETG, buse 0,4 mm, couche 0,20 mm. 161,28 g estimés avec supports, environ 16 h 25. [Relevé](../../../archives/aura-007/fusion/Verification_Tranchage.json).
- Estimation statique maximale sur les poses vérifiées de 0,0552 N·m pour l’épaule et 0,0327 N·m pour le coude, à vide, avec volumes PETG pleins et 6 g de câblage et de vis au poignet. Mesurer le couple utile et le comportement à la coupure après montage.

## Design et mouvements

- Reprendre la [[02_Conception_Fusion/DESIGN_V3|silhouette V3]] avec trois segments, les capots, le poignet et la main blanche à cinq doigts. La main et le poignet sont fixes sur ce prototype. Garder l’articulation visuelle du troisième segment en position fixe.
- Motoriser **J1 au socle, J2 à l’épaule et J3 au premier coude**. Prévoir une base stable et des pivots supportés des deux côtés pour limiter l’effort sur les sorties de servo. Fixations directes sur palonniers d’origine et capots démontables.
- Dessiner une copie de table plus légère. Prendre **120 à 140 mm entre l’épaule et le poignet** comme point de départ, puis ajuster d’après les masses imprimées et les encombrements. La V3 à taille actuelle demande environ **4,76 N·m** à l’épaule à l’horizontale d’après son calcul initial. Le MG90S est donné pour **0,18 N·m au blocage à 4,8 V**. Mesurer le couple utile continu sur la copie légère. [Fiche TowerPro](https://towerpro.com.tw/product/mg90s-3/)

## Commande et premier essai

- Un Arduino Nano Every et un bouton. Les trois servos sont alimentés par un bloc secteur 5 V séparé du port USB de la carte, avec masse commune côté basse tension. Calibrer d’abord les limites de chaque servo seul.
- Premier geste sans charge utile. Tourner un peu le socle, lever l’épaule, plier le coude, marquer une pause, revenir au repos. Lancer un cycle par appui et limiter la vitesse par interpolation.
- Vérifier dans Fusion les empreintes et les interférences des poses de départ et de transition. Puis essayer l’épaule avec une charge représentative de la copie et mesurer courant, chauffe et tenue. Confirmer la stabilité, le comportement à la coupure et dix cycles reproductibles sur le prototype assemblé.

[Liste d’achat et budget](../../../archives/v2/README_V2_ELEMENTS_A_ACHETER.md) · [[09_Gestion/TACHES#AURA-007 — Réaliser le bras V3 de table|Suivi]].
