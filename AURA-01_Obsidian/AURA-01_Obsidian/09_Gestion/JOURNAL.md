# Journal des sessions

## 2026-11-25 — Stabilisation et contre-audit AURA-01

- Enregistré **AURA-01 V5 · Stabilisation** v2 dans Fusion. L’archive réouverte compte 143 occurrences, 18 liens de mouvement et 27 pivots actifs. Le STEP réimporté livre 156 solides fermés. La V5 roulis originale reste restaurable depuis son tag. [Preuve Fusion](../../../docs/diagnostic/corrections/fusion_sauvegarde.json) · [Archives](../../../archives/README.md)
- Fixé J2R/J3R, passé le faisceau au centre de J1, intégré les rehausses de 90 mm, les butées et les ressorts. Validé numériquement la dépose de J2 en deux mouvements, de J3 après le support démontable et de J7 après la cassette. La garde géométrique calculée vaut 8,68 mm aux butées. La pince passe de 17,68 à 3,70 mm à la fermeture échantillonnée. [Rapport des corrections](../../../RAPPORT_CORRECTIONS.md)
- Rejoué 153 identifiants dans Fusion. Le solveur en atteint 141 à 0,02°. Trois combinaisons à J1 extrême et J7 ±32° expliquent douze refus. Les contre-poses des solides positionnés indépendamment retrouvent seulement les deux engagements M4 prévus. [Campagne finale](../../../docs/diagnostic/corrections/campagne_finale.json) · [Contre-poses](../../../docs/diagnostic/corrections/contreposes_brep.json)
- Livré 54 références STL/3MF et 15 projets pour Kobra 3, Kobra X et Kobra 3 Max. Relu les 108 exports et tranché 17 plateaux. Le firmware neuf voies passe neuf essais hôte et trois compilations MicroPython. [Fabrication](../../../manufacturing/README.md) · [Firmware](../../../firmware/README.md)
- Compté le filament fourni à 0 €. Le scénario atteint 188,74 € TTC avec provisions, avant le devis d’intégration. Restent le panier à 150 € et les essais physiques de montage, de retenue et de coupure. [Nomenclature](../../../purchases/NOMENCLATURE.md) · [Montage](../../../assembly/README.md)

## 2026-11-24 — Actualisation du tableau GitHub Axo

- Tableau public mis à jour avec sept cartes. Trois jalons datés expliquent les versions r02 à r05 et renvoient aux fichiers publiés.
- La carte V5 rassemble les problèmes du diagnostic et les corrections en cours. Les étapes suivantes couvrent le budget des essais, les premières impressions 3D et la validation sur un premier montage. [Tableau Axo](https://github.com/users/Flombt/projects/3)

## 2026-11-24 — Visserie disponible et devis r04

- Comparaison des six photos de quincaillerie avec la nomenclature et les volumes de fixation du document Fusion v4. Réemploi des M2×12 et écrous M2 après essai. Les vis M2×10 et les petites têtes J1/J2/J3 demandent une présentation sur pièces.
- Devis daté pour les neuf moteurs, les roulements, le câblage et l’alimentation. Les EZO sont des candidats à tester sur les portées. Le premier doigt se monte avec un seul KST avant la série. Les pièces à usiner, le collecteur et le chariot de cartes restent à chiffrer ou à qualifier. [Visserie et liste d’achats r04](../../../archives/r04/achats/README.md).

## 2026-11-24 — Planches couleur Anycubic r04 pour clé USB

- Export Fusion v4 vérifié. Les 53 STL sont convertis et contrôlés en 3MF, à l’échelle millimétrique. Les cinq planches couleur couvrent 61 pièces et une planche rassemble les sept coupons.
- Six planches rouvertes et retranchées dans Anycubic Slicer Next 2.0.0.3. Le préréglage de référence est Kobra 3 Max, buse 0,4 mm. Le support de cartes J1 reste isolé avant son ajustement physique.
- Les 59 fichiers sont disponibles à plat dans le dossier `miroir USB historique` à la racine du projet. [Guide des 3MF par couleur](../../../archives/r04/anycubic/README.md).

## 2026-11-24 — Fabrication et nouvelle cinématique r04

- Instantané de la r03 v3 préservé. Nouveau document [[02_Conception_Fusion/TABLE_R04|Prototype de table r04]] enregistré en v4. F3D réimporté avec 187 occurrences et STEP de 311 solides.
- Déport de cinq KST, cinq gaines et tambours indépendants. J1 porté, entraînement 88/20 et collecteur. Le dégagement sous la paume écarte le contact du majeur en roulis négatif.
- 143 poses et six recontrôles ciblés, 45 essais de gaines et dix de brins, neuf corridors de dépose après ouvertures locales. 53 STL et 11 plateaux PETG tranchés sans avertissement. Retours, efforts et protections à valider physiquement.
- Ajout des vidéos à caméra fixe et de la main, rendus, rapport et fichiers de fabrication. [Rapport de fabrication](../../../archives/r04/VALIDATION_FABRICATION.md) · [Commit d61135d](https://github.com/Flombt/Axo/commit/d61135dd10a30e44230460528a4378c2e916fc7e) · [Release GitHub](https://github.com/Flombt/Axo/releases/tag/aura-009-r04-fabrication).

## 2026-11-24 — Démonstration cinématique AURA-009 r03 v2

- Instantané de l’onglet actif Fusion exporté et réimporté en copie de travail, avec 145 occurrences, 148 liaisons, 16 couplages et 251 solides visibles. La reconstruction Blender conserve la géométrie, les commandes et les guides du faisceau.
- Fusion a contrôlé 143 poses, par ses liaisons puis avec les matrices exactes de l’animation. Aucune interférence volumique détectée au-dessus de 0,006 mm³ sur ces échantillons. Les 25 raccords ont été vérifiés sur 3 960 images Blender. La distance pouce–index passe de 43,82 à 17,68 mm en CAO.
- Prévisualisation vérifiée puis rendu 4K sur RTX 5070 Ti. Après une déconnexion du pilote OpenGL, reprise des images restantes sous Vulkan. Les quatre vidéos, le projet Blender, la couverture et le rapport sont sauvegardés. [[04_Animation_Emotion/ANIMATIONS#AURA-009 r03 v2 — Démonstration cinématique|Démonstration r03 v2]] · [Rapport cinématique](../../../archives/r03/animations/RAPPORT_CINEMATIQUE.md).
- README, rapport et couverture publiés sur main. Les quatre MP4 et le projet Blender ont été contrôlés dans la Release. [Commit 0c74d78](https://github.com/Flombt/Axo/commit/0c74d78865ef246c0c8c2362aadc8b54ae2693c1) · [Film, extraits et projet Blender sur GitHub](https://github.com/Flombt/Axo/releases/tag/aura-009-r03-v2-cinematique).

## 2026-11-23 — Faisceau de la r03, Fusion v2

- Le déplacement du bras avait mis en évidence des arcs d’essai rigides visibles hors de leurs attaches. L’état avant retouche est conservé séparément. Le modèle principal r03 v2 remplace ces volumes par quatre guides mobiles, 12 pivots de faisceau, huit attaches et six colliers. Une fenêtre de fiche J3 et un passage de câble J7 sont usinés dans la CAO.
- Les 25 interfaces restent alignées et les 59 poses réimportées sont exemptes d’interférence au seuil retenu. Les 72 poses du pouce, les butées et 149 positions de dépose ont été rejouées. Inspection sur 16 vues Fusion avec les deux configurations combinées aux limites.
- F3D réimporté avec 145 occurrences et 148 liaisons, STEP réimporté avec 251 solides et version Fusion v2 complète. Le dimensionnement des conducteurs, la tenue des colliers et la fatigue sous torsion restent à qualifier. [[02_Conception_Fusion/TABLE_R03|Fichiers et preuves]].

- Publication de la r03 corrigée sur main. Le lot et les dossiers historiques ont été vérifiés après le push. [Commit ec2abbd](https://github.com/Flombt/bras-robotique/commit/ec2abbde9c5103ec50d0bb93d371c3885fdda637)

## 2026-11-23 — Refonte AURA-009 de table r03

- Connexion Fusion MCP locale opérationnelle. La r02 ouverte en mode récupéré a été archivée avant intervention. La r03 **AURA-01 — V3 de table — AURA-009 r03** a été enregistrée dans son propre document, Fusion v1, puis réimportée depuis F3D et STEP.
- Reconstruction des supports et arbres J2/J3, des butées et retenues, de la platine, de J7 et de la traverse à cinq réglages. J3 passe au XC330-M288-T. Le logiciel de commande et les réglages physiques restent à qualifier.
- 59 poses globales et 72 poses du pouce sans interférence signalée. Six corridors de démontage, 149 positions, sans contact sur les paires sélectionnées. Le passage STEP a réussi après mise à disposition de la version enregistrée. Le dernier tranchage des sept 3MF PETG n’a produit aucun avertissement.
- Les sources, empreintes, rendus, fichiers d’atelier et limites sont regroupés dans la [[02_Conception_Fusion/TABLE_R03|note r03]]. Le premier montage vise les coupons et le banc ancré.

## 2026-11-23 — Tableau GitHub de conception Axo

- Tableau renommé « Axo — Conception du bras robotique », avec un court résumé du bras. Quatre cartes présentent la modélisation en cours, puis les commandes, les pièces à imprimer et la finalisation après les essais de montage.
- Cartes à faire précisées dans GitHub Projects. Imprimer les pièces du bras en 3D après les premiers essais, puis suivre la validation du design final dans une carte dédiée.
- Tableau vérifié depuis le dépôt public bras-robotique. Le tableau lui-même est privé. [Tableau Axo](https://github.com/users/Flombt/projects/3)
- Visibilité du tableau passée en public à la demande de Florian. Accès anonyme vérifié sur la vue Backlog et sur les cartes de conception.

## 2026-11-23 — Axo sur GitHub

- Publication de 42 images, une vidéo de démonstration et 20 STL du kit r02. Les copies ont été vérifiées par empreinte. Le commit [993370f](https://github.com/Flombt/bras-robotique/commit/993370fc9e7fa9456cae99fc2b786ea0cf98a299) a été confirmé sur main.
- Le dépôt est privé. La soumission nécessite un dépôt personnel public et demande aussi un lien GitHub Project.

## 2026-11-23 — Audit d’achat et panier r02

- Réouverture de **AURA-01 — V3 articulée — Montage r02** v1 via le MCP Fusion. Inventaire en lecture seule de 77 occurrences et 20 pivots, avec mesure de la platine, de la bride J7 et des interfaces de la main. Fusion signale le document enregistré sans modifications.
- Le panier Amazon.fr contient 24 offres AURA-01 vérifiées pour **177,47 €** hors frais éventuels. Les moteurs TowerPro sont chiffrés séparément. L’alimentation, la protection et les fixations à valider sont renseignées. Aucun achat ni paiement effectué. [Relevé et capture](../../../archives/r02/kit/ACHATS_AMAZON_R02.md)
- Relevé d’achat ajouté au kit. Liens mis à jour dans les README du kit et des achats, la note de montage, les tâches et les décisions. Qualifier en atelier les pattes, les vis, le renvoi du pouce, le faisceau et l’alimentation avant de compléter les achats.

## 2026-11-23 — Présentation animée du bras dans Blender

- Six clips tirés des poses de la démo Fusion r02, avec 174 poses échantillonnées et 30 s de lecture à 24 images/s. Trois cadrages suivent le bras, le poignet et la main.
- Intégration dans la scène Blender ouverte et sauvegarde séparée dans [la version de présentation](../../../archives/r02/kit/AURA-01_Bras_Robotique_r02_Presentation.blend). Les positions et la mise à l’échelle de la scène ont été conservées. Comparaison de 19 images-clés, de leurs 1 463 transformations et vérification des gros plans et de la lecture dans Blender.

## 2026-11-23 — Dossier de montage à la racine et ouverture dans Blender

- Le kit r02 est regroupé dans [AURA-01_Notice_Montage](../../../archives/r02/kit/README.md). Les fichiers ont été vérifiés par rapport à l’archive source. Le README du projet et la note de montage pointent vers ce dossier.
- [Copie Blender](../../../archives/r02/kit/AURA-01_Bras_Robotique_r02.blend) issue du document Fusion enregistré r02, version 1. Les 77 composants et 94 maillages reprennent la pose de référence et les six apparences. Le fichier a été ouvert et son affichage vérifié dans Blender 5.2.1 LTS.
- Les superpositions de la vue Blender ont été réactivées et l’échelle de la grille a été réglée à 0,1. Le contour de la phalange sélectionnée a été contrôlé dans la fenêtre ouverte. Les réglages ont aussi été vérifiés à la réouverture du fichier du kit.

## 2026-11-22 et 23 — AURA-009 · Kit V3 r02

- Le nouveau document r02 est enregistré en version 1 et synchronisé dans Fusion. L’original r01 a été conservé. Réouverture de l’archive F3D contrôlée et export STEP réalisé.
- Sur la r01, aucune collision volumique n’a été reproduite dans les dix poses de pouce sondées. L’intervalle minimal de 0,27 mm justifiait de revoir le raccord. Chape, retenue d’axe, guide de renvoi et accès de maintenance repris dans la r02.
- Vérification r02 dans Fusion. 72 poses globales et 72 poses locales pouce/index sans interférence au seuil retenu. 48 chemins de pose ou d’outil et 598 positions. Approche des segments dans leurs chapes vérifiée à pas de 0,5 mm. Les poses combinées sont échantillonnées.
- 20 STL et cinq 3MF tranchés dans PrusaSlicer 2.9.6. Les orientations d’impression révisées donnent 236 et 56 mm² d’appui direct pour les segments 2 et 3. Le coupon et l’index restent les premiers essais matériels.
- Programme compilé pour les deux variantes AVR Nano. Vidéo de démonstration capturée sur l’archive Fusion r02. Aucun essai de câblage ou de fonctionnement sur le robot.
- Le [[02_Conception_Fusion/MONTAGE_V3|dossier r02]] rassemble les archives, mesures, notice illustrée, manuel, inventaire et dépannage. Le tableau de bord, la cible active, les décisions, les tâches et la matrice ont été actualisés.

## 2026-11-21 — Initialisation documentaire

- README maître établi d'après le cahier des charges utilisateur et la capture Fusion.
- Projet initial visible ; aucune inspection directe du fichier CAO, simulation ou impression réalisée par cette rédaction.
- Concept de travail AURA-01 proposé.
- Notes Obsidian créées ; aucune connexion MCP ni modification Fusion effectuée ici.

## 2026-11-21 — Mise en place de la mémoire Obsidian

- **Périmètre** — Coffre local `Aura/AURA-01_Obsidian/AURA-01_Obsidian`. Lecture et écriture confirmées sur le disque.
- **Modifications** — Ajout des [[AGENTS|règles Codex]] dans le coffre et d’un renvoi dans l’espace de travail `Aura`. Réorganisation du [[00_DASHBOARD|tableau de bord]], des liens entre les notes et des groupes de la vue Graphe. Mise à jour des consignes de démarrage et création du [[09_Gestion/TACHES|suivi des tâches]].
- **Vérifications sur disque** — 194 liens locaux résolus, dont 26 renvois à des sections et 2 liens vers la capture. Les 20 notes sont accessibles depuis le tableau de bord. Le diagnostic local de Codex a chargé `AGENTS.md` depuis `Aura` et depuis la racine du coffre.
- **Essai Obsidian** — Ouverture du coffre de travail dans Obsidian 1.15.1 sous Windows. Le lien du tableau de bord ouvre le suivi des tâches, puis le renvoi Phase 0 ouvre la bonne section de la roadmap. Les cinq groupes colorés apparaissent dans la vue Graphe. T-052 est consigné dans la [[08_Tests/MATRICE_TESTS|matrice de validation]].
- **Accès au coffre** — Obsidian affichait une copie téléchargée du même nom. La racine du coffre de travail a été ajoutée dans une nouvelle fenêtre, avec ses propres réglages locaux.
- **Fusion** — Le MCP a renvoyé la commande active via une requête en lecture seule. La Phase 0 d’audit et de sauvegarde est à reprendre lors d’une session CAO.
- **Décision et suite** — [[09_Gestion/ADR#ADR-005 — Mémoire et suivi dans le coffre Obsidian|ADR-005]] et [[09_Gestion/TACHES#AURA-002 — Auditer et sauvegarder Assemblage final|tâche AURA-002]].

## 2026-11-21 — Phase 0 Fusion et sauvegarde v5

- **Document ouvert** — `Robotic Arm — V1 / Assemblage final` v5, dans Fusion 2706.1.17. MCP connecté. Autodesk Assistant visible.
- **Sauvegarde** — Export F3Z dans `Sauvegardes_Fusion/AURA-01_Assemblage-final_source-v005_2026-11-21.f3z`. Neuf F3D correspondant au manifeste, références et CRC contrôlés. La première tentative par l’API avait produit un F3D du document principal seul. L’export natif a fourni l’archive distribuée.
- **Contrôles** — Huit solides, sept liaisons telles que construites et quatre mouvements A1–A4 pilotés. 46 poses contrôlées par interférence Fusion. Jeux des pivots, de la bride et du guide relevés. Voir l’[[02_Conception_Fusion/audit_initial|audit complet]] et la [[assets/fusion_audit_v005_2026-11-21.png|capture v5]].
- **État de Fusion en fin d’essai** — Position neutre rétablie, inventaire et chronologie comparés au départ. Le cloud reste en v5 et l’astérisque du pilotage temporaire est encore affiché dans l’onglet local.
- **Fichiers du coffre modifiés** — Rapport et capture ajoutés. Mise à jour du tableau de bord, du README, de la note mécanique, de la matrice, du contexte court, des ADR, du journal, de la roadmap et des tâches.
- **Décision et suite** — [[09_Gestion/ADR#ADR-006 — Assemblage final v5 comme référence de Phase 0|ADR-006]], puis [[09_Gestion/TACHES#AURA-003 — Préparer le squelette articulé|conception V2 dans une copie]]. Les essais FDM et la restauration de l’archive restent au suivi.

## 2026-11-21 — AURA-003 et prototype V2

- **Fusion** — Restauration de l’archive v5 dans `AURA-01 — Restauration v5` avec huit références distinctes. Second import dans `AURA-01 — Conception V2`. Enregistrement et réouverture de `AURA-01 — V2 — Prototype mécanique` en v5. Les révisions de la source et de ses huit fichiers liés ont été contrôlées après l’enregistrement.
- **Modifications** — Couronne J1, entretoisage J2/J3, poignet démontable J4/J5, pince à deux mors, coques galbées avec accès aux vis, six réserves moteur. La chronologie Fusion comporte 45 paramètres nommés.
- **Preuves** — 226 configurations Fusion, dont 137 états distincts sur dix trajectoires. Minimum de 5,53 mm au-dessus de l’appui en mouvement, sans interférence volumique aux états testés. HOME contrôlée après réouverture. Accès aux fixations testés sur gabarits et ordre de démontage consigné. Huit références de poses persistantes et 21 3MF contrôlés.
- **Coffre** — Notes mécanique et d’animation mises à jour avec trois captures. Tâches, ADR, journal, matrice, audit, tableau de bord, contexte, roadmap et renvoi dans le README actualisés.
- **Risques et suite** — L’estimation des masses et couples met en évidence le besoin d’ancrage du socle. Les jeux et les montages seront vérifiés par [[09_Gestion/TACHES#AURA-004 — Valider les interfaces d’impression|AURA-004]]. Le routage, les actionneurs et les essais en charge sont à poursuivre. [[09_Gestion/ADR#ADR-007 — Cinématique et maintenance du prototype V2]].

## 2026-11-21 — AURA-004 motorisation et fabrication

- **Fusion** — Copie séparée depuis la V2 v5. Création de la plaque ancrée et du berceau J1, localisation des pièces à modifier, manchons/arbres J2–J4, boîtiers des six moteurs, réducteur J5 et vis/écrous G1. STEP constructeur XC330 pour les trois axes distaux. Trois enveloppes J1–J3 d’après fiches avec empreinte à vérifier. Enregistrement et ouverture de la copie en v3.
- **Preuves** — À HOME aucune interférence CAO à la réouverture. Contrôles sur 99 configurations distinctes de dix transitions, liaisons d’entraînement J5 et G1 vérifiées depuis les entrées moteur et les sorties. Limites J2 restaurées après le contrôle de trajectoires qui en nécessitait la désactivation temporaire. Démonstration de 16 s et captures conservées dans le coffre.
- **Fabrication** — Tranchage virtuel des 21 fichiers de référence, des dix 3MF révisés/nouveaux et des cinq coupons. Profils, quantités et résultats dans `Exports_Fusion/AURA-004_Fabrication`. Essais en atelier à autoriser.
- **Calcul et décision** — Masse estimée ≈2,33 kg avec la plaque et une charge de 100 g. Cibles marquées J2 1,25 N·m et J3 0,68 N·m au joint, marge incluse. [[09_Gestion/ADR#ADR-008 — Ancrage démontable AURA-004|ADR-008]] et [[09_Gestion/ADR#ADR-009 — Actionneurs TTL à 11,1 V pour essais|ADR-009]].
- **Coffre** — Mécanique, impression, électronique, animation, matrice, tâches, contexte, tableau de bord et roadmap actualisés. Nomenclature ajoutée et renvoi dans le README.
- **Suite** — Les caractéristiques des moteurs sont vérifiées sur fiches. Les interfaces constructeur J1–J3 et la vis G1 restent à préciser avec le matériel. AURA-004 demeure EN COURS. Protéger le bras contre la descente à la coupure avant la mise sous tension du bras complet.

## 2026-11-22 — AURA-004 reprise et préparation atelier

- **Fusion** — Réouverture de la copie motorisée dans l’application de bureau. Export local terminé dans `Sauvegardes_Fusion/AURA-004_Motorisation-fabrication_2026-11-22.f3z`. Manifeste et intégrité de l’archive contrôlés, révision racine v3. Cette session a utilisé l’interface de Fusion, le MCP était indisponible. Les preuves de mouvement et de géométrie restent celles du 21 novembre. [[02_Conception_Fusion/CONCEPTION_MECANIQUE#AURA-004 — Assemblage de travail motorisé|Note mécanique]].
- **Fabrication** — Nouveau projet 3MF avec cinq coupons orientés et disposés sur un plateau 220 × 220 mm. Profil PETG intégré puis vérifié par un tranchage après réouverture. Prévision de 65,93 g et 7 h 35 min. Profil atelier et mesures de jeu ouverts. [[03_Impression_3D/PROTOCOLes_FDM#Plateau virtuel des cinq coupons|Plateau et feuille de mesures]].
- **Décisions et contrôles** — Preuves de catalogue ajoutées à l’ADR-009 pour les palonniers J1–J3. Vérifier le centrage, les vis et l’accès au faisceau au montage à blanc. Le banc J2/J3 dispose de cibles d’effort calculées pour contrôler le couple utile avec retenue mécanique. [[09_Gestion/ADR#ADR-009 — Actionneurs TTL à 11,1 V pour essais|ADR-009]] · [[05_Electronique/NOMENCLATURE_AURA004#Palonniers J1–J3 à vérifier au montage|Nomenclature]] · [[08_Tests/MATRICE_TESTS#Reprise du 22 novembre 2026|Matrice]].
- **Suite** — AURA-004 **EN COURS**. Passer au profil réel, mesurer les coupons et éprouver les assemblages, la coupure et le couple utile. [[09_Gestion/TACHES#AURA-004 — Valider les interfaces d’impression|Tâches]].

## 2026-11-22 — AURA-005, bras V3 et main blanche

- **CAO** — Construction d’une maquette indépendante par un script local dans Fusion. MCP absent. Révision locale r02, 23 composants, 22 pivots natifs pilotés individuellement et quinze contrôles boîtier/logement. [[02_Conception_Fusion/DESIGN_V3|Fichiers, cotes et résultats]].
- **Accès** — Export F3D et contrôle d’intégrité terminés. Réimport depuis le disque à vérifier, la boîte de dialogue Fusion est restée inaccessible au contrôle de l’interface.
- **Vidéo** — 168 images natives à 16 i/s, 10,5 s. Trois chapitres sur le roulis, les cinq doigts et le bras. Lecture complète vérifiée après encodage. [[04_Animation_Emotion/ANIMATIONS#V3 — Vidéo du poignet, des doigts et du bras|Chapitres]].
- **Décision** — V3 à trois segments, trois rotations de poignet et quinze moteurs de doigts. [[09_Gestion/ADR#ADR-010 — Main blanche et troisième segment|ADR-010]] · [[05_Electronique/README_MOTEURS_V3|Références d’achat]].
- **Suite** — Essais physiques ouverts. Vérifier un X06 et son palonnier sur une phalange, puis le couple d’un doigt complet. Revoir l’équilibrage de l’épaule avec les masses réelles. [[09_Gestion/TACHES#AURA-005 — Concevoir et éprouver le bras V3|Tâches V3]].

## 2026-11-22 — Simplification et validation FDM de la V3 r03

- **Audit** — Réouverture locale de la r02 dans Fusion. Treize collisions entre composants dès HOME et 110 recouvrements entre corps d’un même composant. Les volumes par pièce et les 22 comparaisons de poses sont enregistrés dans le dossier de fabrication r03.
- **Reprise CAO** — 23 occurrences, 22 pivots et 11 solides imprimables. Fourches intégrées, jeu des pivots et du pouce revus, cavités de servo ouvrant vers le dessous. F3D rouvert. Aucune intersection volumique détectée sur les 165 poses r03. [[02_Conception_Fusion/DESIGN_V3#V3 r03 — Structure simplifiée pour le FDM|CAO et relevés]].
- **Fabrication** — Onze STL fermés et six 3MF vérifiés par réouverture et tranchage. Supports générés uniquement sur le segment distal. Dossier et archive d’impression vérifiés. [[03_Impression_3D/PROTOCOLes_FDM#AURA V3 r03 — Kit d’impression|Kit r03]].
- **Suivi** — [[09_Gestion/ADR#ADR-011 — Un solide imprimé par corps articulé|Décision]], [[08_Tests/MATRICE_TESTS#V3 r03 — Assemblage et impression|preuves]] et [[09_Gestion/TACHES#AURA-005 — Concevoir et éprouver le bras V3|tâches]] mises à jour. Essais physiques de la phalange, d’un doigt complet puis des pièces du bras ouverts.

## 2026-11-22 — État de l’intégration autonome de la V3

- **Constat** — Lecture des sources de construction et des preuves de la r03. Les quinze logements des KST sont présents. J2, J3 et J4 ont des volumes de référence. J1 et les trois axes du poignet demandent une intégration moteur. Le faisceau continu, la visserie définitive, les montages capteurs, l’alimentation autonome et le logiciel de commande restent ouverts.
- **Préparation** — Architecture d’alimentation et de commande candidate ajoutée à la [[05_Electronique/SCHEMA_FUTUR#AURA-01 V3 — Intégration avant impression complète|note électronique]]. Courants documentaires recalculés. Pas d’impression complète avant qualification d’un premier module motorisé et conception des interfaces. [[09_Gestion/TACHES#AURA-005 — Concevoir et éprouver le bras V3|Tâches]].

## 2026-11-22 — AURA-006, deux bancs mécatroniques et intégration V3

- **CAO enregistrée.** Fusion 2706.1.17 a rouvert la r03 et la branche locale indépendante. Interventions à l’aide des API natives dans Fusion, ouvertes depuis le poste. Aucun outil MCP Fusion disponible dans cette session.
- **Doigt.** Trois KST, transmissions 15T, axes, bagues, vis et butées modélisés. Les 18 poses de service et trois poses à 47° sont dégagées, contacts des butées à 53°. D00–D03 exportés et tranchés.
- **Épaule.** STEP constructeur XM540, cartouche porteuse, réduction 4:1, arbre Ø12 et frein à ressort candidat sur la sortie. La révision 4 passe ses 13 angles de service. Les butées ont été atteintes au-delà. Cible 5,68 N·m en statique et 8,22 N·m pour le dimensionnement.
- **Branche.** Nouveaux mécanismes pour les quinze phalanges, paume modifiée, STEP ROBOTIS pour les autres moteurs et implantation du pack batterie, des cartes et de segments de faisceau. La qualification des transmissions et du câblage du bras reste en cours.
- **Mémoire et fabrication.** Rapport, notice d’atelier et prix des moteurs, décisions ADR-012 et ADR-013, tâches AURA-006 et matrice. L’archive r03 est conservée. Aucun achat, aucune impression et aucune mise sous tension physique dans cette session.
- **Suite.** Qualifier au banc le doigt et le maintien en charge de J2. Reprendre les transmissions et boucles mobiles avec les cotes et les résultats. [[02_Conception_Fusion/INTEGRATION_MECATRONIQUE_V3|Rapport et fichiers réels]].

## 2026-11-22 — Sauvegarde de la session Fusion

Sept archives AURA enregistrées dans le dossier « AURA-01 — Sauvegarde V3 et bancs — 2026-11-22 » du projet Fusion « Robotic Arm — V1 ». La branche mécatronique a été rouverte depuis le cloud avec 321 liaisons. Les 18 onglets ouverts ont une archive locale individuelle contrôlée. [Branche mécatronique dans Fusion](https://epitech619.autodesk360.com/g/projects/202611211172950976/data/dXJuOmFkc2sud2lwcHJvZDpmcy5mb2xkZXI6Y28uZklOeDVCbVFRQi1mc2FubXZzaHJ4Zw/dXJuOmFkc2sud2lwcHJvZDpkbS5saW5lYWdlOjB2S2RYUVd2VGphZjFLQXJKSFE2d2c) · [Inventaire de sauvegarde](../../../archives/v3/sauvegarde-fusion-2026-11-22/Sauvegarde_Fusion.json).

## 2026-11-22 — Liste d’achat V3

[README V2 — Éléments à acheter](../../../archives/v2/README_V2_ELEMENTS_A_ACHETER.md) créé à la racine à partir du README moteurs et de la notice des bancs. Prix et fiches de vente relevés avec priorité à Amazon France, puis auprès de vendeurs spécialisés. Le frein reste à chiffrer et les poulies de J2 attendent la validation d’interface. Suivi AURA-006 actualisé.

## 2026-11-22 — Priorité au bras V3 de table

Périmètre et design consignés dans la fiche du [[02_Conception_Fusion/PROTOTYPE_TABLE|bras V3 de table]]. Budget et liens vendeurs relevés dans la [liste à la racine](../../../archives/v2/README_V2_ELEMENTS_A_ACHETER.md). Mise à jour du README maître, des règles Codex, du contexte, du tableau de bord, de la roadmap, des décisions et des tâches. La CAO et les essais physiques restent à faire.

## 2026-11-22 — Bras V3 de table prêt pour présentation

Fusion 2706.1.17 piloté via MCP. Sauvegarde source **V3 — Intégration mécatronique**, v1, vérifiée avant création du document indépendant. Nouveau [document Fusion v1](https://epitech619.autodesk360.com/g/projects/202611211172950976/data/dXJuOmFkc2sud2lwcHJvZDpmcy5mb2xkZXI6Y28uS0w2NDZueTlSV3VLYXF5Z2ZkN196UQ/dXJuOmFkc2sud2lwcHJvZDpkbS5saW5lYWdlOlhxMVQ3NXBHUUk2eUNOWFJSZUpxQmc) dans **Robotic Arm — V1**, ouvert et synchronisé. Archive F3D rouverte avec 19 occurrences et trois liaisons pivot. 62 poses contrôlées en CAO, neuf STL vérifiés et trois 3MF tranchés. Capture vidéo des trois axes. [Fiche de présentation](../../../archives/aura-007/fusion/Fiche_presentation.md).

Mise à jour de la fiche AURA-007, du suivi, de la roadmap, des décisions, de la matrice et du README d’achat. Fixations, connectique, impression et commande physique à qualifier au banc.

## 2026-11-22 — Main et poignet articulés à budget réduit

Correction du périmètre à la demande de l’utilisateur. Silhouette et trois segments V3 repris. Nouvelle copie Fusion v2 dans **Robotic Arm — V1**. Quinze phalanges, roulis ±36° et prise groupée par un tambour. Passages de rappel rendus débouchants. 72 poses, trois plateaux tranchés et vidéo Fusion. [Document Fusion](https://epitech619.autodesk360.com/g/projects/202611211172950976/data/dXJuOmFkc2sud2lwcHJvZDpmcy5mb2xkZXI6Y28uS0w2NDZueTlSV3VLYXF5Z2ZkN196UQ/dXJuOmFkc2sud2lwcHJvZDpkbS5saW5lYWdlOm8wU21DcFFwVF9pQ3lrSGdWeThxR0E) · [Fiche de présentation](../../../archives/aura-008/fusion/Fiche_presentation.md).

README d’achat et moteurs, note de conception, règles, contexte, tableau de bord, décisions et suivi actualisés. Les perçages, la tension des tendons et le couple utile du coude restent à contrôler au montage.

La v2 a été synchronisée. Le serveur MCP a cessé de répondre au contrôle de la fenêtre active après la capture. L’archive locale et la vidéo ont ensuite été vérifiées sur disque.

## 2026-11-24 — AURA-01 r05 Budget Edition

- Audit de la r04 v4, comparaison de trois paniers et refonte des interfaces porteuses dans Fusion. La r05 enregistrée en v2 a été réimportée avec 105 occurrences et 18 couplages.
- Corrigé les dégagements de chapes, cassettes et gardes. Calculé masses, centres, couples, butées et réserves de câbles sur 85 poses.
- Exporté 39 STL, F3D et STEP. Tranché 18 plateaux et 39 3MF individuels. Intégré les réglages de supports et parois dans les archives. Retourné le palier 608 après comparaison.
- Réalisé la commande Pico, les vues, la vidéo et le rapport. Panier cible à 149,97 € TTC. Port réel, visserie disponible et essais physiques à confirmer.
- [[02_Conception_Fusion/TABLE_R05|Modèle et documentation r05]] · [[05_Electronique/README_MOTEURS_V3|Moteurs et alimentation]]
- Publication vérifiée sur la branche principale. [Commit r05](https://github.com/Flombt/Axo/commit/ecc2308ec4521cbc6c49ad148433d983fa783578)

## 2026-11-24 — Revue design de la V5

- Archive r05 v2 auditée et sauvegardée avant reprise. Variante native enregistrée dans Fusion et archive locale rouverte avec 116 occurrences, 27 pivots et 18 liens de mouvement.
- Cinq essais de commande indépendante au solveur natif et quatorze contrôles de poses au noyau solide. Risque confirmé de descente sous le plan de table en combinant les butées basses J2/J3. Exemples chiffrés consignés dans la note de revue.
- Panier cible de 148,98 € TTC livré sous hypothèses de port, visserie existante comprise en réemploi. Le lot de servos, les mouvements en charge et les passages réels du faisceau restent à qualifier. [[02_Conception_Fusion/TABLE_V5_REVUE_DESIGN|Revue]] · [Prix et stock](../../../archives/v5-revue/ACHATS.md)

## 2026-11-24 — Deux axes longitudinaux sur la V5

- Vérifié l’archive de la revue V5 v2 et sauvegardé une variante distincte dans Fusion. Réouverture contrôlée avec 154 occurrences, 31 pivots et 20 liens de mouvement.
- Réalisé les deux roulis en série avec les tangages, leurs paliers fendus et les deux entraînements déportés dans le socle. Test natif aux quatre extrémités et recontrôle des solides sur 31 poses.
- Chiffré les pièces ajoutées à 13,10 € et le panier de mise au point à 149,48 € selon les hypothèses de port. Passage des gaines, maintien et alimentation en charge à qualifier. [[02_Conception_Fusion/TABLE_V5_ROULIS|Implantation]] · [Achats historiques](https://github.com/Flombt/Axo/blob/aura-01-v5-roulis-v1/purchases/NOMENCLATURE.md)

## 2026-11-24 — Audit indépendant avant fabrication de la V5 roulis

- Identifié la V5 roulis Fusion v1 et vérifié l’empreinte du F3D. La tête GitHub demeure la r05. Rejoué les poses sur une réimportation temporaire.
- 141 poses cibles atteintes et 33 analyses d’interférence. Point bas à −56,68 mm. Quatre jonctions J1 s’écartent de 33,31 à 39,45 mm. Pince pouce-index à 17,68 mm au mieux de la grille.
- Inventorié les 154 occurrences et 1 134 fichiers. Vérifié trois plateaux r05 dans Anycubic et les scènes historiques dans Blender. La V5 roulis n’a pas encore de kit d’impression conjoint.
- Confirmé que le fichier d’entrée r05 échoue à la compilation MicroPython testée et que la V5 réclame onze voies. Le budget conditionnel atteint 161,43 € avec une bobine avant corrections. Aucun essai physique.
- [Rapport complet](../../../DIAGNOSTIC_ROBOT_COMPLET.md) · [Registre](../../../docs/diagnostic/latest/REGISTRE_PROBLEMES.md) · [Suivi historique](../../../docs/diagnostic/latest/SUIVI_HISTORIQUE.md)

## 2026-11-24 — Réorganisation et règles de maintenance

- Associé le dossier Aura à l’historique Git vérifié. Déplacé la CAO active vers [fusion/AURA-01.f3d](../../../fusion/AURA-01.f3d) avec la même empreinte. Les archives anciennes ont un manifeste par révision.
- Vérifié la reconstruction de 116 projets de transfert à partir des exemplaires canoniques et la récupération d’une vidéo r03 par SHA-256. Les quatre vidéos ont des copies vérifiées sur la release.
- Mis à jour la navigation et ajouté la vérification en lecture seule. [Rapport de réorganisation](../../../docs/REORGANISATION_PROJET.md) · [Règles](../../../AGENTS.md) · [Contexte](../../../docs/architecture/PROJECT_CONTEXT.md)

## Template de session

### YYYY-MM-DD HH:mm — <objectif>
- **Documents lus :** ...
- **Fichiers du coffre modifiés** — ...
- **Fichiers Fusion touchés :** ...
- **Actions réellement exécutées :** ...
- **Résultats vérifiés :** ...
- **Échecs / obstacles :** ...
- **Décisions :** ...
- **Prochaine action :** ...
