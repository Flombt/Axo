# README moteurs — AURA-01 V3

## AURA-01 V5 · Roulis épaule et coude

| Repère | Revue design v2 | Variante à deux axes de roulis | Qté | Enveloppe et course |
|---|---|---|---:|---|
| J2R | Épaule à axe de tangage seul | MakerMind MG90S de position, RBS11204 | 1 | 22,8 × 12,2 × 28,5 mm, 13,4 g, monté dans le socle. Tambour ±60° et roulis ±20°. |
| J3R | Coude à axe de tangage seul | MakerMind MG90S de position, RBS11204 | 1 | Même gabarit, tambour ±72° et roulis ±24°. |
| P, I, M, A, U | Tower Pro SG90 RBS15198 | SG90 MakerMind 23 × 12,2 × 29 mm pour le panier économique | 5 | Servo de position individuel. Gabarit des oreilles et palonnier à présenter au montage. |

Couple au blocage MG90S annoncé de 1,8 kgf·cm à 4,8 V. Réduction par tambours 3:1. Le calcul sans objet saisi donne 0,034 N·m à l’épaule et 0,007 N·m au coude dans les poses échantillonnées. Le couple de service dépend de la friction et de la précontrainte des gaines. Le rail de mise au point est 5 V / 10 A pour des essais avec mesure. L’hypothèse de pointe cumulée est de 11,3 A, donc l’enveloppe de simultanéité et l’alimentation définitive restent à établir. [MG90S](https://www.makermind.fr/p/servomoteur-micro-mg90s) · [SG90 de la main](https://www.makermind.fr/p/servomoteur-micro-sg90-9g-pour-modelisme-rc-avion-projets-arduino) · [Budget](../../../purchases/NOMENCLATURE.md) · [[02_Conception_Fusion/TABLE_V5_ROULIS|Implantation]]

## AURA-01 V5 · Revue design

| Repère | Référence économique r05 | Variante à valider | Qté | Implantation |
|---|---|---|---:|---|
| J1 | Tower Pro SG90 analogique | Tower Pro SG90 analogique RBS15198 | 1 | 23 × 12,2 × 29 mm, réduction 38/22 et course CAO ±88° au socle |
| J2 | Tower Pro MG996R 180° | MG996R 180° de position, Atelier de la Robotique | 1 | 40,7 × 19,7 × 43 mm annoncés, corps vertical, réduction 54/18 et ±21° à l’épaule |
| J3 | Tower Pro MG996R 180° | MG996R 180° de position, Atelier de la Robotique | 1 | Même gabarit, corps dans le longeron, réduction 36/18 et ±32° au coude |
| J7 | Serrage M5 manuel | Tower Pro SG90 analogique RBS15198 | 1 | Servo couché, entraînement direct et palier coaxial pour ±32° de roulis |
| P, I, M, A, U | Trois Tower Pro SG90 pour P, I et MAU | Cinq Tower Pro SG90 analogiques RBS15198 | 5 | Deux rangées et une gorge de traction par doigt |

Le couple au blocage annoncé à 4,8 V est de 1,8 kgf·cm pour le SG90 et de 13 kgf·cm pour le MG996R retenu. Le couple de service et le gabarit d’oreilles sont à vérifier sur le lot. Le courant de pointe de calcul de 9,5 A repose sur 7 × 0,90 A et 2 × 1,60 A. Le rail moteur prévu est de 5 V / 10 A et la commande Pico est alimentée par USB avec masse commune. [SG90](https://towerpro.com.tw/product/sg90-analog/) · [MG996R 180°](https://www.atelierdelarobotique.fr/produit/servomoteur-numerique-mg996r-15-kg-cm) · [Panier](../../../archives/v5-revue/ACHATS.md) · [[02_Conception_Fusion/TABLE_V5_REVUE_DESIGN|Implantation et résultats CAO]]

## AURA-009 table r05 · Fusion v2

| Repère | r04 | r05 | Qté | Conditions |
|---|---|---|---:|---|
| J1 | NEMA 17 | Tower Pro SG90 analogique de position | 1 | Gabarit 23 × 12 × 29 mm, 9 g, engrenages polymère, 38/22, course moteur ±51°. |
| J2 | MG996R | Tower Pro MG996R 180° de position | 1 | 40,7 × 19,7 × 42,9 mm, 55 g, rapport 3:1. |
| J3 | ROBOTIS DYNAMIXEL XC330-M288-T | Tower Pro MG996R 180° de position | 1 | Même gabarit, rapport 2:1, PWM. |
| J7 | MG90S | Serrage M5 manuel | 0 | Course CAO ±15°. |
| P, I et MAU | Cinq KST X06 V6.0 | Tower Pro SG90 analogique de position | 3 | Cinq emplacements sous l’avant-bras, P et I indépendants. |

Le MG996R est annoncé à 9,4 kgf·cm et le SG90 à 1,8 kgf·cm au blocage à 4,8 V. Budget provisoire de 1,60 A par MG et 0,90 A par SG, soit 6,80 A sur le rail moteur externe 5 V / 8 A. Pico séparé sur USB. Couple de service, courant, température et coupure attendent le banc. [SG90](https://towerpro.com.tw/product/sg90-analog/) · [MG996R](https://towerpro.com.tw/product/mg996r/) · [Panier](../../../archives/r05/LISTE_ACHATS_R05.md) · [[02_Conception_Fusion/TABLE_R05|Implantation]]

## AURA-009 table r04 · Fusion v4

- J1 passe du secteur manuel au **StepperOnline 17HS08-1004S**, 1 moteur fixe de 140 g, pignon 20 / couronne 88. Le couple de maintien constructeur n’est pas un couple disponible en mouvement. [Fiche StepperOnline](https://www.omc-stepperonline.com/download/17HS08-1004S.pdf)
- T1 commun MG90S remplacé par **5 KST X06 V6.0**, un par doigt. Corps 20 × 7 × 16,6 mm, 6 g, PWM et 6 V. 0,04 N·m nominal, 0,22 A nominal et 0,58 A au blocage par voie. [Fiche KST](https://robu-prod-media.s3.ap-south-1.amazonaws.com/uploads/2024/02/X06_V6.0_Technical_Specifcation.pdf)
- J2 MG996R, J3 XC330 TTL et J7 MG90S restent montés. La partie tournante requiert sept PWM et un TTL. Deux départs 24 V par collecteur, puis rails 5 V et 6 V. Le dimensionnement thermique et les transitoires attendent l’essai. [Rapport de fabrication](../../../archives/r04/VALIDATION_FABRICATION.md)


## AURA-009 de table r03 — Motorisation de référence

| Repère | Référence r02 | Référence r03 | Qté | Interface |
|---|---|---|---:|---|
| J2 épaule | TowerPro MG996R de position | TowerPro MG996R de position | 1 | PWM, support traversant M2,5 et arbre porté |
| J3 coude, MTR-02 | TowerPro MG90S de position | ROBOTIS DYNAMIXEL XC330-M288-T, 902-0173-000 | 1 | TTL demi-duplex, protocole 2.0, rail nominal 5 V |
| J7 roulis | TowerPro MG90S de position | TowerPro MG90S de position | 1 | PWM, cassette et arbre sur deux roulements |
| T1 main | TowerPro MG90S de position | TowerPro MG90S de position | 1 | PWM, traverse à cinq réglages |

**J3.** Corps 20 × 34 × 26 mm, 23 g. Alimentation constructeur 3,7–6,0 V. À 5 V, 0,93 N·m et 1,8 A au blocage, 81 tr/min à vide. Le maintien continu et le cycle exigent un essai thermique et mécanique. L’implantation CAO utilise le STEP constructeur et l’interface de palonnier Ø12. La chaîne structurelle passe par l’arbre Ø5 et ses bagues. [Fiche et plan ROBOTIS](https://emanual.robotis.com/docs/en/dxl/x/xc330-m288/) · [Référence constructeur](https://en.robotis.com/shop_en/item.php?it_id=902-0173-000)

**Puissance.** 4,2–5,2 A à 5 V au blocage simultané d’après les valeurs constructeur J2/J3 et une hypothèse de 0,5–1,0 A pour chaque MG90S. Cible de dimensionnement provisoire 6,5 A. Mesurer les pointes, chutes et retours d’énergie. Prévoir interface TTL demi-duplex et protections de puissance. La commande r02 est PWM et doit être adaptée. J1 reste indexable sans moteur. [MG996R](https://towerpro.com.tw/product/mg996r/) · [MG90S](https://towerpro.com.tw/product/mg90s-3/) · [[02_Conception_Fusion/TABLE_R03|Couples et preuves r03]]

## AURA-009 de table r02 — Référence historique

| Repère | Ancienne V3 complète | AURA-008 r01 et AURA-009 r02 | Qté |
|---|---|---|---:|
| J2 épaule | ROBOTIS XM540-W270-T | TowerPro MG996R de position, 40,7 × 19,7 × 42,9 mm | 1 |
| J3 coude | ROBOTIS XM540-W270-T | TowerPro MG90S de position, 22,8 × 12,2 × 28,5 mm | 1 |
| J7 roulis | ROBOTIS XC330-T288-T | TowerPro MG90S de position | 1 |
| T1, main | 15 KST X06 V6.0 | 1 TowerPro MG90S, tambour et tendons communs | 1 |

Quatre servos PWM sur rail 5 V candidat. Les couples de blocage à 4,8 V sont d’environ 0,92 N·m pour le MG996R et 0,18 N·m pour le MG90S. Mesurer le couple de maintien et le courant à l’essai. J1 est orientable à la main. [MG996R](https://towerpro.com.tw/product/mg996r/) · [MG90S](https://towerpro.com.tw/product/mg90s-3/) · [Achats et prix](../../../archives/v2/README_V2_ELEMENTS_A_ACHETER.md) · [[02_Conception_Fusion/MONTAGE_V3|Implantation et montage]].

## Références historiques de la V3 complète

Références de la V3 à trois segments et main indépendante. Les sources d’achat ont été consultées le 22 novembre 2026. Les quantités décrivent le bras complet. Le montage de chaque famille d’actionneurs reste à qualifier au banc.

La r03 standardise trois coques de phalange et garde les mêmes références. Le tranchage r03 estime environ 32 g de PETG par doigt avant retrait des bordures et ajout des moteurs. Peser le premier assemblage et mesurer le couple utile sur sa géométrie. [[03_Impression_3D/PROTOCOLes_FDM#AURA V3 r03 — Kit d’impression|Version de fabrication]]

## Références d’achat

| Articulation | Référence exacte | Quantité | Tension et interface visées | État et sources |
|---|---|---:|---|---|
| 5 doigts, 3 phalanges chacun | **KST X06 V6.0** | **15** | **6,0 V**, PWM de position | Empreinte utilisée pour les quinze logements. Couverture de 120° constructeur à étalonner. [Plan et fiche KST](https://www.kst-servo-shop.de/media/4b/63/fe/1749810623/KST_0053_X06_V6_Datenblatt_04_2025_de.pdf?ts=1751463826) · [Intermodel, réf. 263-X06-V6](https://www.intermodel.fr/servos/8933-micro-servo-x06-v6-hv-6gr18kg-kst-kst-servo-micro-hv-kst-x06.html) |
| J2 épaule et J3 premier coude | **ROBOTIS DYNAMIXEL XM540-W270-T**, 902-0137-000 | **2** | 11,1 V régulé, TTL, protocole 2.0 | Enveloppes CAO sur J2 et J3. Réduction et compensation du poids à dimensionner. [Fiche ROBOTIS](https://emanual.robotis.com/docs/en/dxl/x/xm540-w270/) · [Boutique ROBOTIS](https://en.robotis.com/shop_en/item.php?it_id=902-0137-000) |
| J1 socle, J4 second coude et J6 flexion du poignet | **ROBOTIS DYNAMIXEL XM430-W350-T**, 902-0124-000 | **3** | 11,1 V régulé, TTL, protocole 2.0 | Enveloppe présente sur J4. Fixations J1 et J6, réduction J4 et tenue en charge à qualifier. [Fiche ROBOTIS](https://emanual.robotis.com/docs/en/dxl/x/xm430-w350/) · [Génération Robots](https://static.generation-robots.com/en/402710-dynamixel-xm430-w350-t-servo.html) |
| J5 déviation et J7 roulis du poignet | **ROBOTIS DYNAMIXEL XC330-T288-T**, 902-0171-000 | **2** | 11,1 V régulé, TTL, protocole 2.0 | Candidats compacts. Empreinte et rapport de transmission à contrôler sur le poignet. [Fiche ROBOTIS](https://emanual.robotis.com/docs/en/dxl/x/xc330-t288/) · [Génération Robots](https://static.generation-robots.com/fr/403891-servomoteur-dynamixel-xc330-t288-t.html) |

Le KST est affiché à 40,90 € TTC chez Intermodel lors de la consultation, soit environ **614 € pour quinze** au même prix, hors port. Le premier essai demande un seul KST, son palonnier OEM et une phalange instrumentée. La version V6.0 doit figurer explicitement sur l’offre ou être confirmée par le vendeur. [Offre Intermodel](https://www.intermodel.fr/servos/8933-micro-servo-x06-v6-hv-6gr18kg-kst-kst-servo-micro-hv-kst-x06.html)

## Enveloppe, commande et couple de la main

- Le X06 V6.0 pèse 6 g nominalement. Le boîtier fait **20 × 7 × 16,6 mm**, avec environ **28 × 7 × 19,3 mm** pattes et sortie comprises. Le plan cote les deux perçages Ø2,2 mm à 24 mm d’entraxe et la sortie cannelée à 15 dents, nominale Ø4 mm. Utiliser le palonnier prévu pour cette sortie et un pivot passif coaxial du côté opposé. [Plan coté KST](https://www.kst-servo-shop.de/media/4b/63/fe/1749810623/KST_0053_X06_V6_Datenblatt_04_2025_de.pdf?ts=1751463826)
- À 6 V, KST annonce **0,039 N·m au régime nominal** (0,4 kgf·cm), **0,147 N·m au blocage**, 0,22 A nominal et 0,58 A au blocage. Pour quinze unités, la somme est de 3,30 A au nominal et 8,70 A au blocage théorique. Prévoir une distribution 6 V séparée, avec départs par doigt, limitation et marge sur les transitoires. Le retour de position du X06 est interne au servo. Ajouter un capteur externe si le contrôleur doit connaître la position réelle. [Performances et PWM KST](https://www.kst-servo-shop.de/media/4b/63/fe/1749810623/KST_0053_X06_V6_Datenblatt_04_2025_de.pdf?ts=1751463826)
- Utiliser quinze canaux PWM de position indépendants, référencés à la masse de la commande. Le bus TTL DYNAMIXEL du bras a son propre rail de puissance. Son ordre de grandeur cumulé au blocage est **16,3 A à 11,1 V** pour les sept références prévues. Les protections, le câblage distribué et les pointes mesurées déterminent le dimensionnement final. [Guide de sélection et alimentation ROBOTIS](https://emanual.robotis.com/docs/en/reference/dxl-selection-guide/)
- Pour le majeur, les volumes hors servo et axe relevés dans Fusion sont de 16,07, 13,89 et 11,26 cm³. En prenant 55 % de matière effective sur ces volumes, du PETG à 1,27 g/cm³, 6 g par servo et des centres de masse à 22, 78 et 125 mm du premier pivot, l’estimation est **0,033 N·m à l’horizontale à vide**. Avec 65 % de matière effective, elle atteint environ 0,037 N·m. Peser le premier doigt et vérifier couple, jeu et échauffement en cycle. La première cible est la gestuelle légère. [[02_Conception_Fusion/DESIGN_V3#Limites et dimensionnement d’atelier|Hypothèses V3]]

## Mise à jour à chaque changement de moteur

Modifier ce tableau dans la même intervention que le modèle. Indiquer le repère, l’ancienne et la nouvelle référence, les quantités, la tension, l’enveloppe, le palonnier, les sources et la date. Reporter le changement dans le générateur des volumes, la note CAO, le journal et, s’il change l’architecture, dans les ADR. Vérifier le logement avec les câbles en place, mesurer le débattement utile et recalculer le couple et le courant avant la mise à disposition de la nouvelle révision.

| Date | Révision | Changement |
|---|---|---|
| 2026-11-23 | AURA-009 de table r03 | MTR-02 passe du MG90S au XC330-M288-T. J3 TTL à 5 V, arbre porté. Quantité totale maintenue à quatre servos. |
| 2026-11-22 | V3 initiale | KST X06 V6.0 pour les quinze phalanges. Sept DYNAMIXEL candidats pour le socle, les trois segments et le poignet. |
| 2026-11-22 | Intégration mécatronique | Références moteur conservées. Banc J2 avec XM540-W270-T, HN13-N101, réduction 4:1 et frein d’arbre. Doigt pilote avec trois X06 V6.0, palonniers et guidages. |

Le X06 de la V3 est la variante à pattes classiques **BR0023.0144-V6**. Prix indicatif affiché au 22 novembre 2026, **39,99 USD** pièce, soit **119,97 USD** pour le doigt et **599,85 USD** pour 15, hors frais et taxes. Le palonnier en 7075 **TLS0082** est vendu par deux, 17 USD le kit. Il reste à confirmer l’ajustement sur un exemplaire. [KST X06](https://kstservos.com/products/x06-v6-0-hv-micro-digital-metal-gear-glider-1-8kg-torque-servo-motor) · [TLS0082](https://tomas-liu-studio.com/products/cha-servo-06-horn)

Les STEP ROBOTIS d’origine et les calculs de charge sont indiqués dans le [[02_Conception_Fusion/INTEGRATION_MECATRONIQUE_V3|rapport mécatronique]]. Le couple statique du frein de J2 et les couples de blocage ne démontrent pas le couple continu du servomoteur. Ajouter la courbe réelle du banc à la [[08_Tests/MATRICE_TESTS|matrice]] dès qu’une mesure est disponible.
