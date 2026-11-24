# Impression FDM et protocole d'assemblage

Références dans le cahier des charges aux [[README#18 — Impression 3D : stratégie de fabrication FDM|sections FDM et tolérances]] (18 et 19) et aux [[README#13 — Fiches de conception par pièce : catalogue initial|fiches P-001 à P-032]]. Reporter les résultats dans la [[08_Tests/MATRICE_TESTS|matrice de validation]] et les corrections dans la [[02_Conception_Fusion/CONCEPTION_MECANIQUE|conception mécanique]].

## Avant toute impression

- Connaître la machine, le volume utile, la buse et les profils matériaux.
- Faire un coupon de tolérance et un coupon d'insert.
- Contrôler orientation des couches, supports, dimensions et accès aux outils.
- Préférer 3MF si pertinent ; vérifier explicitement les unités d'un STL.
- Mesurer les pièces et reporter les corrections dans Fusion.

## Enregistrements d'essais

| Pièce | Révision | Matière | Profil | Jeu mesuré | Verdict |
|---|---|---|---|---|---|
| À compléter | — | — | — | — | Non testé |

## AURA-004 — Fabrication préparée

### Tranchage virtuel

PrusaSlicer 2.9.6 a importé et tranché les 21 maillages de référence V2 sur un plateau virtuel de 220 × 220 × 250 mm. Chaque fichier a été orienté, centré et posé sur le plateau dans le slicer. Les statistiques incluent les supports et bordures générés. Le CSV garde les rotations, la quantité, la longueur de filament, la masse et le temps estimé pour chaque fichier. Le profil et le relevé se trouvent dans `Exports_Fusion/AURA-004_Fabrication`, depuis la racine Aura.

| Famille | Orientation d’essai | Supports et points à regarder dans l’aperçu |
|---|---|---|
| Socle, couronne | Face inférieure sur le plateau | Sous le gradin de bride et au fond des avant-trous. Préserver la planéité de la portée. |
| Épaule | Face du disque à plat | Sous le logement du socle et dans les passages horizontaux des oreilles. Contrôler l’accès de retrait. |
| Bras supérieur et avant-bras | Sur un flanc, axe des pivots vertical | Sous les ajours du squelette et au débouché des rainures de manchon. Conserver les couches dans la longueur. |
| Chape J4 et support basculant | Chape sur le flanc, support avec la portée J5 verticale | Sous les oreilles, les dégagements de vis et le logement transversal. Vérifier la matière résiduelle autour du manchon. |
| Berceau G1, deux mors | Berceau sur sa semelle. Mors sur leurs flancs. | Sous les rebords et dans les passages horizontaux des guides. Les retirer sans ovaliser un alésage. |
| Garnitures courtes | Grande face à plat | TPU candidat. Vérifier bavures, vissage, compression et adhérence. |
| Coques et quatre contre-appuis | Coques ouvertes vers le plateau. Contre-appuis à plat. | Examiner la voûte des coques, les douilles et les fenêtres d’accès. La surface visible et les lamages doivent rester utilisables. |
| Rotor J5, deux demi-colliers, quatre tubes et quatre rondelles d’ajustage | Pièces tranchées pour préparer des gabarits. Portées verticales ou faces de séparation à plat. | Préférer un matériau usiné ou une pièce standard adaptée pour le service. Vérifier les ajustements dans les logements réels. |
| Cassettes J4/G1 et pièces nouvellement modifiées | Orienter la portée ou les passages critiques verticalement, avec reprise des efforts dans le plan des couches. | Vérifier les fenêtres, les vis M2 et l’accès lorsqu’un moteur est déposé. Supports moteur J1–J3 et bride J5 prévus en aluminium pour le service. |

Le profil comparatif emploie une buse virtuelle de 0,4 mm, des couches à 0,20 mm, quatre périmètres, cinq couches haut/bas, un remplissage gyroïde de 30 %, des supports automatiques et une bordure de 3 mm. PETG provisoire à 245 °C et plateau 85 °C puis 80 °C. TPU des garnitures à 225 °C et 55 °C, remplissage rectiligne plein et débit volontairement réduit. Appliquer la fiche du filament réel et contrôler le débit. La plaque de 260 × 220 × 8 mm et les arbres clavetés sont des pièces métal.

Référence V2 avec les quantités d’assemblage et les pièces métalliques simulées en plastique pour comparaison. Le slicer estime **188,79 g pour 61,82 m** de filament au total. Les pièces candidates polymères seules donnent **173,34 g pour 56,76 m** avec ce profil. Garder 15 % de provision pour coupons, réglage et supports supplémentaires. Les réserves concernent le calcul matière. La masse de la CAO en service tient compte séparément des métaux et des moteurs.

### Nomenclature de la branche AURA-004

Les dix 3MF de `Pieces_AURA004` ont été tranchés. Substituer les sept références révisées aux pièces homologues de la V2 et ajouter le pont J1 et les deux cassettes. Les fenêtres latérales des cassettes donnent accès aux vis et aux supports. Le fichier `Nomenclature_FDM_AURA004.csv` indique la source, la quantité et l’orientation de chaque référence. Le scénario polymère couvre **18 références et 21 pièces**, pour **193,58 g et 63,38 m**. Les cinq coupons tranchés ajoutent **66,00 g et 21,61 m**. La provision totale est d’environ **300 g** avec 15 % de marge.

### Coupons et montage à blanc

Les cinq 3MF du dossier `Coupons` ont une encoche du côté des jeux les plus faibles. Le fichier `AURA-004_Coupons.f3d` contient la CAO récupérable dans Fusion.

| Coupon | Série CAO | Mesure à consigner |
|---|---|---|
| `Pivot_horizontal_D5` | Ø5,10 à 5,70 mm par pas de 0,10 mm, pour axe Ø5. | Passage, ovalisation, rotation libre et mouvement radial. |
| `Pivot_horizontal_D6` | Ø6,10 à 6,70 mm par pas de 0,10 mm, pour axe Ø6. | Même procédure. Relever séparément incidence de l’orientation et de l’assemblage serré. |
| `Portee_verticale_D15` | Ø15,10 à 15,70 mm par pas de 0,10 mm. | Passage de la portée J5, frottement et jeu axial du montage complet. |
| `Guidage_G1_paires_axe_D3` | Paires de trous, entraxe 7,80 mm et Ø3,10 à 3,70 mm. | Coulissement des deux guides ensemble sans point dur. |
| `Insert_M3_5p7` | Trous borgnes de 7 mm, Ø3,8, 4,0, 4,2 et 4,4 mm. | Mise à fleur, fissures, couple avant rotation, puis traction sur trois coupons. |

Le jeu radial mis à l’essai vaut la moitié de l’écart de diamètre. Imprimer les coupons avec le même lot, la même orientation et les réglages prévus pour la pièce. Mesurer avec des piges ou un alésomètre, et contrôler deux directions par trou. Essayer trois répétitions avant de corriger une cote. Pour l’insert M3 × 5,7, le plan CNC Kitchen indique un avant-trou nominal de Ø4,0 mm. Vérifier les résultats avant de dimensionner un insert dans le corps final. [Plan des inserts CNC Kitchen](https://cnckitchen.com/s/CNCKitchen_Heat-Set-Insert-Dimensions-and-Design-Guidelines.pdf).

Séquence de montage à blanc. Plaque et appuis, socle et épaule, manchons/arbres J2–J4, rotor et entraînement J5, deux guides puis écrous et vis G1, coques en dernier. Contrôler la remise en place des détrompeurs, la préhension à la main, la libre rotation après serrage et les trajectoires de l’outil de montage.

Pour passer au profil réel, relever le fabricant et le modèle d’imprimante, le volume utile, la buse installée, le type de plateau, le matériau et le lot, le profil slicer/firmware et le résultat dimensionnel des coupons. Aucune impression n’a été lancée.

### Plateau virtuel des cinq coupons

Depuis la racine Aura, ouvrir `Exports_Fusion/AURA-004_Fabrication/Plateau_AURA004_Coupons_VIRTUEL.3mf` comme projet dans PrusaSlicer. Il contient les cinq maillages d’origine, chacun à l’échelle 1:1, avec le profil exploratoire PETG et le plateau de 220 × 220 mm. La réouverture et le tranchage dans PrusaSlicer 2.9.6 ont restitué la buse de 0,4 mm, les couches de 0,20 mm, les supports automatiques et la bordure de 3 mm. Avec les bordures, les boîtes englobantes sont distantes d’au moins 12,5 mm entre elles et de 27,5 mm du bord théorique. Le plateau complet est estimé à **65,93 g, 21,58 m et 7 h 35 min**. Le G-code de vérification a été produit en local puis effacé. Le profil machine, la matière et le plateau d’atelier restent à confirmer.

| Rangée dans le projet | Coupon | Emprise XYZ en mm | Axe des perçages dans le projet |
|---|---|---|---|
| 1, Y = 37 mm | Pivot D5 | 94 × 13 × 13 | Horizontal |
| 2, Y = 73 mm | Pivot D6 | 94 × 13 × 13 | Horizontal |
| 3, Y = 109 mm | Portée D15 | 143 × 22 × 6 | Vertical |
| 4, Y = 145 mm | Double guidage G1 | 119 × 11 × 10 | Horizontal |
| 5, Y = 181 mm | Insert M3 × 5,7 | 49 × 14 × 10 | Vertical |

Les sections des maillages confirment le sens des séries de diamètre, du X le plus faible au plus élevé, et l’entraxe de 7,80 mm à l’intérieur de chaque paire G1. Reproduire l’orientation de l’alésage dans la pièce finale. Une portée finale verticale et un trou de coupon horizontal exigent deux essais distincts.

### Mesures et choix des ajustements

1. Relever la machine, le profil, la buse, le matériau et le lot. Pour mesurer la répétabilité, prévoir trois impressions du profil retenu. Après refroidissement et retrait des supports, noter la bavure, la déformation et la facilité d’accès pour chaque coupon.
2. Pour chaque axe métallique, relever le diamètre maximal mesuré. Pour chaque alésage, relever le plus petit diamètre mesuré parmi les deux directions de mesure et, pour un trou débouchant, aux deux extrémités. Le jeu diamétral minimal estimé est la différence entre ces deux valeurs. Pour une portée cylindrique, le jeu radial nominal est la moitié de l’écart diamétral. Consigner l’ovalisation séparément.
3. Pour les pivots et la portée J5, tester une rotation complète à la main sur le coupon avec la pièce conjugée, puis vérifier la rotation après serrage au montage à blanc. Pour G1, engager les deux axes en même temps et vérifier toute la course à la main. Relever le jeu et les points durs dans les deux sens. Retenir le plus petit diamètre satisfaisant la fonction sur les trois répétitions, puis valider le jeu de l’articulation montée.
4. Pour les inserts, renseigner profondeur, température de pose, affleurement, rotation et fissures. Faire les essais de couple et d’arrachement sur des pièces séparées ayant une épaisseur de paroi représentative. Définir le critère à partir de la charge et du serrage prévus pour la fixation finale et retenir la condition qui satisfait les deux essais.

| Tirage et profil | Coupon et Ø CAO | Ø axe et Ø alésage mesurés | Jeu minimal et ovalisation | Course ou tenue observée | Verdict |
|---|---|---|---|---|---|
| À renseigner | | | | | |

Consigner les mesures avec le montage correspondant dans la [[08_Tests/MATRICE_TESTS#AURA-004 — Essais de la branche motorisée|matrice de validation]].

## AURA V3 r03 — Kit d’impression

Depuis la racine Aura, ouvrir `Exports_Fusion/AURA_V3/Fabrication_r03/AURA-01_V3_FDM_r03_Kit_impression.zip`. Le kit réunit le guide, onze STL déjà orientés et six projets 3MF pour les **23 pièces imprimées**. La plus grande emprise est celle du socle de 186 × 176 mm. Les axes, vis, paliers et actionneurs se montent séparément.

Les onze maillages ont été vérifiés fermés, en un seul tenant et en millimètres. PrusaSlicer 2.9.6 a retranché chacun des six plateaux après réouverture du 3MF, avec le profil PETG intégré sur 220 × 220 × 250 mm. Le segment distal est le seul à générer des supports. Le tranchage unitaire estime environ 0,6 g de support. Pour l’ensemble, le profil virtuel estime 1 002 g et 92 h 22 min.

Valider un seul doigt avec trois phalanges et les KST X06 V6.0. Contrôler l’axe passif de 3 mm dans l’alésage nominal de 3,40 mm, le jeu latéral nominal de 0,80 mm par joue, la fixation des pattes et le passage des fils dans toute la flexion choisie. Les réglages de l’imprimante réelle et les essais de résistance restent à établir. [[02_Conception_Fusion/DESIGN_V3#V3 r03 — Structure simplifiée pour le FDM|CAO r03]] · [[08_Tests/MATRICE_TESTS#V3 r03 — Assemblage et impression|Matrice]]
