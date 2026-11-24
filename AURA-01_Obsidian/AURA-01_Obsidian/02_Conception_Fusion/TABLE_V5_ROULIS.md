# AURA-01 V5 — Roulis d’épaule et de coude

**24 novembre 2026 · Variante de revue enregistrée dans Fusion.** Source « AURA-01 V5 — Revue design » v2 validée visuellement par le porteur du projet. La reprise est partie d’une copie de l’archive contrôlée en phase 0. [Modèle Fusion F3D](../../../fusion/AURA-01.f3d) · [Liste d’achats](../../../purchases/NOMENCLATURE.md)

## Implantation et mouvements

| Axe Fusion | Mouvement | Course de revue | Entraînement |
|---|---|---:|---|
| J2R | Roulis autour de l’axe épaule–coude. Le bras entraîne l’avant-bras et la main. | ±20° | MG90S dans le socle, tambour ±60° |
| J3R | Roulis autour de l’axe coude–poignet. L’avant-bras entraîne la main. | ±24° | MG90S dans le socle, tambour ±72° |

Les axes de roulis suivent les deux axes longitudinaux locaux X. Ils s’insèrent après les pivots de tangage J2 et J3. Le modèle comprend six axes principaux et cinq commandes de doigts. Les carénages et la palette reprennent la V5 revue, avec un dégagement local dans le capot du bras. Un collier porte-arbre ajoute **8 mm** à chacun des deux entraxes, qui passent à **80 et 101 mm**.

Chaque collier comprend un arbre creux, deux portées dans un palier fendu et une butée. Deux brins opposés par axe relient le tambour du socle au collier. Le rapport des rayons de **4 et 12 mm** donne une réduction de **3:1**. Le modèle représente les gaines et les brins dans la pose neutre. Les points d’arrêt des gaines, leur réserve dans les mouvements combinés et la friction se vérifient au montage.

## Contrôles Fusion

- **154 occurrences, 31 pivots et 20 liens de mouvement.** Le F3D a été réimporté. Une commande d’épaule de 10° dans l’archive réouverte a entraîné le tambour de 30°.
- Les deux roulis ont atteint les quatre extrémités de course au solveur natif. À chaque essai, les autres axes de commande sont restés à 0°. Les cinq commandes indépendantes des doigts ont été retestées après reprise.
- **31 poses** de solides contrôlées, avec contrôle supplémentaire de quatre configurations après la dernière retouche. Le contrôle au noyau solide ne détecte aucun volume d’intersection structurelle supérieur à **0,03 mm³** sur cet échantillon. Les deux vis de butée filetées du socle gardent leur engagement prévu.
- Le calcul statique de la gravité sans objet saisi atteint **0,034 N·m** autour de J2R et **0,007 N·m** autour de J3R dans les poses échantillonnées. Il utilise les volumes CAO des pièces et des masses de gabarit. La traction, le jeu, le couple disponible et la température restent à vérifier au banc.
- La programmation sur table doit borner la descente combinée de J2 et J3. Les axes et les gains validés ici concernent la cinématique de la maquette.

## Achat et traçabilité

**13,10 €** de pièces supplémentaires aux quantités chiffrées, avant le port d’une commande séparée. **149,48 € TTC** pour le panier complet de mise au point avec cinq SG90 économiques pour les doigts, aux conditions de port du panier. Avec onze servos, l’addition des hypothèses de pointe donne 11,3 A. Les tests en charge et l’alimentation définitive restent à qualifier. [Pièces et prix](../../../purchases/NOMENCLATURE.md) · [[05_Electronique/README_MOTEURS_V3#AURA-01 V5 · Roulis épaule et coude|Moteurs]]

SHA-256 de l’archive revue `55d3f7964cd04625a4f9062db03c406900fc6acf57cedec86a5bfd5b46495361`. SHA-256 de l’archive source `d44b5dbafedf1d7ecbb4df91b2020320680f58dc70f29f906f79b77b0ccff923`.
