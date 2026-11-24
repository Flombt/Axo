# AURA-004 — Nomenclature de référence

Cette nomenclature correspond à la [[02_Conception_Fusion/CONCEPTION_MECANIQUE#AURA-004 — Assemblage de travail motorisé|branche de travail AURA-004]]. Les prix catalogue affichés sont des repères pour une unité, consultés pour la session du 21 novembre 2026. Confirmer le prix, la TVA, la livraison et le contenu du kit avant de figer une commande.

## Actionneurs

Données fabricant à **11,1 V**. Le couple et le courant au blocage sont des données de pointe. La vitesse est à vide. La résolution théorique des cinq servos J1–J5 est de 4 096 pas par tour moteur, soit 0,0879° au palonnier. Les jeux de la mécanique, les calibrations, le couple continu et le bruit restent à mesurer.

| Axe | Référence | Qté | Dimensions mm / masse g | Blocage N·m / A | Vitesse à vide | Catalogue TTC et disponibilité indicative |
|---|---|---:|---|---|---:|---|
| J1 | XL430-W250-T | 1 | 28,5 × 46,5 × 34 / 57,2 | 1,40 / 1,30 | 57 tr/min | 36,00 €. Délai annoncé de quatre semaines. [Fiche constructeur](https://emanual.robotis.com/docs/en/dxl/x/xl430-w250/) · [Vendeur](https://www.generationrobots.com/fr/355-dynamixel-serie-x) |
| J2 | XM540-W270-T | 1 | 33,5 × 58,5 × 44 / 165 | 10,0 / 4,20 | 28 tr/min | 489,96 € catalogue neuf. Disponibilité à reconfirmer. [Fiche constructeur](https://emanual.robotis.com/docs/en/dxl/x/xm540-w270/) · [Vendeur](https://www.generationrobots.com/fr/403368-servomoteur-dynamixel-xm540-w270-t.html) |
| J3 | XM430-W350-T | 1 | 28,5 × 46,5 × 34 / 82 | 3,80 / 2,10 | 43 tr/min | 317,40 € catalogue, 269,79 € affichés en promotion. Disponibilité annoncée fin janvier 2027. [Fiche constructeur](https://emanual.robotis.com/docs/en/dxl/x/xm430-w350/) · [Vendeur](https://static.generation-robots.com/en/402710-dynamixel-xm430-w350-t-servo.html) |
| J4 et J5 | XC330-T288-T | 2 | 20 × 34 × 26 / 23 chacun | 0,92 / 0,80 | 65 tr/min | 110,40 € par unité catalogue. Le vendeur affiche des délais variables dont fin janvier 2027. [Fiche constructeur](https://emanual.robotis.com/docs/en/dxl/x/xc330-t288/) · [Vendeur](https://www.generationrobots.com/fr/355-dynamixel-serie-x) |
| G1 | XC330-T181-T | 1 | 20 × 34 × 26 / 23 | 0,76 / 0,80 | 104 tr/min | 110,40 € catalogue. Délai à reconfirmer. [Fiche constructeur](https://emanual.robotis.com/docs/en/dxl/x/xc330-t181/) · [Vendeur](https://www.generationrobots.com/en/403890-dynamixel-xc330-t181-t-servo.html) |

**Sous-total moteurs catalogue. 1 174,56 € TTC**, hors expédition et accessoires. Variante de coût à étudier après mesure du couple continu de J2 et J3. Un ensemble d’occasion vendu sans vis change la visserie, la disponibilité et les critères d’inspection.

### Comparaison

- **Servos numériques retenus pour la CAO.** Bus commun, mesure interne de position, profils de mouvement et surveillance de défaut. Les XM 540/430 sont plus encombrants et coûteux. Les XC330 réduisent la masse au poignet et libèrent de la place pour les paliers. Les volumes de réservation V2 sont plus petits que les boîtiers retenus. Le nouveau montage utilise des supports déportés.
- **Motoréducteur DC à encodeur.** Exemple Pololu 4755, 100:1, 12 V, 210 g, Ø37 × 72,5 mm, 100 tr/min à vide, 5,5 A au blocage extrapolé. Le fabricant limite la charge continue du réducteur à environ 0,98 N·m. Possibilité sur J1 ou avec réduction supplémentaire, avec pont de puissance, boucle et référence de sortie à développer. La masse et l’encombrement le rendent moins adapté au poignet. [Pololu 4755](https://www.pololu.com/product/4755/specs).
- **Pas-à-pas à réduction.** Exemple 17HS15-1504S, 42 × 42 × 39 mm, 0,42 N·m de maintien, 1,5 A nominal par phase. Une réduction 3:1 est une piste pour la base et augmente le maintien aux dépens de vitesse. Prévoir encodeur de sortie, homing, contrôle de perte de pas et dissipation à l’arrêt. Le couple de maintien seul ne donne pas le couple en mouvement. [Fiche STEPPERONLINE](https://www.omc-stepperonline.com/nema-17-bipolar-42ncm-59-49oz-in-1-5a-42x42x39mm-4-wires-w-1m-cable-connector-17hs15-1504s).

## Électronique et protections

| Qté | Référence ou définition | Prix repère / source |
|---:|---|---|
| 1 | ROBOTIS OpenRB-150, boucle locale et USB | Prix et délai à reconfirmer chez le vendeur. [Constructeur](https://emanual.robotis.com/docs/en/parts/controller/openrb-150/) · [Vendeur](https://www.generationrobots.com/fr/266-capteurs-et-communication) |
| 1 en prêt ou achat futur | Banc B&K Precision 1688B, 1–18 V / 20 A, équivalent de banc possible | 420 € affichés par le fabricant en France. Vérifier TVA et possibilité d’emprunt. [B&K Precision](https://www.bkprecision.com/products/power-supplies/BK1688B-1-18v-0-20a-switching-dc-power-supply.html?region_code=fr) |
| 1 | Arrêt à deux contacts NC XB5AS8444 | 25,40 € TTC affichés. [Schneider](https://www.se.com/es/es/product/XB5AS8444/pulsador-seta-parada-emergenciagdp-2nc/) · [Vendeur](https://www.one-elec.com/materiel-electrique-industriel/boutons-et-voyants-industriels.html?nom_de_l_appareil=XB5&profondeur%5B0%5D=52%C2%A0mm&profondeur%5B1%5D=82%C2%A0mm) |
| 1 ensemble | Contacteur/relais puissance CC, retour auxiliaire, réarmement et coffret | À chiffrer après le courant coupé, le temps de décharge et la compatibilité avec le dispositif de retenue mécanique. |
| 1 lot | Bornier étoile, sept protections fusibles, sept porte-fusibles, détrompage, faisceau et connecteurs | Câbles X3P 180 mm, 27,14 € par lot de dix affichés. Prévoir la répartition de puissance et contrôler les longueurs au montage. [ROBOTIS X330](https://emanual.robotis.com/docs/en/dxl/x/xc330-t288/#connector-information) · [Tarifs accessoires](https://static.generation-robots.com/en/402710-dynamixel-xm430-w350-t-servo.html) |
| 1 à 2 | Référence G1 multi-tours, capteur de référence ou codeur de sortie lors des essais J5/J1 | À sourcer après choix de l’implantation, écart de détection et câblage. |

## Pièces sur plan et quincaillerie

| Qté | Désignation | Approvisionnement |
|---:|---|---|
| 1 + 4 | Plaque aluminium 6082 de 260 × 220 × 8 mm et quatre tubes Ø14 × 52 mm | Découpe et perçage en atelier, devis. |
| 4 + 4 | Fixations M6 du plateau et tirants M4 longs du socle avec écrous/rondelles | Standard métal à métrage final. Longueur M4 selon empilement, accès et dépassement. Contrôler le support d’ancrage. |
| 1 jeu | Quatre reprises J1–J4, coussinet J1, trois manchons et trois arbres avec double méplat J2–J4 | Acier/bronze ou aluminium selon le plan. Chiffrage atelier après jeu ajusté, appuis, usure et validation du plan de montage. |
| 6 | Supports moteur, dont berceau J1, supports J2/J3 et bride J5 en métal pour le service | Cassettes J4/G1 en PETG candidat, rigidité à éprouver. Les attaches au palonnier des trois grands servos restent à relever sur pièce. |
| 1 + 1 | Engrenage module 0,8, pignon 18 dents et couronne 42 dents | Acétal usiné ou métal selon mesure de bruit et d’effort. Relever jeu, fixation antirotation et tenue de la denture. |
| 1 + 2 + 2 | Vis Ø4 à avance 2 mm avec pas opposés, deux écrous sur plan, deux guides métal Ø3 | Demander un chiffrage atelier une fois le filet, la longueur active, la retenue axiale et les couples d’essai spécifiés. |
| 1 lot | Vis M2/M3, inserts d’essai, rondelles et goupilles | Arrêter longueurs après mesure réelle. [CNC Kitchen, plan des inserts](https://cnckitchen.com/s/CNCKitchen_Heat-Set-Insert-Dimensions-and-Design-Guidelines.pdf). |
| Selon CSV | Pièces PETG et garnitures TPU | [[03_Impression_3D/PROTOCOLes_FDM#AURA-004 — Fabrication préparée|Détail des orientations, quantités et consommation]]. Imprimante, matériau et lot à confirmer. |

## Palonniers J1–J3 à vérifier au montage

Les kits constructeur identifient le palonnier de chaque moteur. Les vis ci-dessous sont des références des kits citées pour le montage du palonnier sur un support, avec une longueur à recalculer pour l’adaptateur AURA-01.

| Axe et actionneur | Palonnier fourni avec le moteur selon ROBOTIS | Vis pour liaison palonnier-support relevées sur les fiches |
|---|---|---|
| J1 · XL430-W250-T | HN11-N101, livré monté | M2 × 5 dans le kit moteur. [Kit XL430](https://en.robotis.com/shop_en/item.php?it_id=902-0135-000) |
| J2 · XM540-W270-T | HN13-N101 | M2,5 × 4 dans le kit moteur. [Kit XM540](https://en.robotis.com/shop_en/item.php?it_id=902-0137-000) |
| J3 · XM430-W350-T | HN12-N101 | M2 × 3 dans le jeu de palonnier référencé séparément. Vérifier la visserie du kit moteur livré. [Kit XM430](https://en.robotis.com/shop_en/item.php?it_id=902-0124-000), [jeu HN12-N101](https://en.robotis.com/shop_en/item.php?it_id=903-0238-000) |

Avant de figer les adaptateurs, relever le diamètre de centrage, la répartition des perçages, l’offset axial de la face d’appui et la profondeur utile de chaque taraudage. L’engagement d’une vis vaut sa longueur depuis la tête d’appui moins l’épaisseur de l’empilement traversé. Vérifier l’engagement suffisant et la garde en fond de trou, puis l’accès à l’outil avec le connecteur TTL et le faisceau en place. Le verdict d’intégration se prend sur le plan et au montage à blanc. [[02_Conception_Fusion/CONCEPTION_MECANIQUE#Implantation et transmissions|Interfaces en CAO]].
