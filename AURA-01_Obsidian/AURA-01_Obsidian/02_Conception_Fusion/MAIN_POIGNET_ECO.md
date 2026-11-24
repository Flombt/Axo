# AURA-008 — Main et poignet articulés à budget réduit

**Priorité active.** Garder les trois segments V3 et remettre en service les quinze phalanges et le roulis du poignet. La r01 reprend la platine, les longueurs 47/44/40 mm et les interfaces du bras de table. La paume, ses doigts et les interfaces d’épaule et de poignet ont été remodélisés pour la nouvelle motorisation.

[Document Fusion v2](https://epitech619.autodesk360.com/g/projects/202611211172950976/data/dXJuOmFkc2sud2lwcHJvZDpmcy5mb2xkZXI6Y28uS0w2NDZueTlSV3VLYXF5Z2ZkN196UQ/dXJuOmFkc2sud2lwcHJvZDpkbS5saW5lYWdlOm8wU21DcFFwVF9pQ3lrSGdWeThxR0E) · [Archive F3D](../../../archives/aura-008/fusion/AURA-01_V3_Main_Poignet_r01.f3d) · [Fiche avec vidéo et plateaux](../../../archives/aura-008/fusion/Fiche_presentation.md) · [Budget et achats](../../../archives/v2/README_V2_ELEMENTS_A_ACHETER.md).

## Implantation

| Repère | Fonction et choix d’essai |
|---|---|
| J1 | Orientation manuelle du socle autour d’un axe M4, avec retenue par rondelles et écrou. |
| J2 | Épaule sur un TowerPro MG996R, avec appui passif coaxial et deux pattes à quatre perçages. L’entraxe longitudinal modélisé est de 48,7 mm. Vérifier les pattes et le palonnier reçus. |
| J3 | Coude sur un TowerPro MG90S, avec axe passif opposé au servo. Le troisième segment conserve son raccord fixe. |
| J7 | Roulis du poignet sur un MG90S, ±36° échantillonnés. Le palonnier monte dans la bague de la paume, qui prend appui radial dans le dernier segment. Ouverture centrale pour le tournevis. Prévoir une boucle souple extérieure pour les trois fils du servo de main. |
| T1 et T2 | Un MG90S entraîne le tambour, qui tire la traverse des cinq tendons. Rayon de gorge nominal 6 mm, 72° d’enroulement, soit ≈7,5 mm de course. La traverse s’insère par l’avant des rails, avec deux vis de butée. |
| Quinze phalanges | Cinq doigts de trois phalanges. Axes acier Ø2 mm dans des passages CAO Ø2,18 mm, six géométries d’impression répétées. Tendons côté paume, rappels élastiques sur le dos de la main. Prévoir une longueur réglable et un peu de compliance sur chaque fil, notamment le pouce. |

Alimentation 5 V pour les quatre servos, branches courtes et masse commune avec le Nano compatible 5 V. La logique peut être alimentée par son port USB d’atelier. Mesurer les chutes transitoires avant le mouvement combiné. Le cycle au bouton reste à programmer et à calibrer.

## Contrôles du 22 novembre 2026

- Fusion a rouvert l’archive avec 39 occurrences, 20 pivots, une translation et 16 couplages de mouvement. Le tambour a effectivement entraîné les quinze pivots et la traverse. Le modèle pose l’armature avant le réglage de la fermeture, en raison d’un verrouillage du solveur observé lorsque le roulis était piloté à la volée avec la prise fermée.
- 72 poses échantillonnées avec les enveloppes moteurs, axes et contours des pièces. Aucune interférence volumique détectée au seuil de 0,006 mm³. Le calcul statique à vide avec PETG plein et 10 g de câblage/vis à la paume donne **0,1204 N·m à J2** et **0,0829 N·m à J3**. Le couple constructeur est un repère de blocage. À J3, mesurer la tenue et la chauffe avant les cycles longs. [Relevé Fusion](../../../archives/aura-008/fusion/Verification_Fusion.json).
- 17 STL fermés et connectés, 26 pièces sur trois 3MF tranchés. PETG, buse 0,4 mm, couches 0,20 mm. 196,11 g estimés, supports compris, et environ 21 h 12. Les passes de rappel de la paume débouchent des deux côtés. [Relevé PrusaSlicer](../../../archives/aura-008/fusion/Verification_Tranchage.json).

## Premier montage

Imprimer un index et tester trois axes Ø2 mm. Ébavurer les guides, faire passer un tendon de 0,40 mm et un élastique de rappel, puis vérifier la réouverture. Contrôler la rotation libre du poignet et la boucle de câbles à ±36°. Mesurer le courant et la tenue du coude en appui avant de lancer le geste à vide. Les rapports concernent la CAO et le tranchage. La prise d’objet et la durée de vie restent à qualifier.
