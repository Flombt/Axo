# AURA-01 — Audit initial dans Autodesk Fusion

**21 novembre 2026 · Robotic Arm — V1 · Assemblage final v5 · Fusion 2706.1.17 sous Windows**

**Diagnostic.** Le prototype fournit une base cinématique numérique exploitable. Le socle reste fixe et le solveur pilote trois rotations de pose et une translation de pince. Le poignet est rigide et la pince a un doigt mobile. Les priorités V2 sont la retenue mécanique des pivots, un poignet J4–J5 compact, l’intégration des actionneurs et la validation FDM des ajustements.

![[assets/fusion_audit_v005_2026-11-21.png|Vue Fusion de l’assemblage v5 en position neutre]]

## Révision et sauvegarde

- Le serveur MCP a identifié le projet et le document actif, puis exécuté dans Fusion l’inventaire, les mesures B-Rep, le pilotage des liaisons et l’analyse des interférences. Autodesk Assistant était visible dans la session.
- Le document de départ était enregistré en **v5**. Identifiant de révision `urn:adsk.wipprod:fs.file:vf.MU3Fmx2JSga13UjZNZWmCQ?version=5`.
- Archive native versionnée à la racine de l’espace `Aura`, dans `Sauvegardes_Fusion/AURA-01_Assemblage-final_source-v005_2026-11-21.f3z`. L’export natif F3Z inclut l’assemblage et les huit fichiers externes. Les versions et les neuf membres F3D correspondent au manifeste et les contrôles CRC de l’archive et des membres sont passés. Taille 1 621 518 octets. [Sauvegarde native Fusion avec références](https://help.autodesk.com/view/fusion360/ENU/?caas=caas%2Fsfdcarticles%2Fsfdcarticles%2FHow-to-make-a-local-archive-back-up-file-in-Fusion-360.html)
- SHA-256 `90eb4b714630c2820e5d5b952fe7a5995050c20d23d509c64ef86dbe5bb0808f`. La restauration était ouverte à la fin de l’audit. Elle a depuis été vérifiée dans Fusion pendant AURA-003 (T-051). [[02_Conception_Fusion/CONCEPTION_MECANIQUE#Restauration et indépendance|Preuve de restauration]].
- Après les essais, les quatre valeurs sont revenues à zéro. L’inventaire, les matrices de placement, les douze paramètres d’assemblage et les quinze entrées de chronologie correspondent au relevé de départ. Le document cloud est resté en v5. Fusion affiche encore l’astérisque de la manipulation temporaire dans l’onglet local.

## Inventaire et état de la géométrie

Huit occurrences externes à la racine et huit solides fermés, un par occurrence. Fusion recense neuf définitions avec la racine incluse. Les références étaient complètes et à jour. La racine contient huit insertions et sept liaisons dans sa chronologie, zéro corps, zéro esquisse et zéro paramètre utilisateur. Ses douze paramètres de modèle portent les limites et valeurs de repos des quatre liaisons mobiles. Les fichiers liés exposent 47 fonctions d’extrusion et leurs esquisses, sans avertissement remonté sur ces fonctions lors de la lecture. Tous les corps portent le matériau CAO « Acier ».

Les boîtes des pièces ci-dessous sont mesurées suivant leurs axes locaux. L’assemblage neutre occupe **252,61 × 96,00 × 141,23 mm** suivant X, Y, Z. Les cotes sont issues des solides et converties des unités internes Fusion. [Unités de l’API Fusion](https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/Units_UM.htm)

| Pièce suivie | Encombrement local en mm | Constat dans Fusion | Action V2 proposée |
| --- | --- | --- | --- |
| Base v2 | 96,00 × 96,00 × 15,00 | Flasque Ø96 avec bossage Ø20. Quatre passages Ø4,5 et lamages Ø8,3 de 2,25 mm de profondeur sur un carré de 56 mm. Base fixée au parent dans Fusion. | Conserver la base circulaire et le principe de fixation. Dimensionner l’appui, la retenue axiale du plateau et un compartiment accessible pour l’actionneur J1. |
| Épaule v2 | 62,00 × 62,00 × 47,00 | Plateau Ø62, alésage Ø20,6, chape à deux oreilles de 7 mm, passage d’axe Ø6,2 et perçages Ø2,7 pour une future platine. | Conserver la double chape et l’axe lisible. Prévoir entretoises, guidage, platine démontable et accès à la visserie. |
| Bras supérieur v2 | 122,00 × 31,20 × 24,00 | Longeron ajouré et chape de coude. Entraxe épaule–coude 100,00 mm. Oreilles du coude de 6,3 mm, passage Ø5,2 et perçages de platine Ø2,7. | Conserver le chemin des efforts et la silhouette. Revoir les transitions de section et l’ajourage après étude de la flèche et des contraintes aux oreilles. |
| Avant-bras v2 | 93,50 × 24,00 × 20,00 | Longeron ajouré et moyeu Ø5,2. Distance du pivot de coude au repère d’interface fixe 84,00 mm. Quatre trous d’interface Ø3,3. | Conserver le principe de bride. Affiner le volume distal et ménager une route de câble avec accès de maintenance. |
| Poignet v2 | 52,00 × 47,00 × 27,50 | Bride en appui sur l’avant-bras, quatre perçages Ø3,3 alignés. Corps unique avec traverse, glissière en T et doigt fixe. Liaison rigide à l’avant-bras. | Remplacer le bloc rigide par un module J4 pitch / J5 roll démontable. Séparer le guidage et l’effecteur pour rendre la pince remplaçable. |
| Pince v2 | 39,65 × 7,00 × 16,15 | Patin en T, col de guidage, doigt mobile strié et perçage d’entraînement Ø2,6. L’autre doigt est solidaire du poignet. | Conserver le code couleur et l’étude du guidage. Ajouter transmission, retenue aux extrémités et mors à inserts souples. Étudier deux doigts mobiles synchronisés pour atteindre la cible G1. |
| Axe d’épaule v1 | Longueur 37,60 | Portée Ø6, gorge Ø5,35, épaulement et tête hexagonale. Fixé à l’épaule par une liaison rigide. | Conserver cette géométrie comme enveloppe de montage. Dimensionner un axe métallique, son palier et sa retenue. |
| Axe de coude v1 | Longueur 34,85 | Portée Ø5, gorge Ø4,35, épaulement et tête hexagonale. Fixé au bras supérieur par une liaison rigide. | Employer le même principe de retenue démontable, en vérifiant la gorge, le jeu axial et l’accès à l’outil. |

Les perçages et les deux axes sont modélisés. Les deux axes constituent toute la quincaillerie modélisée. La visserie, les roulements, les circlips et les moteurs restent à spécifier. Le dossier `Moteurs` du projet Fusion était vide lors de l’inspection. Les perçages de platine et d’entraînement définissent des interfaces géométriques, à compléter par des volumes constructeur, une transmission et un trajet d’insertion.

La nouvelle capture retrouve la base ronde sombre, les deux longerons bleus, les têtes d’axes visibles et le doigt mobile rouge de la [[assets/fusion_etat_initial_2026-11-21.png|capture de départ]]. Les libellés `Cube MCP` et `Corps2` de l’historique d’Autodesk Assistant sont absents de l’inventaire des solides et de la chronologie de la v5.

## Articulations et mouvements mesurés

Le repère de l’assemblage utilise Z vertical. Les longueurs sont en mm et les angles en degrés, par rapport à la pose neutre `(0, 0, 0, 0)`.

| Cible AURA-01 | Liaison dans Fusion | Axe et repère relevés | Valeurs atteintes |
| --- | --- | --- | --- |
| J1 · rotation du socle | A1 · pivot Base–Épaule | +Z, point (0 ; 0 ; 7,8) | −80° à +80° |
| J2 · épaule | A2 · pivot Épaule–Bras supérieur | +Y, ligne passant par X = 0 et Z = 42,35 | −32° à +21° |
| J3 · coude | A3 · pivot Bras supérieur–Avant-bras | +Y, ligne passant par X = 69,47 et Z = 114,28 au neutre | −38° à +18° |
| J4 · inclinaison du poignet | Interface Avant-bras–Poignet rigide | Axe fonctionnel à créer | — |
| J5 · roulis du poignet | Interface Avant-bras–Poignet rigide | Axe fonctionnel à créer | — |
| G1 · préhension | A4 · glissière Poignet–Pince | +Y au neutre et solidaire du repère du poignet | −22,5 à +4,5 mm, soit 27 mm de course |

Le contrôle des surfaces cylindriques montre la coaxialité nominale de chaque pivot avec ses pièces d’interface. Les sept liaisons sont de type « telles que construites » et actives. Les trois liaisons rigides concernent l’interface avant-bras–poignet et les deux axes de fixation. Chaque commande mobile a déplacé les occurrences attendues. A1 entraîne tout le bras au-dessus de la base, A2 entraîne le bras supérieur et l’aval, A3 entraîne l’avant-bras et l’aval et A4 déplace uniquement le doigt mobile. Le socle est resté immobile sur les 46 poses.

### Interférences et limites du contrôle

Le solveur Fusion a atteint les consignes dans 46 configurations. À chaque pose, l’analyse d’interférences a inspecté les huit solides en excluant les faces simplement coïncidentes. Elle renvoie **zéro interférence volumique détectée** pour ces poses. L’appui prévu entre l’avant-bras et le poignet mesure 0 mm au droit des faces de bride. Les pièces mobiles restent au-dessus de Z = 0 sur l’échantillon, avec 8,35 mm au point le plus bas de l’épaule. [Analyse d’interférences de Fusion](https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/fusion_Design_createInterferenceInput.htm)

- **Pose neutre** — `(0, 0, 0, 0)`.
- **29 poses sur un axe à la fois** — A1 à ±20°, ±40°, ±60° et ±80°. A2 à −32°, −24°, −16°, −8°, +7°, +14° et +21°. A3 à −38°, −28,5°, −19°, −9,5°, +6°, +12° et +18°. A4 à −22,5, −18, −13,5, −9, −4,5, +2,25 et +4,5 mm.
- **16 poses combinées** — Produit des deux butées de chacun des quatre axes. Les deux surfaces planes opposées des mors mesurent 24,00 mm d’écart au neutre et 1,50 à 28,50 mm aux butées de la glissière.
- **Portée de la preuve** — Contrôle géométrique aux points échantillonnés. L’analyse de contact est désactivée et zéro ensemble de contacts est configuré. Le balayage continu, les nouveaux carters, les câbles, les butées physiques, l’effort de serrage, la stabilité et la calibration HOME après réouverture restent à vérifier.

## Jeux fonctionnels et risques FDM

| Interface | Mesure nominale en CAO | Risque mécanique et réponse proposée |
| --- | --- | --- |
| J1 · bossage et plateau | Ø20 dans Ø20,6. Jeu radial 0,30 mm et séparation axiale 0,35 mm. | Soulèvement et basculement en porte-à-faux. Prévoir une retenue axiale démontable et des surfaces de guidage adaptées. Vérifier le couple de renversement et la fixation de la base Ø96 sur table. |
| J2 · chape et moyeu d’épaule | Ø6 dans Ø6,2. Jeu radial 0,10 mm. Moyeu de 15 mm dans une chape de 20 mm, soit 2,50 mm de chaque côté. | L’ovalisation imprimée peut réduire le faible jeu radial. Les espaces latéraux demandent un entretoisage pour limiter le battement. Prévoir un coupon axe–palier et un test en charge. |
| J3 · chape et moyeu de coude | Ø5 dans Ø5,2. Jeu radial 0,10 mm. Moyeu de 14 mm dans une chape de 18,6 mm, soit 2,30 mm de chaque côté. | Même risque d’ovalisation et de battement. Maîtriser la coaxialité au montage et vérifier la tenue des oreilles et de la retenue d’axe. |
| G1 · glissière en T | Patin de 7,30 mm dans un canal de 8,00 mm. Jeu de 0,35 mm par côté. Col de 4,25 mm dans une fente de 4,80 mm, soit 0,275 mm par côté. Jeu vertical nominal de 0,35 mm sous le patin et 0,50 mm au-dessus. Lèvre de retenue de 1,20 mm. | Coincement par rugosité ou défaut de forme. Risque de rupture ou de délaminage de la lèvre sous effort du mors. Prévoir un premier coupon de la section complète, puis comparer une traverse épaissie à un guide démontable en deux pièces. |

Dans la section des perçages de platine, le ligament nominal entre le passage d’axe et le trou voisin est de **3,55 mm** à l’épaule et **3,05 mm** au coude. Ce sont des distances locales entre diamètres, utiles pour cibler une coupe et un essai de fatigue. Les ajourages et changements de section méritent une revue des chemins d’effort. Orienter les pièces de façon que les sollicitations aux oreilles ne reposent pas principalement sur l’adhésion entre couches. Vérifier l’accès aux supports sous le guide en T, l’insertion des axes, la tenue des inserts et l’accès de l’outil de serrage.

Pour préparer le dimensionnement, une charge hypothétique de 100 g appliquée verticalement à X ≈ 204,61 mm au neutre donne un moment statique d’environ **0,201 N·m à J2** et **0,133 N·m à J3**. Ce calcul concerne la charge seule. Le dimensionnement intégrera les masses des pièces et des moteurs, leurs bras de levier, les efforts dynamiques et les marges de tenue.

La forme B-Rep fermée est constatée. Pour qualifier la fabrication, il reste à choisir machine, matière et profil, à contrôler l’orientation et les supports dans le slicer, puis à mesurer les coupons et à réaliser un montage à blanc. La résistance, la fatigue, la flèche sous charge et la tenue au serrage restent à mesurer. Le matériau « Acier » affecté dans Fusion doit être remplacé par des données représentatives pour calculer les masses et la résistance de la version imprimée. Voir le [[03_Impression_3D/PROTOCOLes_FDM|protocole d’impression]] et le [[README#19 — Jeux, tolérances, ajustements et essais|plan des ajustements]].

## Écarts au cahier des charges

| Cible du README | État de la v5 |
| --- | --- |
| REQ-001 · pièces indépendantes et paramétriques | Huit pièces externes distinctes avec historique d’extrusion. Les cotes maîtresses nommées et la propagation d’une modification restent à établir. |
| REQ-002 à 004 · cinq axes, pince et repli | Trois pivots de pose éprouvés sur l’échantillon. La glissière agit sur un doigt. J4, J5, la synchronisation des doigts et une pose HOME qualifiée restent à concevoir ou à valider. |
| Dimensions de départ | Socle Ø96 mm contre 160 mm en hypothèse. Épaule–coude 100 mm contre 135 mm. Coude–interface rigide 84 mm contre 120 mm envisagés pour le futur entraxe coude–poignet. Le datum final J4 reste à définir. |
| REQ-005 à 007 · FDM, moteurs et maintenance | Jeux CAO mesurés, perçages et interfaces présents. Les données atelier, les actionneurs, les fixations et l’accès à l’outil restent à valider. |
| REQ-008 à 010 · silhouette, expression et fluidité | Identité visuelle de départ présente. Les placements articulaires sont pilotables dans Fusion. Les gestes, la répétabilité, la vitesse et la fluidité restent sans essai. |

Références du projet dans le [[README#04 — Morphologie cible et degrés de liberté|schéma des axes]], les [[README#05 — Dimensions de départ : hypothèses à paramétrer, pas cotes de fabrication|cotes de départ]] et les [[README#06 — Gestion des exigences et statuts de preuve|exigences REQ-001 à REQ-018]].

## Plan de conception AURA-01 V2

1. **Socle et chaîne mobile.** Partir d’une copie de travail issue de la v5. Conserver les repères éprouvés de J1–J3. Définir les cotes maîtresses, l’effort de renversement du socle, la retenue J1 et les paliers, entretoises et retenues de J2/J3. Coter les empilements axiaux et modéliser les références de fixation avec leur accès d’outil.
2. **Design expressif.** Définir un poignet démontable à deux axes, avec un pitch J4 pour les gestes d’inclinaison et un roll J5 pour l’orientation des mors. Conserver le socle rond, les volumes effilés et la lecture des axes. Comparer les silhouettes en salut, en retrait et en exploration. Décliner en graphite/titane, bleu glacier et accent corail, avec capots démontables autour d’une structure porteuse distincte.
3. **Intégration et fluidité.** Faire le bilan des masses, centres de gravité et couples de J2/J3 avec la charge utile envisagée et des volumes fournisseurs réels. Intégrer transmission, connecteurs, mou de câble et butées. Employer des limites de vitesse, accélération et variation d’accélération pour les transitions. Vérifier HOME, repli, extension et trajectoires intermédiaires, à nouveau avec carters et câbles. Contrôler le jeu et la répétabilité à basse vitesse.
4. **Premiers essais FDM.** Prototyper un pivot complet et la section de glissière avant les grandes impressions. Comparer les jeux nominaux mesurés avec des coupons sur la machine retenue. Vérifier au slicer l’orientation, les supports et le volume utile, puis mesurer l’ovalisation, la tenue des inserts, la flèche, l’usure et le fonctionnement du guide. Lancer l’assemblage complet après montage à blanc et validation de ces interfaces.

## Sortie de Phase 0

La révision de départ, les cotes et les inconnues sont documentées. La [[09_Gestion/TACHES#AURA-002 — Auditer et sauvegarder Assemblage final|tâche d’audit]] est clôturée. Les validations se poursuivent dans la [[08_Tests/MATRICE_TESTS|matrice de tests]] et la conception V2 démarre à la [[09_Gestion/TACHES#AURA-003 — Préparer le squelette articulé|tâche AURA-003]]. Voir aussi le [[09_Gestion/JOURNAL#2026-11-21 — Phase 0 Fusion et sauvegarde v5|journal de session]].
