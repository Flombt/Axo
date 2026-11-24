# AURA-01 V3 — Bras à trois segments et main blanche

## V3 r03 — Structure simplifiée pour le FDM

La r03 conserve trois segments de **140, 123 et 112 mm** entre axes, sept pivots de pose et quinze pivots de doigts. Huit pièces uniques et trois formes de phalange répétées cinq fois donnent **23 pièces à imprimer**. Les fourches, ponts, logements et coques auparavant disjoints sont réunis par corps articulé. Les servos des doigts s’insèrent par le dessous. Les perçages horizontaux les plus critiques ont un toit à 45°. La platine de 186 × 176 mm porte quatre passages Ø6,9.

L’audit de la r02 rouverte dans Fusion a trouvé **13 interférences entre composants à HOME** et 110 recouvrements entre corps distincts d’un même composant. Les principaux conflits concernaient le longeron de l’épaule, la chape du poignet et l’implantation du pouce. Les 22 poses comparées ont présenté des collisions dans la r02. La r03 dégage les axes, réduit les porte-à-faux autour des fourches et libère le passage du pouce.

Autodesk Fusion a commandé les **22 pivots** et testé **165 poses**, dont les 22 de comparaison, sur les 23 solides imprimés et 18 enveloppes de servo. Aucun volume d’intersection n’a dépassé 0,001 mm³ dans les positions testées. L’archive F3D a été exportée puis rouverte dans Fusion avec ses 22 pivots. Les résultats détaillés se trouvent dans `Exports_Fusion/AURA_V3/Fabrication_r03/Verification_FDM_r03.json` depuis la racine Aura. [[08_Tests/MATRICE_TESTS#V3 r03 — Assemblage et impression|Matrice des preuves]]

Les fixations de moteurs, les faisceaux, les paliers, les transmissions et la résistance restent à éprouver au montage à blanc puis au banc. Les limites des poses numériques sont dans le relevé. Le quantitatif et le profil d’impression se trouvent dans le [[03_Impression_3D/PROTOCOLes_FDM#AURA V3 r03 — Kit d’impression|protocole FDM]].

## Historique r02

La V3 r02 est une maquette native indépendante, créée et pilotée dans Autodesk Fusion 2706.1.17 le 22 novembre 2026. Depuis la racine Aura, les fichiers sont dans `Exports_Fusion/AURA_V3`.

L’archive a passé le contrôle d’intégrité. Le réimport a ensuite réussi par le script d’audit r03 dans Fusion.

| Livrable | Fichier |
|---|---|
| Assemblage natif, pose de référence | `AURA-01_V3_Main-articulee_r02.f3d` |
| Vidéo en trois chapitres, 10,5 s | `AURA-01_V3_Demonstration.mp4` |
| Vue d’ensemble | `AURA_V3_Apercu.png` |
| Relevés des pivots, des logements et de l’export | `Verification_CAO.json` |
| Générateur local Fusion | `Generateur_AURA_V3/Generateur_AURA_V3.py` et `geometrie.py` |

## Cinématique et style

- Trois segments en série de **140, 123 et 112 mm** entre axes. J1 oriente le socle en lacet. J2, J3 et J4 règlent l’élévation et la flexion des trois segments. J5, J6 et J7 donnent au poignet la déviation, la flexion et le roulis. Les axes de flexion du bras sont parallèles en pose de référence. Le lacet du socle et les trois axes du poignet étendent l’espace des poses.
- **Cinq doigts, trois phalanges par doigt et un pivot indépendant par phalange**. Le pouce part de biais pour replier ses trois segments vers la paume. Les quatre autres doigts plient dans des plans voisins. Le modèle totalise **22 pivots** et 23 composants mobiles ou fixes.
- La paume et les capots des doigts sont blancs. Le bras utilise des longerons graphite, des capots gris perle et des repères bleu pétrole près des articulations. La main mesure environ **256 mm du pivot de roulis au bout du majeur étendu**. La dimension tient compte du servo, des pattes, de la visserie et des passages de câble à chacune des quinze positions.
- La platine fait 274 × 216 × 9 mm et porte quatre passages Ø6,7. Les coupes du poignet et les longerons sont préliminaires. Les cotes de la maquette résident dans le générateur. Les solides natifs et les liaisons sont éditables dans Fusion.

## Logements et transmission dans les doigts

Le boîtier KST est porté par la phalange qu’il actionne. Sa sortie est au même axe que le pivot. Le siège du palonnier appartient à la phalange précédente ou à la paume. La joue opposée porte un axe passif Ø3,04 et une bague qui reprennent les efforts transversaux. Cette disposition évite de faire traverser le boîtier par l’axe passif. Les pattes de servo sont représentées d’après leur plan coté. Le capot de chaque phalange est un corps démontable, avec deux passages de vis. Des dégagements amorcent le chemin des fils et un évidement réduit la matière aux extrémités.

Les logements nominalement libres laissent environ 0,55 mm à la patte la plus proche, 0,57 mm par côté au niveau du boîtier et 0,85 mm sous le boîtier. Fusion a contrôlé **15 paires boîtier/logement sans volume d’intersection**, sur les enveloppes CAO au repos. Tenue des pattes, centrage du palonnier constructeur, fixation de la bague et boucles de câble restent à éprouver sur une phalange.

## Limites et dimensionnement d’atelier

Chaque pivot natif a été commandé séparément de 8°. Le point témoin a bougé et le relevé des autres angles est resté à zéro à la précision du relevé. Les bornes des doigts sont de 0 à 62°, 0 à 72° et 0 à 66° depuis l’ouverture. Le roulis du poignet a été animé de part et d’autre de la position neutre jusqu’à environ 55°. Les scènes de la vidéo illustrent les mouvements en CAO. Les essais de charge, de durée, de câblage et de collisions de l’assemblage sur toutes les trajectoires sont ouverts. [[08_Tests/MATRICE_TESTS#V3 — Contrôles du bras à main articulée|Matrice V3]]

Le calcul horizontal de premier dimensionnement utilise des masses réparties de 0,33, 0,30, 0,23, 0,26 et 0,38 kg pour les trois segments, le poignet et la main, aux abscisses 70, 201,5, 319, 416,5 et 580 mm depuis J2. À vide, les moments statiques de J2, J3 et J4 valent environ **4,76, 2,93 et 1,70 N·m**. À titre de cible provisoire avec un facteur de service 1,5, cela donne 7,14, 4,40 et 2,55 N·m au joint. Peser les modules et établir le couple continu, la réduction, l’équilibrage et la retenue hors tension avant d’arrêter les moteurs du bras. La platine ancrée et la retenue mécanique précèdent l’essai sous tension du bras complet.

Commencer par une phalange FDM avec un seul servo, son palonnier et son axe opposé. Mesurer l’ajustement et le jeu après assemblage, la masse imprimée, la course utile, l’effort et l’échauffement sur des cycles répétés. Monter ensuite un doigt complet à l’horizontale pour vérifier que son moteur proximal tient la masse des trois phalanges. [[05_Electronique/README_MOTEURS_V3|Références moteurs et couples]]

## AURA-006 — Branche mécatronique

La branche indépendante reprend la silhouette r03 et ajoute une main motorisée en CAO, l’implantation des véritables encombrements ROBOTIS et la place des modules de puissance. Le banc J2 indépendant porte l’effort sur un arbre à roulements et permet de caractériser le frein de maintien. [[02_Conception_Fusion/INTEGRATION_MECATRONIQUE_V3|Résultats et limites par sous-ensemble]] · [[03_Impression_3D/NOTICE_BANCS_V3|Montage et essais]].
