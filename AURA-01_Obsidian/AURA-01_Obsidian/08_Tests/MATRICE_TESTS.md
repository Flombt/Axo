# Matrice de validation

## AURA-009 r04 — Fabrication et fonctionnement

| Contrôle | Résultat numérique | Suite |
|---|---|---|
| CAO articulée | 143 poses et 6 recontrôles locaux sans volume parasite au seuil 0,006 mm³. | Parcourir les mouvements au banc. |
| Gaines et tendons | 45 passages de gaine et 10 états de tendon exempts de contact au seuil retenu après reprise du majeur. | Mesurer traction et retour selon le roulis. |
| Impression | 53 maillages, 11 plateaux PETG, sept coupons. | Tester les ajustements et les supports avant les pièces de service. |

[[02_Conception_Fusion/TABLE_R04|Prototype de table r04]] · [Rapport de fabrication](../../../archives/r04/VALIDATION_FABRICATION.md).

## AURA-009 r03 v2 — Trajectoires de la démonstration

| Contrôle | Résultat vérifié le 24 novembre 2026 | Suite physique |
|---|---|---|
| Trajectoires Fusion | 143 poses distinctes par liaisons natives et par matrices exactes, sans interférence volumique détectée au seuil de 0,006 mm³. | Vérifier les courses, les jeux et la tenue de la retenue sous charge. |
| Raccordement du faisceau | 25 raccords sur 3 960 images Blender. Écart maximal inférieur à 0,0001 mm. | Mesurer les jeux des connecteurs, l’effort sur les attaches et la fatigue des fils. |
| Main à commande commune | Distance pouce–index de 43,82 à 17,68 mm entre les bouts. | Mesurer le chemin et la tension des tendons, puis tester l’opposition sur objet. |

[[04_Animation_Emotion/ANIMATIONS#AURA-009 r03 v2 — Démonstration cinématique|Démonstration r03 v2]] · [Rapport cinématique](../../../archives/r03/animations/RAPPORT_CINEMATIQUE.md).

## AURA-009 — Kit V3 r02

| Contrôle | Résultat vérifié | Suite physique |
|---|---|---|
| Fusion r02 · positions | 72 poses globales et 72 ciblées sans volume parasite détecté à 0,006 mm³. F3D réimporté avec 77 occurrences, 76 liaisons, 16 couplages. | Parcourir les positions avec fils réels et support de retenue. |
| Pouce et montage | Jeux mini 0,54 mm à la chape et 3,24 mm à la paume. 48 trajectoires et 598 positions. Deux emboîtements des segments contrôlés en plus. | Monter à blanc l’index, la chape et le pivot J3. Contrôler les vis et écrous du lot. |
| Tranchage | 20 STL, 5 plateaux PrusaSlicer, 29 pièces de robot. 15 phalanges tranchées sans supports. | Contrôler diamètre des axes, retrait des supports et tenue des couches. |
| Électronique et logiciel | Schéma 5 V et compilation Nano pour les deux profils ATmega328P. | Câbler, mesurer les chutes de tension, tester la coupure et calibrer. |

[[02_Conception_Fusion/MONTAGE_V3|Dossier r02 et mesures]].

La liste détaillée T-001 à T-054 est dans le [[README#29 — Plan de validation : fiches de tests falsifiables|plan de validation]]. Voir la [[09_Gestion/ROADMAP|roadmap]] pour les phases et le [[09_Gestion/JOURNAL|journal]] pour les preuves de session.

## Règles de preuve

- `VALIDÉ` = date, version, environnement, résultat vérifié et capture/mesure.
- `BLOQUÉ` si une dépendance manque.
- Réexécuter les tests concernés après modification d'un pivot ou d'une pièce.

## Premiers tests bloquants

- Les premiers tests couvrent l’inventaire Fusion (T-001), l’historique paramétrique (T-002), la base fixe (T-004), les joints (T-006 à T-011), HOME (T-014), le repli (T-015), les exports 3MF (T-027) et STL (T-028) et le MCP (T-053).

| Test | Révision | Date | Statut | Preuve |
|---|---|---|---|---|
| T-001 | Assemblage final v5 | 2026-11-21 | VALIDÉ | Huit pièces et leur rôle, huit solides. [[02_Conception_Fusion/audit_initial#Inventaire et état de la géométrie]] |
| T-002 | Assemblage final v5 | — | À_FAIRE | Historique lu. Propagation d’une cote à tester sur une copie. |
| T-003 | Assemblage final v5 | 2026-11-21 | EN_COURS | Ø96 mm et entraxe épaule–coude 100 mm mesurés. Comparaison finale aux cotes maîtresses à établir. [[02_Conception_Fusion/audit_initial#Écarts au cahier des charges]] |
| T-004 | Assemblage final v5 | 2026-11-21 | VALIDÉ | Base fixée au parent et immobile sur 46 poses. [[02_Conception_Fusion/audit_initial#Articulations et mouvements mesurés]] |
| T-005 | Assemblage final v5 | 2026-11-21 | VALIDÉ | Liaison et surfaces de centrage coaxiales selon Z. Jeu radial CAO 0,30 mm. [[02_Conception_Fusion/audit_initial#Jeux fonctionnels et risques FDM]] |
| T-006 | Assemblage final v5 | 2026-11-21 | EN_COURS | Butées −80° et +80° atteintes. Volume d’interférence nul sur les poses testées. Balayage continu à faire. |
| T-007 | Assemblage final v5 | 2026-11-21 | BLOQUÉ | Poses −32° à +21° échantillonnées. Contrôle du câble bloqué par l’absence de faisceau modélisé. |
| T-008 | Assemblage final v5 | 2026-11-21 | EN_COURS | Poses −38° à +18° et butées combinées contrôlées. Balayage continu à faire. |
| T-009 | Assemblage final v5 | 2026-11-21 | BLOQUÉ | Liaison avant-bras–poignet rigide. Inclinaison J4 à concevoir. |
| T-010 | Assemblage final v5 | 2026-11-21 | BLOQUÉ | Liaison avant-bras–poignet rigide. Roulis J5 à concevoir. |
| T-011 | Assemblage final v5 | 2026-11-21 | ÉCHEC | Course CAO 27 mm mesurée. La cible des deux doigts mobiles synchronisés reste à atteindre avec un doigt actuellement fixe. |
| T-014 | Assemblage final v5 | — | À_FAIRE | Retour au neutre dans la session vérifié. Rappel HOME après réouverture à tester. |
| T-051 | Assemblage final v5 | 2026-11-21 | VALIDÉ | Archive F3Z contrôlée, importée et ouverte dans Fusion dans un dossier séparé avec ses huit références indépendantes. [[02_Conception_Fusion/CONCEPTION_MECANIQUE#Restauration et indépendance]] |
| T-053 | Assemblage final v5 | — | À_FAIRE | Connexion MCP prouvée par les lectures et le pilotage. Création du cube selon le protocole à faire dans un document temporaire. |
| T-052 | Coffre après AURA-001 | 2026-11-21 | VALIDÉ | [[09_Gestion/JOURNAL#2026-11-21 — Mise en place de la mémoire Obsidian]] |

## V2 — Contrôles de la conception mécanique

Révision v5 du 21 novembre 2026, Autodesk Fusion 2706.1.17. Les résultats numériques sont circonscrits aux configurations et aux gabarits contrôlés dans la [[02_Conception_Fusion/CONCEPTION_MECANIQUE#V2 — Prototype mécanique enregistré|note mécanique]].

| Test | Statut | Résultat et suite |
|---|---|---|
| T-001 | VALIDÉ | 46 occurrences, 35 définitions, 40 pièces solides et 6 réserves, 45 liaisons. |
| T-002 | VALIDÉ | Jeu radial et paroi recalculés. Hausse du diamètre de trois familles d’alésages et du volume de coque lors du test. Nominal rétabli. |
| T-003 | VALIDÉ | Socle hérité Ø96 mm, entraxe J2–J3 de 100 mm sur le modèle Fusion. Les dimensions cibles du cahier des charges restent provisoires. |
| T-004 | VALIDÉ | Socle immobile pendant l’ensemble des 226 configurations. |
| T-006 à T-010 | EN_COURS | Butées et combinaisons échantillonnées de J1 à J5. Aucun conflit volumique aux états testés. Balayage continu et faisceau à contrôler. |
| T-011 | VALIDÉ CAO | Les deux mors mobiles ont des courses opposées 1:1 et une ouverture entre garnitures de 1,60 à 25,60 mm. Transmission et effort à tester physiquement. |
| T-014 et T-015 | VALIDÉ CAO | HOME vérifiée après réouverture, Peur testée comme pose repliée. Les huit références sont conservées dans les attributs Fusion. |
| T-016 à T-020 | EN_COURS | Masse et couples statiques calculés pour un scénario de charge de 100 g. Projection du centre au-delà du socle. Vérifier masses réelles, maintien et dynamique. |
| T-021 à T-023 | EN_COURS | Gabarits d’accès J1, J4/J5, G1 et coques testés. Dépose du support d’actionneur pour extraire J4. Essais de tenue, montage et outils réels à faire. |
| T-024 à T-026 | BLOQUÉ | Échancrures et conduit pour câbles modélisés. Faisceau, rayons de courbure et torsion à définir. |
| T-027 et T-030 | EN_COURS | 21 exports 3MF. Millimètres, fermeture, arêtes et cotes des maillages contrôlés. Import dans le slicer et surplombs à vérifier. |
| T-033 à T-036 | À_FAIRE | Imprimer les coupons de pivots et de glissières, faire un montage à blanc, tester endurance et température. |
| T-037 à T-041 | EN_COURS | Six gestes et dix transitions échantillonnés. Reproduction motorisée et lisibilité à évaluer. [[04_Animation_Emotion/ANIMATIONS#V2 — Poses de référence]] |
| T-053 | EN_COURS | Le MCP a importé, modélisé, piloté, analysé, exporté, sauvegardé puis rouvert le document V2. Le scénario spécifique du cube temporaire reste à exécuter. |

## AURA-004 — Essais de la branche motorisée

Révision v3, 21 novembre 2026, Fusion 2706.1.17 et PrusaSlicer 2.9.6. Le statut physique AURA-004 demeure **EN COURS**.

| Contrôle | État et preuve | Étape physique restante |
|---|---|---|
| T-001, T-004, T-014 et T-051 | Copie indépendante enregistrée et rouverte à HOME, 75 occurrences, 74 liaisons et 3 liens de mouvement. Révision V2 d’origine v5 et six versions liées vérifiées. | Ancrage et procédure HOME avec position de sortie. |
| T-009 à T-012 | Rotation J4 et J5 et course G1 contrôlées sur les poses. Entraînements J5 (−42° → +18°) et G1 (2 mm/mors/tour sur commandes incrémentales) vérifiés par le solveur. | Vérifier dentures et filets, serrage, maintien en prise, effort/limitation G1 et jeu. |
| T-016 à T-023 | Centres de masse, moments et réactions d’ancrage calculés. Plaque, quatre ancrages et accès démontables modélisés. | Éprouver rigidité et tenue des fixations, contrôler paliers, retenue hors tension, accessoires constructeur et démontage. Tester J2/J3 en charge avec appui mécanique. |
| T-024 à T-026, T-035 et T-036 | Réserves de passage documentées. Aucune qualification du faisceau ni du moteur en température. | Éprouver torsion et frottement, le jeu à chaud et le cycle thermique à l’effort requis. |
| T-027, T-030 et T-031 | 21 fichiers de référence, dix révisés/nouveaux et cinq coupons acceptés en tranchage virtuel. Les 15 nouveaux maillages sont fermés et exprimés en millimètres. | Valider la préparation avec la machine et le matériau réels, l’accès aux supports et l’échelle mesurée. |
| T-032 à T-034 | Cinq coupons 3MF et leur source Fusion dans le dossier de fabrication. | Au moins trois répétitions par profil, puis mesure de répétabilité, jeu opérationnel et essais des inserts après refroidissement. |
| T-037 à T-041 | Neuf configurations repères dont HOME et étendue. Dix transitions, 99 états distincts, sans interférence volumique aux points vérifiés. Butées J2 remises après essai. [[04_Animation_Emotion/ANIMATIONS#AURA-004 — Démonstration de la branche motorisée]] | Tester les gestes à vide, les passages de câble et la répétabilité, puis mesurer le suivi motorisé. Les zones entre échantillons restent à vérifier après modifications. |
| T-042, T-044, T-048 et T-050 | Architecture d’arrêt et programme de mise en service documentés. Vidéo CAO disponible. | Tester coupure, absence de redémarrage, récupération, maîtrise de la chute de J2/J3 et lisibilité des mouvements. |

### Reprise du 22 novembre 2026

| Contrôle | Preuve obtenue | État de la suite |
|---|---|---|
| T-001 et T-051 | Ouverture dans Fusion et export F3Z achevé. Le manifeste de l’archive lisible confirme la v3 et deux références v2. [[02_Conception_Fusion/CONCEPTION_MECANIQUE#AURA-004 — Assemblage de travail motorisé|Archive et empreinte]] | Test de réimport de l’archive locale à faire le jour où une restauration est requise. MCP Fusion indisponible pendant cette reprise. |
| T-027 et T-030 à T-034 | Cinq objets à l’échelle 1:1 sur un seul plateau virtuel, profil PETG relu, tranchage complet et orientations des perçages vérifiées sur les maillages. [[03_Impression_3D/PROTOCOLes_FDM#Plateau virtuel des cinq coupons|Projet de tranchage]] | Contrôler le profil réel, l’accès au retrait des supports, la répétabilité et les jeux sur coupons physiques. |
| T-016 à T-023 | Références de palonnier J1–J3 confirmées sur les fiches constructeur. [[05_Electronique/NOMENCLATURE_AURA004#Palonniers J1–J3 à vérifier au montage|Références et relevés]] | Reprendre les empreintes et l’engagement des vis. Qualifier l’ancrage, la retenue gravitaire et le couple utile. |

### Mesure du couple utile de J2 et J3 au banc

Sur un montage d’essai ancré et retenu mécaniquement, prendre un bras de levier perpendiculaire au dynamomètre. Tarer le levier et vérifier le rayon au centre de l’axe. La conversion de contrôle est `F = T / r`. Avec un rayon effectif de 100 mm, les cibles de dimensionnement se traduisent ainsi.

| Axe | Maintien, équivalent de la charge statique calculée | Cible de dimensionnement à la vitesse de travail |
|---|---|---|
| J2 | 7,38 N pour 0,738 N·m | 12,53 N pour 1,253 N·m à 4 tr/min |
| J3 | 3,90 N pour 0,390 N·m | 6,79 N pour 0,679 N·m à 5 tr/min |

Augmenter l’effort progressivement et relever le couple tenu, la vitesse, l’erreur au joint, le courant et la température jusqu’au cycle de travail visé. Vérifier ensuite la retenue mécanique à la coupure et la reprise après réarmement manuel avant les mouvements du bras assemblé. Ces efforts sont des cibles calculées au joint. La tenue et l’échauffement restent des mesures à effectuer.

## V3 — Contrôles du bras à main articulée

Fusion 2706.1.17, révision locale r02 du 22 novembre 2026. Relevés dans `Exports_Fusion/AURA_V3/Verification_CAO.json` depuis la racine Aura.

| Contrôle | Vérification effectuée | Suite ouverte |
|---|---|---|
| 7 pivots du bras et 15 pivots des doigts | Commande native isolée de 8° par axe et mesure du point témoin. Variation nulle des autres angles à la précision du relevé. | Définir les limites en présence des câbles et de la quincaillerie réelle. |
| 15 logements de servos | Analyse Fusion boîtier contre châssis pour les quinze phalanges. Aucun volume d’intersection détecté sur ces paires. | Montage du palonnier et de la bague, jeu et tenue des fixations après FDM. |
| Trois mouvements | Roulis, flexion des cinq doigts puis mouvement des trois segments capturés dans Fusion. MP4 décodé intégralement. | Vérifier la fluidité en charge et les collisions entre les composants sur les trajectoires. |
| Tenue à l’horizontale | Estimation des moments à vide et comparaison au couple nominal du servo de doigt. [[02_Conception_Fusion/DESIGN_V3#Limites et dimensionnement d’atelier|Hypothèses]] | Mesurer les masses, le couple continu, la température, l’arrêt et la retenue gravitaire. |

## V3 r03 — Assemblage et impression

Révision du 22 novembre 2026. Autodesk Fusion 2706.1.17 et PrusaSlicer 2.9.6. Relevés dans `Exports_Fusion/AURA_V3/Fabrication_r03/Verification_FDM_r03.json` depuis la racine Aura.

| Contrôle | Preuve de la r03 | Suite physique |
|---|---|---|
| Intégrité et nombre de pièces | Export F3D rouvert avec 23 occurrences et 22 pivots. Onze géométries imprimables monoblocs. | Assemblage à blanc et relevé des jeux. |
| Interférences | 13 paires de corps de composants distincts en interférence à HOME sur r02. Pour r03, aucun volume d’intersection supérieur à 0,001 mm³ dans 165 poses échantillonnées, 41 corps contrôlés. | Contrôler les collisions avec vis, paliers et fils en place, et les mouvements entre échantillons. |
| Préparation FDM | 11 STL en millimètres fermés et connectés. Six 3MF retranchés, 23 pièces au total. Supports détectés uniquement pour le segment distal. | Qualifier la machine, le PETG, l’ajustement des axes et l’orientation pour les efforts réels. |
| Premier doigt | Poches accessibles et jeux nominaux documentés dans le [[03_Impression_3D/PROTOCOLes_FDM#AURA V3 r03 — Kit d’impression|kit]]. | Mesurer masse, tenue latérale, libre flexion, effort et température avec le servo et son vrai palonnier. |

## AURA-006 — Révision mécatronique

| Essai | Preuve actuelle | Critère suivant |
| --- | --- | --- |
| Doigt, chaîne cinématique | Les trois actionneurs déplacent chacun leur témoin de 2,372 mm pour 8°. Dix-huit poses de la plage 0–45° et trois poses à 47° sans interférence mesurée. Contact à 53° sur chaque butée | Contrôler jeu, force et température sur le premier doigt monté |
| Épaule, rapport | Les pivots répondent à 4:1. Treize poses de service en 0–60° et trois retours sans collision détectée. Butées détectées à −7° et +69° | Mesurer jeu, tension de courroie et échauffement sur banc ancré |
| Épaule, maintien en cas de coupure | Calcule 5,68 N·m statiques et vise 8,22 N·m au dimensionnement. Frein aval candidat de 16 N·m nominaux | Tenue continue, retard du frein et chute angulaire mesurés en charge |
| Dépose | Les trois KST sur leur banc, le carter et le moteur J2 ont des translations d’extraction dégagées aux positions échantillonnées | Vérifier accès réel des outils, connecteurs et jeux après assemblage |
| Fabrication | 14 STEP et 14 3MF, G-code généré pour les 14 en tranchage virtuel | Coupon, métrologie, ancrage et essais matière |
| Main à 15 KST, implants et faisceau | Huit poses de la main sans collision détectée. 67 contacts OEM externes à HOME. Rayons trop serrés sur les 42 combinaisons de boucle et de pose testées | Corriger les interfaces et augmenter la place pour les câbles. Valider les trajectoires continues |
| Batterie et calcul embarqué | Pack candidat, bilan de puissance et volumes de CAO | Rails, chute de tension, redémarrage, échéances de sécurité et autonomie mesurés |

[[02_Conception_Fusion/INTEGRATION_MECATRONIQUE_V3|Preuves et états détaillés]] · [[03_Impression_3D/NOTICE_BANCS_V3|Protocoles physiques]].

## AURA-007 — Bras de table r01

| Contrôle | Résultat | Vérification physique restante |
|---|---|---|
| Articulations et sauvegarde | Archive rouverte avec 19 occurrences et trois pivots. Un déplacement de 5° sur chacun entraîne son témoin de 1,919 mm, sans dérive mesurée des autres angles. | Caler le neutre et les limites des trois MG90S reçus. |
| Volumes et accessibilité | 62 poses échantillonnées dans Fusion avec les enveloppes moteurs, sans intersection détectée au seuil de 0,006 mm³. | Mesurer le jeu réel et inspecter les courses avec les vis et les fils. |
| Fabrication | Neuf maillages fermés et connectés, trois 3MF PETG tranchés. | Vérifier la machine de l’atelier, les supports et la répétabilité des axes. |
| Épaule et coude | Estimation à vide de 0,0552 N·m à J2 et de 0,0327 N·m à J3. | Mesurer tenue, courant et chauffe au banc. Fixer la platine puis lancer un geste à vide. |

[[02_Conception_Fusion/PROTOTYPE_TABLE#Maquette de présentation r01|Maquette et relevés]].

## AURA-008 — Main à tendons et roulis du poignet

| Contrôle | Résultat CAO | Essai physique suivant |
|---|---|---|
| Phalanges et transmission | 15 pivots de doigt et la traverse répondent au mouvement du tambour. 16 couplages relus dans le F3D. | Régler un doigt, mesurer les débattements et la réouverture, puis régler les cinq tendons ensemble. |
| Roulis et interférences | 72 poses sans interférence volumique détectée, dont roulis à ±36° et fermeture. | Vérifier les câbles et les jeux sur un montage à blanc. |
| Impression | 17 STL fermés et connectés. 26 pièces tranchées sur trois plateaux avec supports. | Vérifier les axes Ø2 mm, les guides et les trous de rappel après impression. |
| Tenue à vide | 0,1204 N·m estimé à l’épaule et 0,0829 N·m au coude sur les poses CAO, PETG plein. | Mesurer le courant, le maintien et l’échauffement du MG90S de coude. |

[[02_Conception_Fusion/MAIN_POIGNET_ECO|Archive et résultats de la révision]].
