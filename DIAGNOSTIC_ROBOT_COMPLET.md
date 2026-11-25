# AURA-01 · Diagnostic technique complet avant fabrication

**24 novembre 2026 · V5 « Revue design · Roulis épaule et coude », Fusion v1**

> Audit de la V5 roulis v1. Le [rapport du 25 novembre](RAPPORT_CORRECTIONS.md) donne l’état de sa révision de stabilisation.

## 1. Résumé exécutif

**Reporter la fabrication du robot complet et les achats du lot.** Le F3D se réouvre dans Fusion et permet six axes et cinq commandes de doigts distinctes en CAO. Mais le bras traverse le plan de table, les quatre gaines franchissent J1 sans liaison mobile définie et la tenue à la coupure reste inconnue. La puissance envisagée est inférieure à la pointe de conception. Les fichiers de tranchage et la commande disponibles appartiennent à des révisions antérieures.

- **Impression.** Le modèle contient **69 occurrences imprimables, 56 références**. Le F3D est le seul export retrouvé pour cette révision. Les plateaux Anycubic r05 correspondent à un autre assemblage. [Inventaire et statut par pièce](docs/diagnostic/latest/preuves/pieces_v5_roulis.csv)
- **Mouvements.** **141 poses acceptées sur 153 demandées**, dont **33 contrôlées au noyau d’interférence** avec la quincaillerie et les enveloppes du faisceau. La main atteint **−56,68 mm sous le plan de table**. À ±88° de lacet, les extrémités des quatre jonctions de gaine s’écartent de **33,31 à 39,45 mm**. [Mesures](docs/diagnostic/latest/preuves/analyse_mecanique.json)
- **Main et motorisation.** Les cinq doigts répondent séparément en CAO. La pince conserve **17,68 mm** entre extrémités dans le meilleur des 36 cas sondés. À **20 g**, le calcul en PETG plein donne **0,368 N·m à J2** et **0,165 N·m à J3** pour la gravité seule. Le scénario chargé avec friction dépasse l’hypothèse de service de J2. [Mesures de pince](docs/diagnostic/latest/preuves/pince_grille_fusion.json) · [Efforts](docs/diagnostic/latest/preuves/analyse_mecanique.json)
- **Énergie et commande.** Le rail **5 V / 10 A** est comparé à **11,3 A** de pointe cumulée selon les hypothèses du panier. Le firmware r05 pilote six voies et son fichier principal échoue à la compilation MicroPython testée. [Essai firmware](docs/diagnostic/latest/preuves/firmware_r05.json)
- **Coût.** Le panier cible annonce **149,48 €** hors filament et corrections. Avec une bobine affichée à **11,95 €**, le scénario atteint **161,43 €**. Le plafond **150 €** reste à démontrer. [Panier V5 roulis](purchases/NOMENCLATURE.md) · [Prix du PETG](https://www.makermind.fr/p/filament-petg-yourdroid-blanc-chaud-1-75-mm-1-kg)

**Maturité moyenne 27/100. Préparation à la fabrication 17/100.** La section 16 donne les verdicts séparés.

## 2. Révision, preuves et périmètre

| État | Identification et résultat |
|---|---|
| **Actif et audité** | Projet Fusion **Robotic Arm — V1**, document **AURA-01 V5 — Revue design · Roulis épaule et coude**, **v1 sur v1**. Logiciel **2706.1.17**, ID **urn:adsk.wipprod:dm.lineage:S7DLYnxoTsq4-clhF52BRA**, aucune modification en attente au relevé initial. |
| **Archive contrôlée** | F3D réimporté dans un document temporaire. **154 occurrences**, **153 liaisons as-built dont 31 pivots**, **20 liens de mouvement**. SHA-256 **55d3f7964cd04625a4f9062db03c406900fc6acf57cedec86a5bfd5b46495361**, conforme à la trace de création. |
| **Parent direct** | V5 « Revue design » v2, 116 occurrences et neuf servos dont cinq commandes de doigts, avec J7 motorisé. F3D **d44b5dbafedf1d7ecbb4df91b2020320680f58dc70f29f906f79b77b0ccff923**. |
| **Dernière révision publiée** | GitHub **Flombt/Axo**, unique branche **main**, tête **ecc2308ec4521cbc6c49ad148433d983fa783578**, **r05 Budget Edition**. Tags r03 cinématique et r04 fabrication. Les deux V5 ultérieures sont présentes dans Fusion et sur disque. |
| **Historique consulté** | Assemblage final V1, V2 et AURA-004, grande V3 et bancs, kit r02, bras de table r03/r04/r05 et les deux V5. Les preuves de fabrication et de commande portent sur leurs révisions respectives. |

[Inventaire Fusion actif](docs/diagnostic/latest/preuves/fusion_actif.json) · [Archive V5 roulis](https://github.com/Flombt/Axo/blob/aura-01-v5-roulis-v1/fusion/AURA-01.f3d) · [Archive V5 revue](archives/v5-revue/fusion/AURA-01_V5_Revue_Design.f3d) · [GitHub vérifié](https://github.com/Flombt/Axo/tree/ecc2308ec4521cbc6c49ad148433d983fa783578)

L’inventaire couvre le dossier Aura et six dossiers de travail AURA sur D:. Il contient **1 134 fichiers, 593 signatures distinctes**. On compte **443 STL, 592 3MF, 49 archives Fusion, 22 STEP, 3 Blender et 25 MP4**. Les outils Autodesk MCP ont lu le document actif, exercé le solveur et mesuré le modèle réimporté. Computer Use a affiché Fusion et les plateaux dans Anycubic Slicer Next. Trois scènes ont été ouvertes dans Blender 5.2.1. Les scripts de conception et jeux de preuves des dossiers D: ont servi à retrouver le modèle de routage et les hypothèses historiques. [Inventaire de fichiers](docs/diagnostic/latest/preuves/inventaire_fichiers.csv) · [Scripts d’audit](docs/diagnostic/latest/scripts/)

Les mesures CAO, les analyses numériques, les hypothèses et les fiches commerciales ont des niveaux de preuve distincts. Aucun essai physique n’a été réalisé. Fusion a retrouvé le document actif v1 après fermeture de la copie d’audit, sans modification en attente. Le fichier autonome **RAPPORT_IMPRESSION_3D.md** n’a pas été retrouvé dans les répertoires examinés. Les rapports r04 et r05 documentent leurs préparations d’impression. [État final Fusion](docs/diagnostic/latest/preuves/etat_fusion_fin_audit.json) · [Premier diagnostic](archives/r02/DIAGNOSTIC_ROBOT.md) · [Améliorations r03](archives/r03/RAPPORT_AMELIORATIONS_R03.md) · [Fabrication r04](archives/r04/VALIDATION_FABRICATION.md) · [Optimisation r05](archives/r05/OPTIMISATION_BUDGET_R05.md) · [Profils r05](archives/r05/anycubic/README.md)

## 3. Conception mécanique, pièce par pièce

Le tableau couvre chaque occurrence avec repère Fusion, parent, quantité, référence d’impression, dimensions et statut. Le JSON conserve les centres, directions et dimensions des faces cylindriques. Ces cotes incluent des arrondis et ne désignent un perçage qu’après repérage de la face. L’enveloppe neutre du robot est **337,41 × 121,50 × 141,05 mm**. [154 occurrences et statuts](docs/diagnostic/latest/preuves/pieces_v5_roulis.csv) · [Géométrie native](docs/diagnostic/latest/preuves/fusion_geometrie_neutre.json)

| Sous-ensemble | Résultat et conséquences |
|---|---|
| **Platine, appui et carte** | Platine **150 × 114 × 6 mm**, quatre trous **Ø5,50 mm** sur **129 × 94 mm**. Les gaines se recouvrent et traversent les enveloppes du socle. L’accès USB, le rayon sous couvercle, la sortie des fils et la chaîne de coupure dépassent le gabarit du Pico. |
| **J1 · axe, rondelles, 608 et pignon** | Deux roulements **8 × 22 × 7 mm**, centres à **20,95 mm** d’écart en Z. Diamètres cylindriques de **22,22 et 22,46 mm** dans le palier. Contrôler l’emmanchement, l’appui des bagues intérieures, la pile de rondelles, le jeu axial et l’efficacité de l’entretoise. Les 608-2RS CAO et les 608.ZZ du panier ont les mêmes cotes nominales. La protection et le comportement réel dépendent du lot. |
| **J2/J3 · MG996R, chapes, pignons et freins** | Les deux axes acier nominaux Ø5 sont portés par des chapes. Les gabarits d’axe atteignent **57,12 mm hors tout**. Le panier propose des **M5×70 sous tête**. Présenter le boulon réel, sa portée lisse et sa projection sous coque. La denture **module 0,8**, rapports **3:1 et 2:1**, transmet l’effort du palonnier au tourillon. La rigidité des joues et les pertes sous précharge restent à éprouver. |
| **J2R/J3R · arbre, chapeau, collier et butée** | Chaque reprise ajoute **8 mm** à un entraxe, portés à **80 et 101 mm**. Portée **Ø15,92** dans **Ø16,42 mm**, soit **0,25 mm** radial. L’évidement longitudinal **Ø8,70 mm** laisse **3,61 mm** de paroi radiale nominale avant les transitions. Passages de chapeau **Ø3,18 mm**. Goupille/vis **Ø1,956 × 2,86 mm** dans un passage **Ø2,17 mm**. La retenue positive, l’accès à l’outil, le jeu après assemblage et l’usure restent à déterminer. |
| **Avant-bras, cassette et carénages** | Cassette **45,8 mm** de large, cinq loges en 3+2. Le capot inférieur recouvre l’enveloppe du tronc électrique de **154,52 mm³** au neutre. Deux gaines heurtent la coque du bras dans le modèle. Réserver les volumes de connecteurs et de service en fermant les gardes. |
| **J7 · support, palonnier, poignet et paume** | Course CAO **±32°**. Le palier coaxial doit reprendre la charge hors cannelure et le palonnier ne doit transmettre que le couple prévu. Les cinq trajets près de J7 peuvent modifier tension et flexion quand la paume tourne. |
| **Pouce et quatre doigts** | Chape démontable, axe commun **Ø1,986 × 47,56 mm** et deux retenues. Onze pivots de phalanges sur vis M2 et deux vis de chape. Examiner la tenue des conduits de faible diamètre, des écrous et des ancrages de tendon. Les rappels et les interfaces de pince demandent un montage instrumenté. |

La charge suit les phalanges, la paume, les arbres de roulis, les tourillons de tangage, la tourelle et les 608 jusqu’aux fixations. Les zones sensibles sont les dentures, les paliers fendus et les attaches de brin. Tester après qualification une réduction de la masse des capots et du nombre de fixations, sans perdre l’accès de maintenance. [Vue du modèle actif](docs/diagnostic/latest/wireframes/01_fusion_actif.png) · [Coupes des paliers](docs/diagnostic/latest/wireframes/08_coupes_paliers_annote.png)

## 4. Cinématique, interférences et socle

### Campagne exécutée

Les six axes et cinq tambours ont été sollicités séparément à plusieurs angles. Les combinaisons comprennent une grille J2/J3, les roulis avec tangages, le lacet et plusieurs prises. **137** des **153** cibles ont été atteintes au premier parcours à **0,02°** près. **Quatre** de plus l’ont été après reprise par pas depuis le neutre. **Douze** combinaisons de lacet, roulis et prise ne sont pas confirmées. Le solveur a notamment laissé le pouce à une autre position ou renvoyé la borne opposée sur certains pivots. Cela limite la preuve numérique des transitions. [Campagne Fusion](docs/diagnostic/latest/scripts/campagne_fusion.py) · [Reprises](docs/diagnostic/latest/preuves/fusion_reprises_130_145.json.gz)

**33 poses** ont passé une analyse d’interférence avec **233 corps**, y compris quincaillerie et enveloppes souples, en écartant les repères de liaison et les faces coïncidentes. Seuil **0,03 mm³**. Parmi **141 paires distinctes**, **139** comportent une enveloppe souple. Les deux paires purement rigides sont les vis M4 dans leurs supports, environ **10,44 mm³** d’engagement par paire. Les **133 zones** au neutre incluent plusieurs intersections pour certaines paires. [Détail et maxima](docs/diagnostic/latest/preuves/analyse_mecanique.json)

- **Table.** Quinze poses passent sous Z=0. À **J2 −21°, J3 −32°**, la main descend à **−56,68 mm**. À **−21°/−8°**, le point bas est encore à **+8,52 mm**, main ouverte et autres axes neutres. À **−7°/−32°**, il est à **−1,97 mm**. Une contrainte couplée et une limite matérielle doivent couvrir mouvement, relâchement, roulis et réglage de la main. [Projection cotée](docs/diagnostic/latest/wireframes/06_plan_table_annote.png)
- **Gaines et fils.** Au neutre, la coque du bras recouvre les gaines J3R de **120,63 et 117,25 mm³** et le capot de cassette recouvre son faisceau de **154,52 mm³**. Plusieurs gaines se croisent dans le même volume. L’engagement d’une extrémité dans son raccord peut être voulu. Les recouvrements en milieu de parcours et dans les carénages demandent reprise et contrôle avec les fils du lot. [Vues de routage](docs/diagnostic/latest/wireframes/10_passages_souples_annote.png)
- **Marges ponctuelles.** Entre les vis d’arrêt J1 et la tourelle, minimum **0,50 mm** aux bornes. Entre les butées de roulis et leurs colliers, minimum **0,15 mm** aux bornes mesurées, écart axial sur les points de Fusion. Les extrémités des quatre doigts longs à même consigne laissent **4,00 mm** entre voisines aux poses ouverte et fermée. [Distances BRep](docs/diagnostic/latest/preuves/distances_fusion.json)

Le contrôle est quasi statique. Les poses échantillonnées et les voisinages mesurés n’établissent pas une marge minimale globale ou continue. Les vrais connecteurs, rayons, précharges, nœuds et déformations restent à mesurer.

### Course J1 câblée

Le solveur atteint **±88°**, soit **176° nominaux**, avec **±50,95°** au servo. Le pignon moteur comporte **38 dents**, la roue de sortie **22**. La rotation continue, le collecteur et la puissance tournante propres à la r04 ont été abandonnés dès la r05. Les deux vis M4 et les 608 décrivent l’arrêt et le maintien, dont le comportement sous charge reste à éprouver.

Aux quatre jonctions, un côté est fixe sur la platine et l’autre suit la tourelle. À ±88°, le calcul par transformées Fusion donne **36,23 / 39,45 mm** de séparation pour les passages J2R et **33,31 / 35,46 mm** pour J3R. Aucune boucle dynamique dimensionnée ne couvre ce déplacement dans les fichiers. **La course exploitable reste inconnue.** Tester ensemble la longueur libre, le rayon, l’effort résistant, le passage électrique, les arrêts et la course logicielle. [Raccords à ±88°](docs/diagnostic/latest/wireframes/07_raccords_j1_annote.png) · [Socle Fusion ouvert](docs/diagnostic/latest/wireframes/03_fusion_socle_j1.png)

### Stabilité

Sans lest et avec alimentation externe, le modèle PETG plein donne **774,86 g à vide**, dont **460,38 g** de pièces imprimées pleines. Centre de masse au neutre **(33,58 ; 0,43 ; 62,31) mm**. Une sensibilité avec 60 % de la masse imprimée donne **590,71 g** à vide. Ce coefficient représente un cas de calcul, le taux de remplissage et la masse réels restent à mesurer.

Avec **20 g** au bout du majeur, marge minimale **4,16 mm** dans le rectangle d’ancrage et **14,16 mm** au bord d’appui idéalisé. Le moment de rappel correspondant est **0,110 N·m**. Au cas 60 %, les valeurs sont **2,78 mm**, **12,78 mm** et **0,077 N·m**. Une traction illustratrice de **1 N à 140 mm** produit déjà **0,140 N·m**. Fixer les **quatre M5** sur un support rigide et éprouvé. Au banc, vérifier soulèvement, glissement et efforts d’assemblage avec le bras retenu. Le rectangle d’enveloppe est optimiste si les pieds ou bords réels fournissent une surface plus petite. [Scénarios de stabilité](docs/diagnostic/latest/preuves/analyse_mecanique.json)

## 5. Motorisation et transmission

| Axes | Composant au panier et prix TTC | Caractéristiques publiées et exigences CAO |
|---|---|---|
| **J1, J7** | 2 × **Tower Pro SG90 RBS15198** à **4,49 €** | **23 × 12,2 × 29 mm**, **9 g**, **1,8 kgf·cm** au blocage à 4,8 V et **0,12 s/60°** selon Tower Pro. La fiche du vendeur annonce une force de positionnement et une vitesse moindres. Courses moteur requises **101,9°** et **64°**. Mesurer palonnier, fixation, sortie de câble, tenue à 3,3 V de signal et précision en charge. |
| **J2, J3** | 2 × **MG996R 180° Atelier de la Robotique** à **7,59 €**, 7,99 € seul | Vendeur **40,7 × 19,7 × 43 mm**, **55 g**, 4,8–6 V, **13/15 kgf·cm** à 4,8/6 V, **0,17/0,13 s par 60°**. Tower Pro publie **9,4/11 kgf·cm** et **0,19/0,15 s par 60°**. La représentativité du gabarit, des oreilles et de la cannelure doit être vérifiée lot en main. Courses moteur **126°** et **128°**. |
| **J2R, J3R** | 2 × **MakerMind MG90S RBS11204** à **3,95 €** | **22,8 × 12,2 × 28,5 mm**, **13,4 g**, 4,8–6 V, **1,8/2,2 kgf·cm** au blocage et **0,10/0,08 s par 60°**. Course au tambour **±60° / ±72°**. Gabarit CAO de microservo avec pattes. Vérifier empreinte, angle utilisable, traction et jeu sous précharge. |
| **P/I/M/A/U** | 5 × **MakerMind SG90 RBS10195** à **1,55 €** | **23 × 12,2 × 29 mm**, **9 g**, **1,5 kgf·cm à 4,8 V**, **0,30 s/60°**, 0–180° catalogue, dentures POM. La fermeture demande **92° de bobine** depuis l’ouverture. Étalonner le neutre de chacun et contrôler le palonnier et l’effort réel. |

Les fiches ne garantissent ni le courant de service des lots exacts, ni la précision en charge, ni le couple continu chaud. Les mesures doivent partir de l’empreinte et du lot exacts. [SG90 Tower Pro](https://towerpro.com.tw/product/sg90-analog/) · [Offre RBS15198](https://www.makermind.fr/p/tower-pro-sg90-servo-micro-analogique-9g) · [SG90 économique](https://www.makermind.fr/p/servomoteur-micro-sg90-9g-pour-modelisme-rc-avion-projets-arduino) · [MG90S](https://www.makermind.fr/p/servomoteur-micro-mg90s) · [MG996R Atelier](https://www.atelierdelarobotique.fr/produit/servomoteur-numerique-mg996r-15-kg-cm) · [MG996R Tower Pro](https://towerpro.com.tw/product/mg996r/)

### Efforts calculés à partir des volumes et positions

Le calcul emploie les volumes et centres Fusion, **1,27 g/cm³** pour le PETG plein, des masses unitaires de **9 / 13,4 / 55 g** pour les servos, **12 g par 608**, **3,5 g** pour le Pico et des densités de gabarit pour acier, PTFE et faisceau. Les éléments absents de la CAO restent hors modèle. La charge est au bout du majeur. Pour chaque axe, l’arbre des pièces désigne ses masses entraînées, dont on projette le moment du poids sur l’axe. Le terme **I × α** emploie l’inertie approchée des masses ponctuelles et les accélérations r05 ou, pour les nouveaux roulis, des valeurs illustratives de 35 et 50°/s². [Méthode](docs/diagnostic/latest/scripts/analyse_mecanique.py) · [Scénarios et poses maximales](docs/diagnostic/latest/preuves/analyse_mecanique.json)

| Axe | Gravité à vide (N·m) | 10 g (N·m) | 20 g (N·m) | Terme inertiel maximal à 20 g (N·m) |
|---|---:|---:|---:|---:|
| J1 | 0 | 0 | 0 | 0,00560 |
| J2 | 0,314 | 0,341 | 0,368 | 0,00389 |
| J2R | 0,0326 | 0,0371 | 0,0417 | 0,00087 |
| J3 | 0,127 | 0,146 | 0,165 | 0,00188 |
| J3R | 0,0073 | 0,0088 | 0,0115 | 0,00005 |
| J7 | 0,0024 | 0,0044 | 0,0070 | 0,00003 |

Les maxima peuvent venir de poses différentes. En reprenant **à titre de scénario** la friction r05 **0,266 / 0,107 N·m** et la réserve câble **0,010 N·m**, on atteint **~0,648 / ~0,284 N·m** pour J2/J3 à 20 g. Le scénario optimiste précédent de service supposait **25 %** du blocage Tower Pro de **0,922 N·m** avec les rapports et **75 %** de rendement, soit **0,519 / 0,346 N·m** en sortie. Ce facteur de service reste une hypothèse. À J2, même le calcul à vide avec ce frottement dépasse 0,519 N·m. À J3, seule une qualification soutenue permet de fixer une charge d’usage. Le blocage et les différences de fiches entre marques ne donnent pas une capacité continue. Les rayons primitifs J2/J3 **21,6 / 14,4 mm** donnent environ **30 / 20 N** tangents dans le scénario chargé. Mesurer le rendement, la tenue de la denture, la température et la répétabilité, puis comparer compensation, allègement distal et réduction. [Calculs r05](archives/r05/OPTIMISATION_BUDGET_R05.md#masse-tenue-mécanique-et-courant)

Le SG90 **J1** transmet un rapport de couple **22/38**. Avec 75 % de rendement, **0,077 N·m** représente le blocage théorique en sortie et **0,019 N·m** un quart de ce cas. L’inertie atteint **0,0056 N·m** à 20 g. Le couple résistant des 608, du faisceau et de quatre gaines reste à mesurer. Les roulis **J2R/J3R** emploient des rayons **4/12 mm**, soit une réduction idéale **3:1**. Le déplacement nominal des brins depuis le neutre atteint **4,19 et 5,03 mm**. À 4,8 V, le MG90S donne environ **44 N** idéaux au blocage pour un rayon de 4 mm. Courbes serrées, prétension, frottements et jeu peuvent consommer une part importante de la traction. Commencer par un axe longitudinal instrumenté.

## 6. Indépendance des doigts et pince

Cinq occurrences **Moteur_FP/FI/FM/FA/FU**, cinq bobines et quinze liens phalange sont présents dans Fusion. Les cinq commandes individuelles à **75°** entraînent uniquement les trois phalanges du doigt demandé, avec les douze autres angles à **0°**. Les niveaux 25° et 92° et la combinaison différenciée **12/92/56/0/71°** ont aussi été essayés. Au neutre, les quinze pivots reviennent à 0° dans le solveur. Le poing CAO règle les cinq bobines à **92°**. Les extrémités du pouce et de l’index restent à **15,27** et **17,22 mm** de la paume.

Dans la grille de **36** combinaisons pouce-index, les bouts **P3/I3** restent à **43,82 mm** ouverts, **35,12 mm** à 46° chacun, **24,76 mm** à 75° et **17,68 mm** à 92° simultanés. **17,68 mm** est le minimum mesuré de cette grille pour les deux bouts. Les mesures **P2/I3** et **P3/I2** restent à plus de 21 mm. Un objet plus mince que 17,68 mm ne peut donc pas être serré bout à bout dans ces poses avec les surfaces actuelles. La prise enveloppante, la compliance et la force restent à tester. [Grille et points](docs/diagnostic/latest/preuves/pince_grille_fusion.json) · [Pince annotée](docs/diagnostic/latest/wireframes/09_pince_annotee.png)

Avec une gorge de diamètre 9,60 mm, une commande à 92° représente **~7,7 mm** d’enroulement nominal, avant l’épaisseur du fil et son déport. Le blocage idéal d’un SG90 économique correspond à **~31 N** sur cette gorge. Le rapport de phalanges imposé par les liens Fusion ne calcule ni la flexion des brins, ni l’effort de contact, le retour élastique, l’usure des attaches ou la variation du trajet au poignet. Vérifier l’effort de rappel et la réouverture, un doigt bloqué puis une autre voie commandée, et l’évolution des tensions pendant J7/J2R/J3R. Le nylon, les nœuds et les ancrages doivent être éprouvés ensemble.

Les trois projets Blender ouverts documentent le montage r02 et la cinématique r03 v2, dont la scène à **3 960 images et 60 i/s**. Les rendus r04 et r05 appartiennent à leurs architectures. La preuve d’indépendance V5 vient des pièces et liaisons natives. [Inventaire Blender](docs/diagnostic/latest/preuves/blender_AURA-01_Animation.json) · [Rapport cinématique r03](archives/r03/animations/RAPPORT_CINEMATIQUE.md) · [Cassette et doigts Fusion](docs/diagnostic/latest/wireframes/05_fusion_flexion_independante.png)

## 7. Imprimabilité et Anycubic

### Paquet V5 roulis

**Aucune des 56 références V5 n’est prête numériquement pour production.** La cote CAO maximale par pièce atteint **150 mm** et les pièces nues passent le critère d’enveloppe des trois machines. Orientation, supports, temps, filament et résistance du kit V5 restent inconnus. Le CSV attribue à chaque occurrence imprimable **Impression bloquée** faute de fichiers cohérents ou **Modification nécessaire** pour les pièces de routage ou d’interface dont une reprise est déjà identifiée. Les coupons historiques ont un statut **Impression d’essai nécessaire** pour servir à un étalonnage compatible. [Statuts individuels](docs/diagnostic/latest/preuves/pieces_v5_roulis.csv)

Les fichiers ont été contrôlés par empreinte pour traiter les copies identiques. **443 STL** ferment avec orientation cohérente selon le contrôle topologique, en mm dans le contexte des nomenclatures. Le STL ne contient pas d’unité. Les **592 archives 3MF** ont passé lecture, intégrité ZIP et décodage des unités et transformations. Quatre triangles dégénérés affectent quatre maillages de trois projets Prusa historiques r03/r04. Ils restent topologiquement fermés. Les archives Fusion ont été contrôlées côté ZIP et les STEP côté en-tête. L’en-tête STEP ne permet pas de valider les propriétés natives ou les tolérances d’import. [Inventaire, maillages et réglages](docs/diagnostic/latest/preuves/inventaire_fichiers.json)

### Prévisualisation dans Anycubic Slicer Next

| Projet historique r05 | Profil affiché | Estimation observée | Contrôle fait |
|---|---|---:|---|
| **02 Gris** | Kobra 3, buse 0,4, PETG, couche **0,20 mm** | **136,86 g · 6 h 37** | **77,40 g** modèle, **55,66 g** supports et **3,80 g** interfaces. Vérifier l’accès de retrait du support et les appuis fonctionnels du palier et de la tourelle au coupon. [Capture](docs/diagnostic/latest/preuves/anycubic_r05_kobra3_gris.png) |
| **04 Blanc** | Kobra X, buse 0,4, PETG, couche **0,16 mm** | **34,78 g · 3 h 12** | **28,22 g** modèle et **6,56 g** supports et interfaces. Les supports touchent des zones sensibles des phalanges et de la paume. Contrôler les trous, leur orientation et le retrait des supports. [Capture](docs/diagnostic/latest/preuves/anycubic_r05_kobra_x_blanc.png) |
| **05 Coupons** | Kobra 3 Max, buse 0,4, PETG, couche **0,20 mm** | **15,15 g · 48 min 01 s** | Six éprouvettes de portées 608, axes et servos au centre du plateau. Aucun support dans l’aperçu. [Capture](docs/diagnostic/latest/preuves/anycubic_r05_kobra3max_coupons.png) |

Les **18 projets assemblés r05** contiennent le profil machine et le G-code calculé. Les **39 projets individuels** couvrent 33 références de robot et six coupons. Les emprises r05 après transformation des objets restent dans **250 × 250 × 260** (Kobra 3), **260 × 260 × 260** (Kobra X), **420 × 420 × 500 mm** (Kobra 3 Max). Le profil r05 Kobra 3 déclare **255 × 255 mm** et les pièces testées restent dans les **250 mm** nominaux. La planche Graphite r04 d’environ **345 × 233 mm** et les coupons r04 excèdent une dimension des petites Kobra. Ces planches couleur r04 couvrent **61 pièces sur 62** avec chariot de cartes r04 encore à part. [Profils r05](archives/r05/anycubic/README.md) · [Planches couleur r04](archives/r04/anycubic/README.md) · [Volumes Kobra 3 et Max](https://wiki.anycubic.com/en/software-and-app/new-page-anycubic-slicer-beta%28orca-version%29/print-size-range-restrictions) · [Notice Kobra X](https://wiki.anycubic.com/kobra-x/M02010203-Kobra%20X%E7%94%A8%E6%88%B7%E6%89%8B%E5%86%8C-EN-260106.pdf)

Les totaux r05 **hors coupons** sont **321,73 g / 19 h 37** sur Kobra X, **338,04 g / 20 h** sur Kobra 3 Max et **373,50 g / 20 h 18** sur Kobra 3. Les durées et consommations sont des calculs du slicer. Préparer des coupons V5 de 608, des paliers fendus, d’axes et d’écrous, de denture et d’un doigt dans leurs orientations de service. Puis mesurer trous, jeux, arrachement sous effort, fatigue, retrait des supports et dimension des parois avant de déclarer les pièces aptes.

## 8. Montage, visserie et maintenance

| Ordre | Sous-ensemble à présenter à blanc | Contrôle avant fermeture |
|---|---|---|
| 1 | Platine et quatre M5, support captif, paliers 608 et composants fixes jusqu’au Pico et aux deux MG90S | Affleurement M8, portées et empilage de rondelles. Prépositionner les pièces accessibles par-dessous. Vérifier câbles et accès USB, jack et arrêt avec les vraies fiches. |
| 2 | Moteur J1 et pignon, roue et tourelle, arrêts M4 et traversées fixes/mobiles | Entrée de l’outil au palonnier et aux butées. Essayer la course manuellement avec les gaines et les conducteurs réels. |
| 3 | Tourillon J2, axe lisse M5, disques, moteur, pignon et arrêt, puis J2R | Poser goupille, arbre et chapeau dans l’ordre. Vérifier écrou, outil, précharge, plan de retenue et accès des brins sans forcer les joues. |
| 4 | Tourillon et roue J3, longeron, arrêt et palier de roulis J3R | Présenter les vis sous la coque, contrôler l’engrènement et laisser accessibles les arrêts de gaines. N’ôter la retenue de banc qu’après qualification. |
| 5 | Cassette montée sur établi, J7, paume, quatre doigts puis chape du pouce | Passer l’axe partagé avant la chape, prévoir récupération de chaque brin et son rappel. Confirmer le dégagement des connecteurs et le réglage individuel. |
| 6 | Faisceau, protections, capots et essai à la main | Étiqueter les onze voies, contrôler continuité et liberté des trajets. Fermer seulement après avoir vérifié les accès de dépose, la retenue et la coupure. |

**Dépose virtuelle.** Douze cibles, **72 directions de translation** et sept distances entre **1 et 62 mm**, arrêt à la première rencontre. Les parcours sont testés sans flexibles et avec les retraits d’éléments indiqués par voie. Deux MG90S de roulis passent vers **−X** et la cassette complète vers **−Z** après déposes conditionnelles. J2 vers **+Y** rencontre la tourelle dès **1 mm** (8,98 mm³), J3 vers **+Y** rencontre le bras à **3 mm** (0,47 mm³). La dépose individuelle des autres servos n’a pas été démontrée par ces translations. Un parcours en plusieurs étapes ou une autre pièce à déposer reste possible. La cassette déposée facilite le remplacement des doigts mais les extrémités de brins et l’accès en atelier restent à éprouver. [Corridors](docs/diagnostic/latest/preuves/couloirs_montage_fusion.json)

**Reprises ciblées J1 et J7.** Avec le porte-servo J1 également retiré, le gabarit J1 se dégage vers **−X**. La dépose du porte-servo lui-même reste à éprouver. En retirant les capots, le palonnier et le support du J7 dans la simulation, l’avant-bras bloque les six départs droits dès **1 mm**, entre **3,16 et 68,40 mm³**. Définir un autre ordre de retrait ou reprendre son support. [Essais de dépose supplémentaires](docs/diagnostic/latest/preuves/acces_outils_fusion.json)

**Vis et outil.** Les quatre accès aux têtes et écrous J2/J3 acceptent numériquement un gabarit de douille **Ø12 × 35 mm** au neutre après retrait des coques et gardes spécifiées. La tête M8 de J1 s’aborde depuis le dessous, à travers le plan de l’établi si la platine est déjà fixée sur un appui plein. Monter l’axe avant cet ancrage ou réserver un dégagement. Présenter la **M8×55**, les **M5×70**, les quatre ancrages, l’axe Ø2, les M2, les M3 de chapeaux et les butées du lot. Mesurer longueurs, filet utile, rondelles, écrous, appuis et débattement de l’outil réel. L’accès à plusieurs vis de capot et points de gaine reste à valider. [Gabarits d’accès](docs/diagnostic/latest/preuves/acces_outils_fusion.json)

**Notice.** La r02 documente le montage à blanc et un banc captif p. 24. Le schéma p. 3 du manuel pilote un Nano et quatre voies. La V5 demande un schéma à onze voies, un dessin des accès réels et une notice pour la gaine, les retenues et les nouveaux paliers. [Notice r02](archives/r02/kit/Notice_Montage_AURA-01_r02.pdf) · [Manuel r02](archives/r02/kit/Manuel_Technique_AURA-01_r02.pdf) · [Achats V5](archives/v5-revue/ACHATS.md)

## 9. Électronique, alimentation et défauts

Le **Pico 2** est alimenté en USB, les servos par un **rail 5 V externe**, avec masse commune côté basse tension. Le RP2350 a douze tranches PWM à deux voies et les GPIO du Pico 2 fonctionnent à **3,3 V**. Le matériel peut donc fournir onze PWM si les broches sont choisies en conséquence. Le brochage V5, le circuit d’arrêt et la mesure du rail restent à définir. Il faut vérifier les seuils et largeurs d’impulsion des lots réels. Aucun schéma à onze voies ni implantation de l’ensemble des protections et connecteurs n’a été retrouvé. [Pico](https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html) · [PWM RP2350](https://www.raspberrypi.com/documentation/pico-sdk/hardware.html#hardware_pwm)

- **Pointe et maintien.** Neuf micros à **0,90 A** et deux MG996R à **1,60 A** valent **11,3 A**, soit **56,5 W** face aux **50 W** du bloc 5 V/10 A. Ces courants sont ceux du scénario de conception. Un MG et cinq micros en pointe totalisent déjà **6,1 A** avant le maintien des cinq autres servos. Le courant disponible dépend du rail, du jack 5,5 × 2,5, du câble et des contacts JR. L’ampacité de chaque pièce et les courants réels restent à mesurer. [AM5120](https://ampul.eu/fr/alimentations-enfichables/3689-prise-d-alimentation-5v-10a-55x25mm)
- **Chutes de tension.** À 20 °C, avec **0,0175 Ω·mm²/m** pour le cuivre, une boucle de **2 m** en **1 mm²** à **10 A** donne **0,35 V** de chute, ou **0,23 V** en **1,5 mm²**. Ce cas de calcul précède les chutes des connecteurs et du départ mobile. Vérifier les longueurs et la tension minimale aux bornes des servos, les courants de pointe, les fusibles de branches, la dissipation, les surcharges et le comportement thermique. Contrôler les contacts en plus du calibre du bloc.
- **Mouvement et coupure.** La consigne PWM ne mesure pas l’angle réel. Une obstruction, un servo débranché ou un début de chute est invisible au Pico dans l’architecture reprise. Le code r05 demande l’arrêt des impulsions en cas de perte de communication. Il faut caractériser le comportement réel du lot et maintenir le bras et sa charge lorsque le couple disparaît.
- **Retour d’énergie.** Avec l’USB maintenu, une coupure du 5 V moteur ne désarme pas le logiciel r05. Le retour du rail peut appliquer une impulsion encore active. Le réarmement logiciel rappelle aussi la pose neutre sans mesurer la position physique. Il faut un retour d’état du rail, une inhibition indépendante et un réarmement local après vérification de la pose, avec retenue mécanique. Tester l’arrêt, la coupure et le retour de chaque source, le blocage et le redémarrage du microcontrôleur.
- **Source de remplacement.** Le candidat **Mean Well LRS-75-5** donne **5 V/14 A**. Son prix de module ne couvre pas coffret, bornes, arrêt, ventilation et raccordement secteur. Chiffrer et qualifier l’installation complète avant d’en faire la référence de la V5. [Fiche Mean Well](https://www.meanwell.eu/Upload/PDF/LRS-75/LRS-75-SPEC.PDF) · [Offre TME](https://www.tme.eu/fr/details/lrs-75-5/alimentations-integrees/mean-well/)

## 10. Logiciel, cinématique inverse et autonomie

| Niveau de preuve | Résultat |
|---|---|
| **Implémenté en r05** | Six axes J1/J2/J3/P/I/MAU, PWM 50 Hz GP6 à GP11, ARM/STOP/PING/MOVE/STATUS, bornes séparées, rampes et temporisation de **350 ms**. Profil vide et commande inactivée au premier départ d’après le code. |
| **Démontré sur hôte** | Parseur, refus d’ARM sans calibration, refus des valeurs non finies et des voies V5. Les rampes atteignent les cibles, STOP et la temporisation éteignent le modèle de sortie. J2 **−18°** et J3 **−22°** sont acceptés ensemble sans vérification de la garde au plan. |
| **Compilable** | Compilation croisée **MicroPython v1.29.0, .mpy v6.3**. Le fichier **controle.py** réussit. **main.py**, ligne 26, échoue sur le déballage du tuple de limites avec **SyntaxError: *x must be assignment target**. Les deux fichiers passent la vérification de syntaxe CPython. USB, PWM, watchdog et logique physique restent à tester sur la carte après correction. |
| **Développement V5** | Les commandes J2R, J3R, J7, annulaire et auriculaire manquent. Revoir MAU, étalonner chaque axe, resserrer les limites après essais de course, imposer l’enveloppe combinée, contrôler les défauts et rattacher les états à la version de matériel. |
| **Cinématique inverse, PC et IA** | Les liaisons natives et le texte série constituent un départ. Développer une FK contrôlée sur mesures, une IK tenant la redondance et les limites couplées, et un planificateur dont les trajectoires restent dans l’enveloppe éprouvée. Le contrôleur local doit décider l’acceptation des commandes et rester sûr en perte du PC. La perception et la commande IA ne sont ni intégrées ni démontrées sur la V5. |

[Essais reproductibles et compilation](docs/diagnostic/latest/preuves/firmware_r05.json) · [Firmware et protocole r05](archives/r05/firmware/README.md)

## 11. Budget TTC, pièces et couverture

Le panier ci-dessous reconstitue la cible publiée. Les lignes chiffrées combinent les prix publics relus, lots et provisions. Le stock compatible et le prix livré ont besoin de confirmation avant décision. L’objectif reste **100 €** et le plafond **150 €**.

| Poste | Quantités et hypothèses | Sous-total TTC du scénario |
|---|---|---:|
| **11 servos** | 5 SG90 éco à 1,55 €, 2 Tower SG90 à 4,49 €, 2 MG90S à 3,95 €, 2 MG996R à 7,59 € | **39,81 €** |
| **Contrôleur, roulements, USB** | Pico 2 7,15 €, lot payé de 10 × 608.ZZ à 3,95 € pour 2 montés, un USB données 3,00 € provisionné | **14,10 €** |
| **Ports moteurs et commande** | MakerMind France 6,95 € et Atelier en relais 4,99 € selon le panier | **11,94 €** |
| **Puissance et faisceau** | Bloc AM5120 29,00 €, éventuel cordon 2,30 €, XT60/distribution 3,30 €, tronc 1,30 €, fils secondaires 2,70 €, 11 jeux JR 4,40 €, interrupteur 2,20 €, fusibles/supports 5,50 €, protections de fils 1,60 €, port AMPUL 8,50 € provisionnés | **60,80 €** |
| **Quincaillerie et rappels** | Pile M8 2,35 €, 2 M5 avec écrous 3,00 €, 4 ancrages 1,60 €, acier Ø2 0,89 €, port ou retrait groupé 2,11 €, nylon 2,49 €, latex 5,99 €. Stock M2/M3/M4 présumé, à compter. | **18,43 €** |
| **Gaines de roulis** | Tube PTFE Ø4/2, **2 m à 2,20 €/m**, gabarits et reprises à définir | **4,40 €** |
| **Total cible matériel** | Avec les provisions et retraits du panier, hors impression et résolution des blocages | **149,48 €** |

Le bloc est affiché **23,77 € HT**. Cela correspond à **28,52 € TTC si la TVA applicable est 20 %**, avant port et éventuel cordon. La ligne de 29,00 € reste une provision. Le nylon **40/100** apparaît en rupture dans une variante. La fiche d’élastique **8648696** donne **1 mm** en titre et **1,4 mm** en description. Ces écarts et les dimensions réelles des articles déterminent le coût et la faisabilité. Le MG996R affiche du stock et le prix à deux unités lors du relevé. [AM5120](https://ampul.eu/fr/alimentations-enfichables/3689-prise-d-alimentation-5v-10a-55x25mm) · [Ports MakerMind](https://www.makermind.fr/c/informations/livraison-et-paiement/) · [Atelier](https://www.atelierdelarobotique.fr/livraison) · [AMPUL](https://ampul.eu/fr/content/1-livraison-et-paiement) · [Pico](https://www.makermind.fr/p/raspberry-pi-pico-2-rp2350) · [608](https://www.makermind.fr/p/10-x-roulements-a-billes-608.zz-8-22-7-mm) · [PTFE](https://www.makermind.fr/p/tuyau-ptfe-1-metre-2-mm-x-4-mm-pour-extrudeur-bowden-au-metre) · [Nylon](https://www.decathlon.fr/p/fil-de-peche-line-4x4-250m/_/R-p-194133?c=blanc) · [Rappel](https://www.decathlon.fr/p/elastique-plein-en-latex-pf-pa-se-500-1mm-6m/334221/c36m8648696)

| Scénario | Total ou écart |
|---|---:|
| **Mise au point selon le panier** | **149,48 €**, marge arithmétique **0,52 €** avant compléments |
| **Même panier et une bobine de PETG affichée à 11,95 €** | **161,43 €**, dépassement **11,43 €** avant compléments |
| **Sept Tower Pro neufs et deux MG90S** | **162,08 €** hors bobine ou **174,03 €** avec la même bobine |
| **Ensemble confirmé et sûr** | **Indéterminé**. Retenue et arrêt, écran, support et fixations, coffret ou bloc final, arrêts de gaine, connectique effective, pièces de friction, outils manquants, chutes de filament et livraisons à confirmer ou à ajouter. |

Le stock de filament, le nombre de couleurs et les quantités en service se recalculent après un tranchage V5. Réemploi documenté des pièces et câbles, achats groupés et une couleur de PETG peuvent réduire le coût. Le panier matériel actuel demanderait déjà **49,48 €** de réduction pour atteindre 100 € avant compléments. La r04 affiche un devis incomplet de **523,58 € TTC + 7,99 USD** avant port. Les valeurs comparables de panier matériel hors filament sont **141,02 €** pour r05, **148,98 €** pour V5 revue et **149,48 €** pour V5 roulis. La r05 affichait 149,97 € avec une bobine à 8,95 € en promotion. [Panier r05](archives/r05/LISTE_ACHATS_R05.md) · [Panier V5](archives/v5-revue/ACHATS.md) · [Panier roulis](purchases/NOMENCLATURE.md) · [Bobine](https://www.makermind.fr/p/filament-petg-yourdroid-blanc-chaud-1-75-mm-1-kg)

## 12. Problèmes historiques et registre courant

Les **43 problèmes initiaux** et **21 points supplémentaires** des rapports r03, r04, r05 et revues V5 sont vérifiés individuellement en annexe. Les 43 se répartissent en **15 partiellement résolus, 7 toujours présents, 7 réapparus, 5 en attente d’essais physiques et 9 devenus non applicables**. Aucun identifiant complet de la cohorte n’est clos sous « résolu numériquement » dans cette révision. Des sous-fonctions sont vérifiées, dont les cinq voies indépendantes et plusieurs déposes sèches. Les priorités du registre actuel sont propres à la V5.

| Gravité | Nombre | Sujets |
|---|---:|---|
| **P0 Bloquant** | **9** | Table, passages J1, retenue, retour d’énergie, rail, kit, commande, compilation et budget. |
| **P1 Critique** | **17** | Couple continu, main, pince, paliers de roulis, course et repérage, montage, axe et visserie, tensions et protection. |
| **P2 Important** | **5** | Stock, cohérence de version, reproductibilité, notice et qualification des butées. |
| **P3 Mineur** | **2** | Triangles historiques et volume nominal du profil Kobra 3. |
| **P4 Optimisation** | **2** | Masse, complexité, lots et consommables. |

[Suivi par identifiant historique](docs/diagnostic/latest/SUIVI_HISTORIQUE.md) · [Inventaire avec preuves, coûts, dépendances et validations](docs/diagnostic/latest/REGISTRE_PROBLEMES.md)

## 13. Wireframes et graphiques

Les cinq vues annotées proviennent des maillages des **corps Fusion réels**, transformés dans les poses mesurées. Les cotes des cylindres et points les plus proches proviennent des BRep. Les captures natives et les résultats JSON permettent de vérifier les annotations.

| Zone | Preuves |
|---|---|
| **Tangages et table** | [Projection cotée](docs/diagnostic/latest/wireframes/06_plan_table_annote.png) · [Capture Fusion aux butées basses](docs/diagnostic/latest/wireframes/02_fusion_butees_basses.png) |
| **Socle et passage des gaines** | [Séparation des raccords J1](docs/diagnostic/latest/wireframes/07_raccords_j1_annote.png) · [Capture du socle ouvert](docs/diagnostic/latest/wireframes/03_fusion_socle_j1.png) |
| **Arbres et paliers fendus** | [Coupes axiales cotées](docs/diagnostic/latest/wireframes/08_coupes_paliers_annote.png) · [Vue Fusion des deux roulis](docs/diagnostic/latest/wireframes/04_fusion_paliers_j2r_j3r.png) |
| **Paume, pince et commandes** | [Écart et points de contact les plus proches](docs/diagnostic/latest/wireframes/09_pince_annotee.png) · [Capture de la cassette et des doigts](docs/diagnostic/latest/wireframes/05_fusion_flexion_independante.png) |
| **Passages souples et carénages** | [Recouvrements au neutre](docs/diagnostic/latest/wireframes/10_passages_souples_annote.png) |

- [Radar de maturité](docs/diagnostic/latest/graphs/01_radar_maturite.png) et [notes par domaine avant/après](docs/diagnostic/latest/graphs/02_comparaison_notes.png).
- [Évolution P0 à P4](docs/diagnostic/latest/graphs/03_evolution_priorites.png) et [statuts des cas initiaux](docs/diagnostic/latest/graphs/04_statut_problemes.png).
- [Paniers chiffrés à périmètre commun](docs/diagnostic/latest/graphs/05_evolution_cout.png), [masses calculées en PETG plein](docs/diagnostic/latest/graphs/06_evolution_masse.png), [temps de tranchage disponibles](docs/diagnostic/latest/graphs/07_evolution_temps_impression.png), [préparation à la fabrication](docs/diagnostic/latest/graphs/08_preparation_fabrication.png).

## 14. Évaluation de maturité et préparation

La première grille attribuait quatre notes sur 25 par domaine. J’ai repris ses critères et paliers de preuve **0** absent, **5** hypothèse étayée, **10** spécification partielle, **15** preuve numérique utilisable, **20** sous-ensemble démontré ou préparation numérique complète, **25** validation à l’échelle recherchée. Les points intermédiaires reflètent la couverture. La moyenne passe de **37,7 r02** à **47,4 r03** puis **27,0 V5 roulis**. Les changements d’architecture font perdre des preuves de fabrication, d’assemblage et de commande qui existaient pour des branches antérieures. [Grille et notes r02](archives/r02/DIAGNOSTIC_ROBOT.md#15-maturité-technique-de-la-r02) · [Notes r03](archives/r03/RAPPORT_AMELIORATIONS_R03.md#comparaison-mécanique-et-maturité) · [Données des graphiques](docs/diagnostic/latest/donnees_graphiques.json)

| Domaine | r02 | r03 | V5 roulis | Sous-notes sur 25 et confiance |
|---|---:|---:|---:|---|
| Conception mécanique | 41 | 64 | **54** | 21 architecture, 19 mouvements, 9 tenue calculée, 5 préparation d’épreuve. Confiance élevée sur CAO, moyenne sur tenue. |
| Motorisation | 32 | 52 | **38** | 18 références, 15 couple et vitesse, 5 rendement/thermique, 0 service mesuré. Confiance moyenne. |
| Imprimabilité | 58 | 69 | **18** | 10 géométrie native, 0 plateaux V5, 8 matière et ajustements, 0 coupon physique. Confiance élevée. |
| Électronique | 38 | 45 | **27** | 10 schéma et broches, 12 implantation, 5 protections et faisceau, 0 montage. Confiance moyenne. |
| Alimentation | 23 | 28 | **22** | 11 source et bilan, 8 pointes, 3 défauts, 0 essai. Confiance élevée sur les hypothèses, faible sur le rail réel. |
| Assemblage | 48 | 59 | **27** | 8 séquence, 10 couloirs et outils, 9 quincaillerie, 0 assemblage. Confiance moyenne. |
| Logiciel | 39 | 28 | **16** | 5 cycle et compilation, 7 calibration, 4 défauts, 0 validation sur robot. Confiance élevée. |
| Intelligence artificielle | 8 | 8 | **8** | 8 architecture, 0 perception, 0 planification reliée, 0 exécution. Confiance élevée. |
| Sécurité | 18 | 29 | **20** | 11 risques et banc, 3 coupure et reprise, 6 défauts/limites, 0 essais. Confiance élevée sur les lacunes. |
| Maintenabilité | 39 | 54 | **21** | 7 démontage documenté, 10 accès CAO, 4 remplacement, 0 interventions répétées. Confiance moyenne. |
| Documentation | 71 | 85 | **46** | 14 inventaire, 6 notice active, 18 traçabilité, 8 cohérence et protocole. Confiance élevée. |

**Préparation à la fabrication · 17/100.** Cette nouvelle grille pondère **mécanique 4/20**, géométrie mesurable avec blocages, **kit V5 0/20**, **achats et budget 8/15**, une partie des lots et prix établie, **assemblage à blanc 5/15**, plusieurs accès mesurés, **alimentation et sécurité 0/20**, **commande opérationnelle 0/10**. Aucun score rétrospectif n’a été construit faussement sur ces critères. Un blocage critique empêche le passage quelle que soit la note. [Grille de préparation](docs/diagnostic/latest/graphs/08_preparation_fabrication.png)

## 15. Feuille de route avant fabrication

| Ordre | Pièces et corrections | Vérification de passage |
|---|---|---|
| **1 · P0 · Géométrie opérable** | Platine, tourelle, jonctions de gaines J1, routes J2R/J3R/J7, capot, chapes J2/J3 et garde au plan. | Rejouer la grille avec bras, main et fils, démontrer la course câblée, les arrêts et une enveloppe combinée avec marge. Reprendre les douze poses refusées. |
| **2 · P0/P1 · Retenue et capacité mécanique** | Disques, chapes, axes M5, arbres et chapeaux de roulis, dentures et ancrages. | Fixer la charge cible, comparer compensation et répartition des masses, éprouver retenue hors tension, jeu et moment en mesurant effort, température et vitesse. Bras captif et établi ancré. |
| **3 · P0/P1 · Énergie, arrêt et commande** | Pico et son boîtier, distribution, limiteurs, onze voies, état du rail et firmware. | Dimensionner avec les mesures du lot. Compiler pour la cible, prouver la coupure indépendante et le réarmement sans mouvement injustifié. |
| **4 · P0/P2 · Paquet et panier figés** | BOM des pièces, vis, bornes, plans, STEP/STL/3MF, notice d’atelier. | Concordance Fusion, exports et quantité. Confirmer un panier TTC livré **≤150 €** avec pièces de sécurité et stock réellement compatible. |
| **5 · P1 · Coupons et sous-ensembles** | 608, appuis fendus, axes, attaches imprimées, denture, paume et doigt. | Contrôler cotes, supports, filets et résistance, premier doigt instrumenté, roulements, efforts au palier, friction et maintenabilité. Qualifier avant impression générale. |
| **6 · P1/P2 · Intégration** | Bras complet ancré, commande locale puis PC. | Montage à blanc, essais axe par axe, cycle borné et essais de perte/retour d’énergie et communication. Démontrer charges et prises puis autonomie éventuelle. |

## 16. Verdict avant fabrication

| Question | Verdict |
|---|---|
| **Commander les composants ?** | **Différer le lot.** Recenser le stock et les références. Un achat de banc ne se justifie qu’après avoir défini l’essai qu’il doit lever, la cote à vérifier et son prix dans le panier. |
| **Imprimer certaines pièces ?** | **Coupons historiques d’étalonnage possibles** sur leur machine et leur profil, par exemple empreinte SG90 ou 608 r05. Préparer ensuite des coupons spécifiques à la V5. |
| **Imprimer le robot entier ?** | **Bloqué** par le kit V5 absent et les reprises géométriques ouvertes. |
| **Assembler ?** | **Montage général non qualifié.** Quelques couloirs à sec démontrés. Fils, vis, outils, séquence complète et démontage à établir. |
| **Moteurs suffisants ?** | **Non démontré.** J2 doit être repris ou qualifié avec compensation et le lot réel. J3 et les autres voies restent à éprouver en service continu. |
| **Doigts indépendants ?** | **Cinq voies séparées vérifiées en CAO.** Indépendance physique, rappel et variation avec J7 à éprouver. Pince mesurée à **17,68 mm** dans le meilleur cas sondé. |
| **Amplitude du socle suffisante ?** | **176° nominaux**, course câblée inconnue. La suffisance dépend d’une enveloppe d’usage définie et des quatre passages repris. |
| **Budget de 150 € respecté ?** | **Non démontré.** **149,48 €** dans le scénario hors filament. **161,43 €** avec une bobine, avant corrections et autres écarts. |
| **Supporter son poids et de petits objets ?** | **Non établi en fonctionnement.** À vide, la gravité dépasse les anciennes valeurs de retenue du bras. La charge de 10 ou 20 g constitue un cas de calcul et de banc, avec tenue, géométrie de prise, température et appui à qualifier. |
| **Corriger quoi avant fabrication ?** | Enveloppe au-dessus de la table, acheminement des câbles et tendons, retenue à la coupure, rail et réarmement, géométrie de pince et déposes critiques, fichiers et nomenclatures cohérents. |
| **Valider quoi physiquement ?** | Cotes et parois d’impression, portées et vis, montage complet à blanc, friction et fatigue, tendons et prise, couple et thermique, stabilité ancrée, arrêt, sous-tension et retour d’énergie. |

**Impression de série bloquée · Assemblage complet non qualifié · Motorisation sous charge non qualifiée · Mise sous tension du bras assemblé bloquée · Fonctionnement autonome bloqué.**
