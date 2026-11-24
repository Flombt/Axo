# Plan de travail mécanique Fusion

Référence à partir de la [[README#04 — Morphologie cible et degrés de liberté|section Morphologie]] du cahier des charges (sections 04 à 13). Voir aussi les [[09_Gestion/ADR#ADR-002 — 5 axes et pince en V1|choix de cinématique]], le [[03_Impression_3D/PROTOCOLes_FDM|protocole FDM]] et la [[08_Tests/MATRICE_TESTS|matrice de validation]].

## Phase 0 — Audit et sauvegarde

1. Versionner `Assemblage final`.
2. Recenser composants, corps, liaisons et cube temporaire éventuel.
3. Comparer axes présents à J1…J5/G1.

L’[[02_Conception_Fusion/audit_initial|audit Fusion de la v5]] consigne la sauvegarde, les mesures, les 46 poses testées et les priorités V2.

## Phase 1 — Cinématique après validation de l’audit

4. Définir les paramètres utilisateur et pivots réels.
5. Corriger base et liaisons sans détruire l'original.
6. Tester HOME, extrêmes et collisions.

## Référentiel rapide

- J1 yaw base ; J2 épaule ; J3 coude ; J4 poignet pitch ; J5 poignet roll ; G1 pince.
- Base diamètre 160 mm, segments 135 et 120 mm : **hypothèses**, non dimensions validées.
- Source CAO : Fusion natif ; projet `Robotic Arm — V1`, document `Assemblage final`.
- État de fabrication : non validé.

## V2 — Prototype mécanique enregistré

Le document `AURA-01 — V2 — Prototype mécanique`, révision v5, est enregistré dans `Robotic Arm — V1 / AURA-01 — Conception V2`. Il a été rouvert en position HOME le 21 novembre 2026 dans Fusion 2706.1.17. L’assemblage comprend 46 occurrences, dont 40 solides de pièces et six volumes de réservation masqués. Les 35 définitions de composants sont reliées par 45 liaisons telles que construites. Un lien de mouvement couple les deux glissières de pince. [Ouvrir le document dans Fusion](https://epitech619.autodesk360.com/g/projects/202611211172950976/data/dXJuOmFkc2sud2lwcHJvZDpmcy5mb2xkZXI6Y28uaUVGeHVyMi1TZTJsX2U3QkkzZThUZw/dXJuOmFkc2sud2lwcHJvZDpkbS5saW5lYWdlOlRfZVpZNERUVDdHU3REdkRxTll2alE).

![[assets/fusion_aura_v2_home_2026-11-21.png|800]]

### Restauration et indépendance

L’archive de la v5 a été réimportée dans le dossier cloud séparé `AURA-01 — Restauration v5`. `Assemblage final` s’y ouvre avec huit références prêtes et indépendantes, huit solides, sept liaisons, une base ancrée dans Fusion et aucune interférence volumique au neutre. Son enveloppe correspond à celle de la v5 auditée à l’arrondi, soit 252,61 × 96,00 × 141,23 mm. La copie de travail a été réimportée séparément depuis la même archive. Après remplacement du poignet et de la pince, la V2 charge les six références utiles de sa propre copie. Elles sont enregistrées dans leur propre révision v2 avec la palette du prototype. La source cloud reste en v5 et ses huit fichiers liés conservent leurs révisions. L’[[02_Conception_Fusion/audit_initial#Révision et sauvegarde|audit initial]] contient le chemin et l’empreinte de l’archive.

### Interfaces mécaniques et maintenance

La V2 conserve le socle Ø96 mm et les entraxes épaule–coude de 100 mm et coude–interface du poignet de 84 mm. Les dimensions de départ du README restent des hypothèses. Les efforts passent par le squelette graphite. Deux coques bleu glacier, des articulations à l’aspect titane et des garnitures corail reprennent la [[README#03.1 — Palette visuelle initiale, entièrement modifiable|palette AURA-01]].

| Sous-ensemble | Composition et données CAO |
|---|---|
| Socle et J1 | Base et épaule héritées. Couronne démontable Ø91 extérieur et Ø60 intérieur sur quatre entretoises de 9,75 mm. Recouvrement radial nominal de la collerette de 1,00 mm et garde axiale de 0,40 mm. Quatre vis indicatives et passages de Ø4,50 mm. Le montage sur un support rigide reste à dimensionner. |
| Épaule J2 et bras supérieur | Géométrie et axe conservés. Deux rondelles de 2,25 mm laissent 0,25 mm de jeu axial de chaque côté. Le jeu radial du pivot hérité reste à 0,10 mm en CAO. |
| Coude J3 et avant-bras | Géométrie et axe conservés. Deux rondelles de 2,05 mm laissent également 0,25 mm de jeu axial par côté. Jeu radial hérité de 0,10 mm. Quatre perçages de Ø3,30 mm s’alignent sur la bride J4. |
| Poignet J4 | Chape séparée, support inclinable, axe métal Ø5 mm sur alésages Ø5,50 mm et circlip indicatif dans sa gorge. Les passages de tige Ø3,30 mm et les accès de tête Ø5,70 mm restent dégagés au montage de la chape. L’ouverture nominale de la fourche est de 19 mm pour 17,50 mm au pivot interne. |
| Poignet J5 | Rotor indépendant et coaxial, portée Ø15 dans Ø15,50 mm, conduit traversant Ø6 mm et flasque de retenue Ø24 mm. Deux demi-colliers vissés capturent le flasque et se retirent latéralement. Quatre passages Ø2,80 mm relient le plateau au berceau de pince. |
| Pince G1 | Berceau indépendant, deux mors guidés sur deux tiges métal Ø3 mm, alésages Ø3,50 mm et deux garnitures corail démontables de 1,20 mm. Course par mors de 12 mm, ouverture mesurée entre garnitures de 1,60 à 25,60 mm, dont 13,60 mm à HOME. Le lien 1:1 impose le déplacement symétrique dans Fusion. L’enveloppe de vis à pas opposés et les poches d’écrous sont modélisées. Les filetages, écrous, paliers, retenues axiales des tiges, butées physiques et l’entraînement restent à spécifier. |
| Coques et fixations | Deux coques galbées de 1,80 mm nominal, avec contre-appuis sous les ajours du squelette, lamages de Ø3,80 mm et échancrures de câble. Les coques sont amovibles. L’épaulement des vis, les inserts éventuels et la tenue des douilles restent à qualifier au montage à blanc. |

Les axes de montage ont été contrôlés à HOME dans Fusion avec des cylindres de gabarit. Accès par le haut aux quatre fixations J1 avec Ø9 mm et aux quatre points des coques avec Ø3,50 mm. Accès latéral aux deux demi-colliers J5 avec Ø3,50 mm et aux quatre points des garnitures avec Ø3,40 mm. La bride J4 accepte les gabarits de tige Ø3 mm et de tête Ø5,50 mm après retrait de son sous-ensemble pivotant. L’accès à la bride G1 accepte Ø3,50 mm après retrait des guides, de la vis et des mors. Le gabarit d’extraction de l’axe J4 rencontre la réserve moteur. Prévoir un support d’actionneur déposable avant de sortir l’axe. Ces gabarits contrôlent les dégagements droits et servent à définir l’ordre de montage. [API Autodesk des corps temporaires](https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/fusion_TemporaryBRepManager.htm).

### Contrôles Fusion

| Mouvement | Type et limite programmée |
|---|---|
| J1 | Rotation verticale ±80° |
| J2 | Épaule autour de l’axe transversal, −32° à +6,5°. La valeur positive abaisse le bras. |
| J3 | Coude autour de l’axe transversal, −38° à +18° |
| J4 | Inclinaison autour de l’axe de l’axe métal, ±30° |
| J5 | Roulis autour de l’axe du rotor, ±65° |
| G1 | Translation couplée des deux mors, ±6 mm chacun. Positif à l’ouverture. |

- 226 configurations distinctes pilotées dans Fusion, couvrant 24 poses isolées sur les commandes, 64 combinaisons de limites, 137 états sur dix transitions et une configuration étendue supplémentaire. Le plan d’appui est Z = 0 et les 40 solides de pièces et les six gabarits ont été inclus dans l’analyse d’interférences. Aucune intersection volumique détectée aux échantillons au seuil de 0,00002 mm³. Le socle est resté fixe et la hauteur minimale de l’ensemble mobile est de 5,53 mm.
- La borne basse de l’épaule a été ramenée de +21° à +6,5° après passage sous le plan d’appui à +21° et une garde de seulement 0,30 mm à +8°. La combinaison la plus proche à +6,5° est `[−80°, +6,5°, +18°, +30°, −65°, +6 mm]`, en ordre J1 à G1.
- HOME est à zéro sur les six commandes. La configuration étendue correspond à `[0°, +6,5°, 0°, 0°, 0°, 0 mm]` et la configuration repliée est représentée par Peur. Les huit valeurs de référence sont enregistrées dans Fusion et détaillées dans la [[04_Animation_Emotion/ANIMATIONS#V2 — Poses de référence|bibliothèque de poses]].
- Le document compte 45 paramètres nommés. Lors d’un recalcul, `pivot_radial_clearance` de 0,25 à 0,30 mm a porté les alésages J4 de Ø5,50 à Ø5,60 mm, J5 de Ø15,50 à Ø15,60 mm et G1 de Ø3,50 à Ø3,60 mm. `cover_wall` de 1,80 à 1,90 mm a augmenté le volume de la coque testée. Les valeurs nominales ont été rétablies. `j2_lowering_max` commande la limite réelle de J2.
- Les transitions ont été échantillonnées avec un profil quintique. Les volumes balayés en continu, la torsion du faisceau, les efforts et le comportement d’une commande motorisée restent à valider. Consulter la [[08_Tests/MATRICE_TESTS#V2 — Contrôles de la conception mécanique|matrice V2]].

### Motorisation et stabilité

| Commande | Réserve CAO locale (mm) | Masse supposée | Intégration à étudier |
|---|---|---:|---|
| J1 | 21,5 × 22 × 20 | 75 g | Réserve déportée derrière le socle. Transmission et fixation au support à concevoir. |
| J2 | 22 × 17 × 22 | 65 g | Réserve latérale sur l’épaule. Couple de maintien et support en priorité. |
| J3 | 22 × 16 × 19 | 55 g | Réserve latérale sur le bras supérieur. Vérifier le déport et la masse réelle. |
| J4 | 19 × 14,7 × 20 | 33 g | Réserve latérale sur la chape. Prévoir son démontage avant l’extraction de l’axe. |
| J5 | 19 × 18 × 13,3 | 28 g | Réserve sous le palier. Conserver le passage axial des câbles. |
| G1 | 17 × 16 × 15 | 24 g | Réserve dans l’axe de la vis. Prévoir l’accouplement et la limitation d’effort. |

Le pré-dimensionnement utilise les volumes et centres des solides Fusion, du polymère supposé plein à 1,27 g/cm³, de l’acier à 7,85 g/cm³ pour les axes, guides, vis et circlip, de l’aluminium à 2,70 g/cm³ pour le rotor et les demi-colliers, les six masses du tableau et une charge de 100 g au centre de prise. La masse totale de ce scénario est de **0,664 kg**.

| Configuration | J1 (N·m) | J2 (N·m) | J3 (N·m) | J4 (N·m) | J5 (N·m) | Projection du centre par rapport à J1 |
|---|---:|---:|---:|---:|---:|---:|
| HOME | 0,000 | 0,579 | 0,342 | 0,095 | 0,009 | 82,14 mm |
| Étendue | 0,000 | 0,606 | 0,342 | 0,095 | 0,009 | 86,20 mm |
| Joie | 0,000 | 0,474 | 0,293 | 0,070 | 0,004 | 66,25 mm |
| Repliée · Peur | 0,000 | 0,394 | 0,278 | 0,093 | 0,009 | 53,97 mm |

La projection du centre de gravité dépasse le rayon d’appui de 48 mm à HOME et en extension sous cette hypothèse. Dimensionner un ancrage, un support élargi ou un lest vérifié avant essai chargé. Le moment gravitaire de J1 est nul autour de la verticale. Son actionneur dépend de l’inertie, des accélérations, des frottements et de la transmission. Pour J2–J5, compléter le couple statique par ces contributions et vérifier la tenue continue et thermique. Pour G1, déterminer les efforts de prise et de pincement à partir des objets, du pas opposé, du rendement et des garnitures. Les réserves constituent des enveloppes provisoires. Références constructeur, fixations, transmission, dissipations et câblage restent à détailler.

### Préparation FDM

Les 21 fichiers 3MF de pièces séparées sont dans `Exports_Fusion/AURA-01_V2_3MF`, à la racine du projet Aura. Les fichiers portent des noms de pièces et des unités en millimètres. Contrôle des maillages fermés, des arêtes et des dimensions par rapport aux solides Fusion. L’écart maximal sur les dimensions d’enveloppe est de 0,026 mm. Les entretoises J1 sont à prévoir en quatre exemplaires, les rondelles J2 et J3 en deux exemplaires chacune et les contre-appuis de coque en quatre exemplaires. Les axes, tiges guides, vis, circlip et réserves moteur sont gérés à part. [Export 3MF natif Fusion](https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/fusion_ExportManager_createC3MFExportOptions.htm).

Orientations à comparer dans le slicer avec la machine et le filament retenus.

- Socle et couronne à plat sur leur face d’appui. Vérifier les logements et la reprise des fixations du support.
- Bras supérieur et avant-bras couchés sur une face longue pour garder des couches dans le sens du segment. Contrôler les perçages transversaux et l’orientation des efforts au pied des oreilles.
- Chape J4 sur une face latérale ou sur la bride selon le résultat pour les couches et les trous. Contrôler la matière résiduelle des oreilles près des quatre dégagements. Coucher les demi-colliers sur leur face de séparation. Réaliser un coupon de portée J5 et étudier le palier réel.
- Berceau sur sa semelle, mors sur leur flanc large et garnitures à plat. Vérifier le parallélisme des guides, l’ancrage des écrous et la flexion en bout de mors.
- Coques ouvertes vers le plateau sur les bords stables. Vérifier les supports dans les douilles et le nombre de périmètres autour des lamages. Contrôler l’écartement des câbles autour de J4 et la torsion à J5 avec le faisceau réel.

Les jeux restent provisoires. Suivre [[09_Gestion/TACHES#AURA-004 — Valider les interfaces d’impression|AURA-004]] pour le tranchage, les coupons près de 0,10/0,25 mm radiaux, les ajustements de vis et les inserts, le montage à blanc et les essais en charge. Les alésages hérités J2/J3, les oreilles J4, les lèvres du collier J5 et l’alignement de la pince sont les points d’inspection prioritaires.

## AURA-004 — Assemblage de travail motorisé

Le document `AURA-01 — V2 — Motorisation et fabrication` est une copie cloud séparée, réalisée depuis la V2 mécanique v5 dans `Robotic Arm — V1 / AURA-004 — Motorisation et fabrication`. La révision v3 a été enregistrée et rouverte à HOME. Les pièces qui reçoivent de nouveaux usinages sont locales à cette copie. Le fichier V2 v5 reste la référence des poses d’origine et des 21 maillages. [Ouvrir la copie dans Fusion](https://epitech619.autodesk360.com/g/projects/202611211172950976/data/dXJuOmFkc2sud2lwcHJvZDpmcy5mb2xkZXI6Y28uSzhxSGlxR2FTaEtWYVdiN3Z3UlE0Zw/dXJuOmFkc2sud2lwcHJvZDpkbS5saW5lYWdlOjdIeHNmM0tfUTNxbkh0MDNITFRsOXc).

Le 22 novembre, l’assemblage a été rouvert dans l’application Fusion et exporté dans `Sauvegardes_Fusion/AURA-004_Motorisation-fabrication_2026-11-22.f3z` depuis la racine Aura. Le manifeste associe le document racine à la révision **v3** et à deux références v2. L’archive de 5 135 344 octets a passé le contrôle d’intégrité ZIP. Son SHA-256 est `e6b5e9fdf24e61a22a8f9bb8074b184b30e874c9e3fc6ee3f89ab636942d501a`. Le réimport de cette archive locale reste à tester si une restauration est nécessaire. Le journal précise le mode d’accès. [[09_Gestion/JOURNAL#2026-11-22 — AURA-004 reprise et préparation atelier|Preuves de la reprise]].

![[assets/fusion_aura004_home_2026-11-21.png|850]]

### Plaque et ancrage démontable

- Plaque en aluminium 6082 de **260 × 220 × 8 mm**, quatre passages **Ø6,6** pour M6 aux coordonnées (±110, ±90 mm), quatre liaisons M4 du socle à (±28, ±28 mm) et logements hexagonaux côté dessous. Quatre tubes Ø14 × 52 mm laissent le passage au moteur J1. Les têtes et accès se démontent par le haut de la couronne et par le dessous de la plaque selon la visserie finale.
- La masse calculée de l’ensemble avec plaque est d’environ **2,33 kg** dans le scénario avec charge de 100 g et provision de 25 g pour câbles et quincaillerie mobile. La plaque pèse environ **1,23 kg** dans ce calcul. La projection du centre avec la plaque reste à environ 31 mm de J1 au maximum sur les chemins vérifiés. Le bras sans la masse de la plaque atteint environ **66 mm** alors que le socle Ø96 n’offre que 48 mm de rayon d’appui.
- Garde statique de projection jusqu’au bord de la plaque **environ 99 mm au minimum** sur les chemins vérifiés. Moment de rappel statique conservatif de la plaque posée avec le bras d’environ **2,27 N·m**. Un effort latéral de 20 N appliqué à 0,32 m du plan d’ancrage produit **6,4 N·m**. Cela motive l’ancrage rigide et un essai au support réel. Un lest seul demanderait plus de masse et un contrôle du glissement.
- Pour la vérification préliminaire, la sollicitation de calcul vaut **7,2 N·m en renversement, 20 N en translation et 5,0 N·m autour de la verticale**. Le moment autour de la verticale prend 0,25 m de bras de levier pour l’effort latéral. La répartition élastique à quatre fixations donne jusqu’à **91 N en traction et 37 N en cisaillement par M4**, ou **26 N et 14 N par M6**. En traction, le calcul utilise `F_i = Mx·y_i/Σy² + My·x_i/Σx²`, avec orientation la plus défavorable et sans déduire le poids. Le cisaillement combine `H/4` et `Mz/(4r)`. Couples de serrage, épreuve d’arrachement et rigidité du plan de travail restent à qualifier.

### Implantation et transmissions

| Axe | Réalisation dans la copie | Vérification et point ouvert |
|---|---|---|
| J1 | XL430 sous le socle, berceau sur la plaque, arbre Ø8 traversant un coussinet rapporté et pont à carré dans l’épaule. Moyeu à méplat et fixation radiale. | Liaison coaxiale et dégagement du berceau contrôlés. Enveloppe constructeur simplifiée. Empreinte du palonnier réel et pointeau à qualifier. |
| J2 | XM540 déporté côté épaule. Support démontable repris aux perçages de la chape. Arbre acier Ø6 à double méplat et manchon claveté dans le bras. | Les flancs du double méplat transmettent le couple à la pièce mobile. La chape porte l’axe. Lumières de montage et plan constructeur à confronter au palonnier reçu. Tenue des trous et retenue axiale à éprouver. |
| J3 | XM430 latéral côté coude. Arbre Ø5 à double méplat, manchon indexé et accouplement côté avant-bras. | Même chemin de reprise d’effort, avec support et accès aux vis. Les perçages et longueurs de vis du servo restent à relever sur pièce. |
| J4 | XC330-T288 avec boîtier et palonnier du STEP ROBOTIS, cassette ajourée à quatre points M2 et arbre Ø5 à double méplat. | Empreinte du boîtier et du palonnier mesurée dans le STEP. Déposer la cassette avant extraction de l’axe. Vérifier la retenue axiale et la résistance de la chape. |
| J5 | XC330-T288 décalé sur une bride. Pignon 18 dents et couronne 42 dents, module 0,8. Assise de la couronne au niveau de la bride G1 et conduit axial conservé. | Réduction 42/18, sens inversé, entraxe CAO 24,12 mm. Commander −42° au pignon a donné +18° au rotor dans Fusion. Mesurer jeu, fixation antirotation, usure et bruit. |
| G1 | XC330-T181, cassette ajourée, liaison de palonnier, vis Ø4 à avance 2 mm et deux écrous hexagonaux en poche. Deux guides métal indépendants reprennent les efforts latéraux. | En commandant la vis par incréments, 360° ont déplacé chacun des mors de 2 mm en sens opposé et 720° de 4 mm. Filets représentés par leur enveloppe. Filet gauche/droit, retenues axiales des écrous et guides, force et limitation de course à spécifier avec l’usinage. |

Le STEP XC330 est le fichier constructeur identifié par SHA-256 `e2f7b060801a1d6a21f23bca2554f29a402f7d73b8498cb201c9e6adf3139eb6`. Les alésages du carter et du palonnier ont été relevés dans Fusion. Les téléchargements STEP des trois autres références ont échoué depuis le poste. Les enveloppes de catalogue et les joues du berceau modélisent leur intégration, avec empreintes de fixation et connecteurs à vérifier avant usinage des supports. [Plans XC330](https://emanual.robotis.com/docs/en/dxl/x/xc330-t288/#drawings), [Plans XM430](https://emanual.robotis.com/docs/en/dxl/x/xm430-w350/#drawings), [Plans XM540](https://emanual.robotis.com/docs/en/dxl/x/xm540-w270/#drawings), [Plans XL430](https://emanual.robotis.com/docs/en/dxl/x/xl430-w250/#drawings).

### Couples et vitesses de premier dimensionnement

Les volumes et centres Fusion sont pondérés à 1,27 g/cm³ pour le polymère plein, 1,20 pour les garnitures, 2,70 pour l’aluminium, 7,85 pour les arbres et vis acier et 8,50 pour les écrous/coussinet. Les moteurs utilisent leur masse de fiche. Les inerties utilisent les distances à l’axe et une majoration fondée sur la demi-diagonale du corps. Le calcul avec charge de **100 g** inclut des nombres de servos réels et des masses de quincaillerie provisoires. Les maxima viennent de 99 configurations de dix transitions et d’une pose étendue.

| Axe | Statique au joint N·m | Terme dynamique + frottement N·m | Cible au joint avec marge N·m | Cible au moteur N·m | Vitesse moteur cible tr/min | Indice de courant A |
|---|---:|---:|---:|---:|---:|---:|
| J1 | 0,000 | 0,094 | 0,141 | 0,141 | 5,8 | 0,13 |
| J2 | 0,738 | 0,098 | 1,253 | 1,253 | 4,0 | 0,53 |
| J3 | 0,390 | 0,063 | 0,679 | 0,679 | 5,0 | 0,38 |
| J4 | 0,104 | 0,036 | 0,211 | 0,211 | 7,0 | 0,18 |
| J5 | 0,019 | 0,020 | 0,059 | 0,030 | 28,0 | 0,03 |
| G1 | 0,018 | 0,010 | 0,042 | 0,042 | 48,0 | 0,04 |

L’accélération et le frottement sont des hypothèses. Le terme additionnel est `1,3·I·α + T_f`. La majoration de 30 % du terme inertiel couvre une première estimation des couplages d’axes. Les frottements retenus de J1 à J5 valent 0,070 / 0,080 / 0,055 / 0,035 / 0,020 N·m. Le facteur de service **1,5** porte sur l’ensemble du moment estimé pour les incertitudes de masse, de frottement et de montage. Pour J5, rendement de transmission supposé de 0,85. Pour G1, hypothèse de 8 N par mors, rendement 0,28, avance 2 mm et terme additionnel de 0,010 N·m. Le rapprochement `(T moteur / T blocage) × I blocage` est un indice de charge électrique. Dimensionner l’alimentation avec les courants publiés de pointe, puis relever les valeurs réelles au banc.

Objectifs de profil en sortie **35, 24, 30, 42 et 72°/s**, puis **1,6 mm/s** par mors. Viser un incrément de commande ≤0,25° par pivot et ≤0,10 mm par mors. À la réception, viser ≤1° d’écart répété sur J1 et J4, ≤0,75° sur J2, J3 et J5, et ≤0,15 mm pour G1 à froid puis à chaud. Le pas d’encodeur théorique après réduction J5 est de 0,0377° et celui de G1 vaut 0,00049 mm pour 2 mm par tour. Vérifier la précision réellement obtenue au joint. Le jeu de denture, l’hystérésis, la précision effective, le bruit, l’échauffement et le couple continu ne sont pas mesurés. Pour J2 et J3, tester le maintien à l’effort réel, la descente freinée, la reprise de position et la chute éventuelle hors tension. Pour J4 et G1, surveiller l’échauffement de la cassette et du servo. La [[05_Electronique/NOMENCLATURE_AURA004|nomenclature]] compare les références et coûts. Le [[03_Impression_3D/PROTOCOLes_FDM#AURA-004 — Fabrication préparée|plan FDM]] détaille les pièces de série et coupons.

La [[08_Tests/MATRICE_TESTS#AURA-004 — Essais de la branche motorisée|matrice]] sépare le pilotage et les collisions échantillonnées des essais physiques. Avant mise sous tension du bras complet, éprouver l’ancrage, le mécanisme de retenue gravitaire, le faisceau, la coupure et les butées. Prévoir un montage à blanc de la vis G1 et une mesure de force. Les couples utiles se valident à la vitesse et au cycle de travail prévus.
