# Décisions d'architecture (ADR)

## AURA-009 r04 — planches couleur anycubic

Décision du 24 novembre 2026. Regrouper chaque couleur en une planche et conserver un 3MF par référence pour les remplacements. Les teintes des corps imprimables viennent de Fusion v4. Le pignon et le support moteur J1 partagent le gris acier. La préparation vise un transfert USB avec le profil matériel réel au moment de l’export. [Guide des 3MF par couleur](../../../archives/r04/anycubic/README.md).

## AURA-009 r04 — Actionneurs d’avant-bras et axe creux

Décision du 24 novembre 2026. Implante cinq microservos sur l’avant-bras et garde le poignet franchissable par cinq gaines de longueur utile contrôlée. Le socle sépare l’appui mécanique, l’engrènement et le passage électrique. La commande et les ajustements se qualifient sur un doigt et un socle à vide. [[02_Conception_Fusion/TABLE_R04|Prototype de table r04]] · [Rapport de fabrication](../../../archives/r04/VALIDATION_FABRICATION.md).

## AURA-009 r03 v2 — Vérification des trajectoires rendues

Décision du 24 novembre 2026. La CAO Fusion demeure la référence des axes, limites, couplages et volumes. Après reprise dans Blender, les matrices du film sont rejouées dans Fusion sur les vrais solides pour contrôler l’effet de l’arrondi des commandes de pivot. Après modification d’un pivot ou d’une trajectoire, réexécuter les contrôles concernés. [[04_Animation_Emotion/ANIMATIONS#AURA-009 r03 v2 — Démonstration cinématique|Démonstration r03 v2]] · [Rapport cinématique](../../../archives/r03/animations/RAPPORT_CINEMATIQUE.md).

## AURA-009 de table r03 — Articulations portées et banc ancré

Décision du 23 novembre 2026 pour le [[02_Conception_Fusion/TABLE_R03|kit r03]].

- Les arbres acier Ø5 de J2/J3 s’appuient chacun sur deux bagues. Le J2 conserve le MG996R avec quatre M2,5 traversantes. Le J3 reçoit un XC330-M288-T à 5 V avec palonnier constructeur. Les corps moteurs se retirent latéralement sans dépose de l’arbre porteur. La commande gère séparément l’interface TTL de J3 et les trois servos PWM. [[05_Electronique/README_MOTEURS_V3|Motorisation]].
- Chaque articulation porteuse reçoit une retenue passive par friction et une assistance de ressort à qualifier. Des butées indépendantes encadrent les plages numériques. La retenue sous charge demande mesure et réglage au banc.
- Le plateau est ancré par quatre M5. La rotation J1 reste indexable à la main, avec axe Ø8 et interfaces réservées pour une motorisation ultérieure. Le lest est fixe et optionnel. J7 reste un seul axe, soutenu par deux roulements.
- La main conserve une commande groupée avec cinq réglages élastiques. Les limites de force et la réouverture nécessitent un essai sur objet retenu. Les capteurs, le calcul et les sources de puissance restent près de la base quand leur fonction le permet.

## Montage r02 — Pouce démontable, axe commun et cassette J7

- **Date** 2026-11-22. Choix retenu pour la [[02_Conception_Fusion/MONTAGE_V3|révision AURA-009]].
- La chape du pouce sort latéralement et se fixe par deux M2×10. Elle se pose après l’axe commun des quatre doigts. Le renvoi lisse inverse le chemin du tendon pour obtenir une flexion à la traction.
- La cassette de roulis sort par l’avant avec le servo. Poser le moyeu à clé après la cassette, puis la paume. Employer une boucle extérieure pour les fils T1.
- La commande à quatre servos de position conserve le Nano. Le rail des servos reçoit le 5 V d’un bloc externe. Le logiciel attend une calibration et un armement, puis lance le cycle sur appui. Qualifier l’ampacité, les protections et le maintien du bras à la coupure.

## ADR-001 — Autodesk Fusion reste la source mécanique
- **Date :** 2026-11-21.
- **État :** DÉCIDÉ.
- **Motif :** projet et prototype déjà présents dans Fusion sous licence Education.
- **Conséquence :** formats maillés et Blender ne remplacent pas le fichier natif.

## ADR-002 — 5 axes et pince en V1
- **Date :** 2026-11-21.
- **État :** HYPOTHÈSE DE CONCEPTION RETENUE.
- **Motif :** compromis expressivité / complexité / masse.
- **À confirmer :** choix moteur, cinématique exacte, dimensions, charge utile.

## ADR-003 — FDM d'abord ; motorisation plus tard
- **Date :** 2026-11-21.
- **État :** DÉCIDÉ.
- **Motif :** fabriquer des pièces personnalisées à l'atelier avec moteurs/vis achetés.
- **Conséquence :** jeux et orientations d'impression à valider.

## ADR-004 — IA non souveraine sur le matériel
- **Date :** 2026-11-21.
- **État :** DÉCIDÉ.
- **Motif :** sécurité et reproductibilité.
- **Conséquence :** commandes structurées et contrôle local.

## ADR-005 — Mémoire et suivi dans le coffre Obsidian

- **Date** — 2026-11-21.
- **État** — DÉCIDÉ.
- **Contexte** — Retrouver les règles et reprendre le projet depuis ses fichiers à chaque session.
- **Choix** — [[AGENTS]] porte les règles Codex et [[00_DASHBOARD|le tableau de bord]] organise la navigation. Le [[README|cahier des charges]] reste la référence du projet.
- **Conséquences** — Consigner les décisions dans les ADR, les modifications et preuves dans le [[09_Gestion/JOURNAL|journal]], les actions dans le [[09_Gestion/TACHES|suivi des tâches]] et l’ordre des phases dans la [[09_Gestion/ROADMAP|roadmap]].
- **Trace** — [[09_Gestion/JOURNAL#2026-11-21 — Mise en place de la mémoire Obsidian|Session de mise en place]].

## ADR-006 — Assemblage final v5 comme référence de Phase 0

- **Date** — 2026-11-21.
- **État** — DÉCIDÉ.
- **Motif** — Disposer d’un état de reprise révisé et de toutes ses pièces liées avant la conception V2.
- **Choix** — Prendre `Robotic Arm — V1 / Assemblage final v5` et l’archive F3Z vérifiée comme référence de comparaison. Développer les variantes V2 dans une copie de travail.
- **Conséquences** — Tracer les prochaines mesures à leur révision et comparer les changements à l’état audité. Le choix de la motorisation et la conception J4–J5 restent à mettre à l’étude.
- **Preuve** — [[02_Conception_Fusion/audit_initial#Révision et sauvegarde|Révision, manifeste et empreinte de sauvegarde]].

## ADR-007 — Cinématique et maintenance du prototype V2

- **Date** — 2026-11-21.
- **État** — DÉCIDÉ pour le prototype numérique.
- **Contexte** — Le poignet v5 était rigide, la pince ne déplaçait qu’un mors et le socle ne comportait pas de retenue axiale suffisante.
- **Choix** — Partir de deux réimportations séparées de la v5. Maintenir le squelette utile, reprendre ses retenues et ajouter une chape avec pivot métal J4 ±30° puis un rotor creux coaxial J5 ±65°. Retenir le flasque du rotor par deux demi-colliers dévissables. Coupler les deux mors par un lien 1:1 dans Fusion, avec une vis à pas opposés comme architecture à détailler. Garder les coques démontables.
- **Limite J2** — Lier la borne d’abaissement à `j2_lowering_max = 6.5 deg`. Les essais à +21° traversaient le plan d’appui et ceux à +8° laissaient 0,30 mm au point testé le plus bas. La garde minimale mesurée à +6,5° est de 5,53 mm.
- **Conséquences** — Les logements réels, la tenue du poignet, la vis, les efforts de pince et le faisceau doivent être validés avec le matériel. Les essais de charge devront tenir compte du besoin d’ancrage. [[02_Conception_Fusion/CONCEPTION_MECANIQUE#V2 — Prototype mécanique enregistré]]

## ADR-008 — Ancrage démontable AURA-004

- **Date** — 2026-11-21.
- **État** — DÉCIDÉ pour la branche de conception. Efforts et appui réels à qualifier.
- **Choix** — Plaque métallique 260 × 220 × 8 mm et quatre ancrages M6. Quatre tubes et les tirants M4 dégagent le motoréducteur de lacet sous le socle.
- **Motif** — Le socle Ø96 mm ne contient pas la projection du centre de gravité du bras seul. Le moment de rappel statique sur la plaque libre est d’environ 2,27 N·m, alors que l’effort accidentel étudié produit déjà 6,4 N·m.
- **Validation** — [[02_Conception_Fusion/CONCEPTION_MECANIQUE#Plaque et ancrage démontable]].

## ADR-009 — Actionneurs TTL à 11,1 V pour essais

- **Date** — 2026-11-21.
- **État** — HYPOTHÈSE DE CONCEPTION RETENUE pour la CAO et la préparation du banc.
- **Choix** — XL430 pour le socle, XM540/XM430 pour épaule et coude, XC330 pour J4/J5/G1. Bus TTL DYNAMIXEL, alimentation puissance séparée et commande locale USB. Arbres à double méplat J2–J4, réduction 42/18 à J5 et vis à pas opposés G1.
- **Motif** — Prioriser la tenue de J2/J3, le retour de position et la masse distale. Préserver un passage de câble axial dans le poignet.
- **Validation** — Contrôles géométriques et premier dimensionnement acquis. Confirmer les attaches J1–J3, le couple continu, les efforts et l’arrêt avec protection contre la chute. [[05_Electronique/NOMENCLATURE_AURA004]].
- **Preuve fabricant du 22 novembre** — Les kits identifient HN11-N101 sur J1, HN13-N101 sur J2 et HN12-N101 sur J3. Les références et supports démontables sont à confronter aux pièces reçues pour vérifier le centrage, l’engagement des vis et l’accès avec le faisceau. [[05_Electronique/NOMENCLATURE_AURA004#Palonniers J1–J3 à vérifier au montage|Références des kits]].

## ADR-010 — Main blanche et troisième segment

- **Date** — 2026-11-22.
- **État** — DÉCIDÉ pour la V3. Motorisation candidate, banc ouvert.
- **Choix** — Trois segments en série avec trois rotations au poignet et une main blanche. Cinq doigts, trois phalanges et trois pivots par doigt. Un microservo dans la phalange actionnée et un pivot passif coaxial de l’autre côté.
- **Motif** — Donner à AURA-01 davantage de possibilités de pose et de gestuelle. Une empreinte de servo commune aux quinze phalanges simplifie les pièces et le stock. La masse distale augmente les efforts sur l’épaule.
- **Conséquences** — Les achats, le couple continu, les rapports de transmission, le faisceau et la retenue hors tension restent à qualifier. Mettre à jour la [[05_Electronique/README_MOTEURS_V3|nomenclature des moteurs]] lors de chaque substitution. [[02_Conception_Fusion/DESIGN_V3|Assemblage et contrôle des pivots]].

## ADR-011 — Un solide imprimé par corps articulé

- **Date** — 2026-11-22.
- **État** — DÉCIDÉ pour la V3 r03, vérifié en CAO et en tranchage.
- **Choix** — Intégrer fourches, ponts et logements à chaque solide. Standardiser un modèle par rang de phalange, cinq exemplaires chacun. Monter les servos et les axes depuis les ouvertures accessibles.
- **Motif** — Les recouvrements r02 gênaient l’assemblage et la séparation des pièces. Le regroupement réduit le nombre de pièces et préserve les mouvements indépendants.
- **Validation** — [[02_Conception_Fusion/DESIGN_V3#V3 r03 — Structure simplifiée pour le FDM|Audit et CAO]] · [[03_Impression_3D/PROTOCOLes_FDM#AURA V3 r03 — Kit d’impression|Six plateaux tranchés]]. La tenue des pièces imprimées reste à éprouver.

## ADR-012 — Transmission de l’épaule et frein de sortie sur banc indépendant

En vigueur pour le banc J2. Le XM540 conserve son palonnier HN13-N101 et entraîne un arbre d’entrée sur deux roulements. La courroie 5M 16/64 transmet à l’arbre Ø12 porteur. Le frein à ressort est placé sur la sortie, en aval de la courroie. Cette disposition reprend la tension indépendamment de l’axe du servo et permet au frein de tenir l’arbre lors d’une rupture de la transmission. La variante en prise directe a été écartée pour l’essai chargé. Fixation, retenue, chauffe et coupure en charge restent à qualifier. [[02_Conception_Fusion/INTEGRATION_MECATRONIQUE_V3#C — Épaule J2 indépendante|Calculs et banc]].

## ADR-013 — Commande déportée et batterie sur bâti fixe

Retenu pour l’intégration. Garder les 15 PWM dans la main, répartir le 6 V en deux groupes et monter la batterie dans un berceau extérieur sur le bâti fixe. Séparer calcul embarqué, contrôleur temps réel et coupure matérielle. Ces dispositions limitent la masse mobile et évitent quinze lignes PWM dans le poignet. Le BMS, les convertisseurs et les trajets des câbles restent soumis aux essais. [[05_Electronique/SCHEMA_FUTUR#AURA-006 — Batterie, arrêt et commande de la main|Implantation et commande]].

## ADR-014 — Commencer par trois axes motorisés sur le design V3

- **DÉCIDÉ le 22/11/2026.** Prioriser le mouvement autonome sur un petit bras au design V3. Lancer un geste stocké localement par un bouton. Mettre la V3 complète en pause pour limiter les coûts et le temps d’intégration.
- **Choix d’essai.** J1, J2 et J3 motorisés. Arduino et alimentation secteur. Conserver poignet, troisième segment et main blanche fixes. Voir le [[02_Conception_Fusion/PROTOTYPE_TABLE|bras V3 de table]].
- **Implantation r01.** Entraxes de 47, 44 et 40 mm, trois MG90S en prise directe, appuis passifs à l’épaule et au coude. Coques accessibles. Voir les [[02_Conception_Fusion/PROTOTYPE_TABLE#Maquette de présentation r01|jeux modélisés et vérifications]].

## ADR-015 — Garder les phalanges et le roulis avec quatre servos

- **Décidé le 22 novembre 2026.** Remotoriser la main et le poignet sur le dessin V3 de table. Remplacer les quinze servos individuels des doigts par un tambour et une traverse à cinq tendons. Prévoir les rappels élastiques et un réglage par doigt.
- **Choix de r01.** Un MG996R à l’épaule, trois MG90S pour le coude, le roulis et le tambour. Socle orientable à la main. Commande Nano 5 V et bloc secteur. Priorité à la prise groupée et à la rotation. [[02_Conception_Fusion/MAIN_POIGNET_ECO|Implantation, budget et essais]].

## ADR-016 — Carte Nano classique et répartition externe pour la r02

- **Date** 23 novembre 2026.
- **Choix** Arduino Nano classique **A000005** comme alternative d’achat au Joy-IT ARD_NANOV3P. Le format 45 × 18 mm, le mini-USB B, l’ATmega328P 16 MHz et les broches à 5 V correspondent à la platine et au firmware.
- **Distribution** Trois WAGO 221-415 dans un boîtier externe pour les quatre servos et la masse logique. Une borne pour le +5 V et deux bornes GND reliées par un pont en 0,75 mm². Conserver une coupure matérielle du rail.
- **Point ouvert** Le bloc et le fusible dépendent de la tension réellement mesurée aux servos et des appels de courant. [Références et contrôles](../../../archives/r02/kit/ACHATS_AMAZON_R02.md)

## ADR-017 — Retenir six servos pour AURA-01 r05

- **Date** — 24 novembre 2026.
- **Choix** — Fusion v2 séparée de la r04 v4. J1 SG90 à engrenage borné, J2/J3 MG996R avec axes portés, J7 manuel, trois commandes de main avec cinq emplacements. Pico sur USB et rail moteur 5 V / 8 A.
- **Motif** — Garder le socle pilotable, le pouce et l’index indépendants en visant 150 € TTC livré. Deux SG90 supplémentaires ouvrent la commande des cinq doigts après reprise du budget de courant.
- **Validation** — Contrôle CAO, courses, ajustement des plateaux et arrêt logiciel vérifiés numériquement. Les contrôles physiques restent ouverts. [[02_Conception_Fusion/TABLE_R05|Données r05]]

## ADR-018 — Redonner cinq commandes à la main dans la revue design V5

- **24 novembre 2026 · Appliqué à la variante pour revue.**
- Conserver le socle et la main V5 comme base. Reprendre l’indépendance des cinq doigts de la r04 par deux rangées de SG90. Donner au coude une transmission intégrée et au poignet un roulis coaxial. Regrouper les câbles sous les coques.
- Le design gagne en finesse transversale et allonge l’entraxe pour rentrer cinq moteurs et un roulis dans l’enveloppe. Le budget d’achat de la variante reste plafonné à 150 €. La validation du design et les essais de table conditionnent les travaux de fabrication. [[02_Conception_Fusion/TABLE_V5_REVUE_DESIGN|Variante et contrôles]]

## ADR-019 — Ajouter le roulis longitudinal à l’épaule et au coude de la V5

- **24 novembre 2026 · Appliqué à la variante pour revue.**
- Former à chaque articulation un axe de tangage et un axe longitudinal en série. Déporter les deux MG90S dans le socle et transmettre le mouvement par brins opposés sous gaine.
- Les paliers apportent 8 mm à chacun des deux entraxes. La modification reprend les volumes de carénage de la V5 revue avec un dégagement local pour le coude. Le prototype doit confirmer les pertes et la retenue au roulis avant qualification. [[02_Conception_Fusion/TABLE_V5_ROULIS|Décision et contrôles]]

## ADR-020 — Fixer les roulis intermédiaires et garder l’accès aux tangages

**25 novembre 2026 · V5-stabilisation.** Les deux colliers et leurs transmissions à gaines sont retirés. Le lacet J1 conserve le faisceau dans un axe creux. Les cinq doigts et J7 restent indépendants. Le plan de pose abaissé de 90 mm et les butées de J2/J3 améliorent la garde calculée. Les ressorts compensent le moment gravitaire. Le support extérieur vissé rend J3 accessible après désaccouplement des ressorts. Le montage physique doit caractériser la retenue et le jeu. [Rapport des corrections](../../../RAPPORT_CORRECTIONS.md) · [Notice de montage](../../../assembly/README.md)

## ADR-021 — Commander neuf voies avec armement local et coupure verrouillée

**25 novembre 2026 · V5-stabilisation.** Le Pico 2 vérifie la calibration, les deux retours analogiques de tangage et leur enveloppe couplée. La conception de puissance couple arrêt NC, verrouillage matériel, rail à coupure séparée et tampon PWM haute impédance à l’arrêt. Le calcul garde 11,30 A en pointe et dimensionne un bloc externe candidat. La chaîne réelle doit être éprouvée sur charge factice avant un moteur. [Électronique](../../../electronics/README.md) · [Firmware](../../../firmware/README.md)

## ADR-022 — Graphe orbital du coffre Obsidian

**25 novembre 2026 · Choix local.** Cyber Glow donne au coffre un thème sombre aux accents cyan. La vue Graph Styler adopte Galaxy, Deep Space et la disposition Orbital autour de `00_DASHBOARD.md`. Les étoiles représentent les notes existantes. Les cinq familles gardent leur périmètre avec une palette adaptée au fond sombre.

**Accès et restauration.** Ouvrir **Ctrl+P → Graph Styler: Open 3D graph**. La configuration active est dans `.obsidian/`. Le bouton **Restore original** de Graph Styler rétablit les réglages du graphe sauvegardés lors de la première application du préréglage. Le thème Wasp reste sélectionnable dans **Paramètres → Apparence** et l’extrait **AURA - Nebuleuse** est désactivable sous **Extraits de CSS**. [Source de l’extrait](../assets/aura-nebuleuse.css) · [[09_Gestion/JOURNAL#2026-11-25 — Graphe orbital du coffre|Journal]]

## Template

### ADR-XXX — <titre>
- **Date :** YYYY-MM-DD.
- **État :** PROPOSÉ / DÉCIDÉ / REJETÉ.
- **Contexte :** ...
- **Choix :** ...
- **Alternatives :** ...
- **Conséquences :** ...
- **Validation :** ...
