# AURA-006 — Intégration mécatronique V3

Révision de travail du 22 novembre 2026. La r03 reste la référence FDM protégée. Le dossier [Intégration mécatronique](../../../archives/v3/integration-aura-006/) contient la branche indépendante, les deux bancs, les STEP ROBOTIS originaux, les preuves et les exports. Voir la [[03_Impression_3D/NOTICE_BANCS_V3|notice, nomenclature et essais au banc]], les [[05_Electronique/SCHEMA_FUTUR|rails et faisceaux]], la [[08_Tests/MATRICE_TESTS|matrice de validation]] et le [[05_Electronique/README_MOTEURS_V3|README moteurs]].

## A — Audit de la r03

Fusion 2706.1.17 a rouvert la r03 avec 23 occurrences, 22 pivots et 18 enveloppes de moteurs. L’empreinte de la r03 est vérifiée dans [Verification_Fusion.json](../../../archives/v3/integration-aura-006/Verification_Fusion.json). Les logements r03 sont utiles pour localiser les actionneurs. Les transmissions, les retenues axiales, les vis, les câbles et l’arrêt hors tension restaient à démontrer. Les 23 pièces imprimées sont toujours la référence de silhouette. Les 165 poses d’origine n’incluaient aucun faisceau ni quincaillerie représentative sur l’ensemble du bras.

Trois STEP constructeur ont été récupérés et vérifiés au format ISO 10303-21 avec leurs empreintes. Le XM540 n'est plus un simple parallélépipède sur le banc J2. Les dessins HN13-N101 indiquent un cercle de huit M2,5 au diamètre 22 mm, une fixation centrale M3 × 8 et une profondeur taraudée de 2,5 mm au palonnier. Les taraudages auxiliaires du carter ont une profondeur maximale de 4 mm. Le X06 est reconstruit à partir du plan coté, faute de STEP public identifié. [XM540](https://emanual.robotis.com/docs/en/dxl/x/xm540-w270/#drawings) · [XM430](https://emanual.robotis.com/docs/en/dxl/x/xm430-w350/#drawings) · [XC330](https://emanual.robotis.com/docs/en/dxl/x/xc330-t288/#drawings) · [fiche KST V6, PDF](https://www.kst-servo-shop.de/media/4b/63/fe/1749810623/KST_0053_X06_V6_Datenblatt_04_2025_de.pdf?ts=1751463826)

## B — Doigt indépendant

Trois corps KST fixés sur les phalanges entraînent au travers du palonnier attaché à la pièce amont. Entraîner le rotor fait tourner la phalange qui porte le corps. En face, un axe acier Ø3 et une bague Ø3 × Ø4,5 × 3 prennent l’appui. Une goupille Ø2 à 9 mm de l’axe court dans une lumière en arc. Les vis de pattes, les vis centrale et excentrée, la retenue de l’axe et les sorties de fils sont des pièces ou volumes distincts dans Fusion.

Le témoin à 17 mm a parcouru **2,372 mm** sur chacun des trois axes à la commande de 8°. Sur 24 poses, les **18 échantillons de 0 à 45°** et les trois essais à 47° sont dégagés. Le pion de chaque butée a rencontré sa chape à l’essai isolé hors course à 53°. Il reste à mesurer le palonnier, le filetage et les longueurs de vis réels, à qualifier l’ajustement des axes et à tester la boucle souple des câbles. Pour une charge transversale au bout, 0,039 N·m nominal donne environ 0,31 N à 125 mm de la racine en première approximation. Une mesure avec cellule de charge tranchera la capacité réelle.

Les quatre pièces D00–D03 sont exportées en STEP et 3MF et ont été tranchées. Le coupon peut être imprimé avant la vérification des achats. Le doigt complet attend un ajustement du palonnier et les essais. [Tomas Liu TLS0082, 15T Ø4](https://tomas-liu-studio.com/products/cha-servo-06-horn) · [igus iglide G300](https://www.igus.com/ContentData/Products/Downloads/iglide_G300_FM_USen.pdf)

L’archive du doigt a été rouverte dans Fusion avec 37 composants, trois pivots moteurs et l’historique. La dépose de chaque KST, quincaillerie et palonnier déposés, est dégagée face à sa phalange aux 17 positions de translation verticale, de 0 à 16 mm. Ce contrôle ne comprend pas la trajectoire du connecteur et des fils réels.

## C — Épaule J2 indépendante

XM540-W270-T → HN13-N101 → arbre d’entrée Ø12 sur deux roulements → courroie synchrone 5M 425 × 15 et poulies métalliques 16/64 → arbre sortant Ø12 × 200 sur deux roulements → moyeu à clavette → levier. Les roulements d’entrée évitent de reprendre la tension de courroie sur la sortie du servomoteur. Une platine à trous oblongs permet le réglage initial de l’entraxe. La courroie et les poulies sont représentées par leurs enveloppes de pas. La largeur, les dents, le profil et la capacité de la poulie de 16 dents restent à confirmer avec le fournisseur choisi.

| Quantité calculée | Valeur au modèle |
| --- | --- |
| Masse suspendue estimée, charge incluse | 1,790 kg |
| Charge, bras de levier | 100 g à 0,70 m |
| Moment gravitaire maximal | 5,678 N·m |
| Inertie autour de J2, masses en points | 0,269 kg·m² |
| Dimensionnement | (5,678 + 0,6 × 0,269 + 0,25) × 1,35 = 8,221 N·m |
| Minimum continu équivalent au servo, rendement supposé 85 % | 1,67 N·m en statique |
| Objectif de pointe au servo à ce rendement | 2,418 N·m |
| Vitesse à vide estimée sortie, entrée à 11,1 V | 7 tr/min |
| Effort tangentiel calculé sur la poulie de 64 dents au dimensionnement | 161 N, hors précharge |

Les masses FDM proviennent de la r03 tranchée, les moteurs des fiches et les accessoires d’estimations. Le fichier de vérification conserve chaque masse et distance. ROBOTIS indique 10 N·m au blocage à 11,1 V et 28 tr/min à vide. La valeur continue reste à mesurer, ainsi que la tension de courroie, les contraintes de fatigue, le cisaillement des clavettes et la déformation des montants. Le frein à ressort candidat se fixe après la transmission, directement sur l’arbre porté. Son couple statique annoncé de 16 N·m donne 1,95 fois le couple de dimensionnement. La bride, le véritable moyeu du frein et leurs fixations doivent être confirmés au plan constructeur. L'énergie d’un arrêt, le temps de prise et la chute à coupure sont à mesurer avec le banc ancré. L’axe J2 du bras reste à adapter à ce banc. [ROBOTIS XM540](https://en.robotis.com/shop_en/item.php?it_id=902-0137-000) · [Gates](https://cms.gates.com/~/media/NAPA/Documents/NAPA_IndustrialBeltCatalog.ashx) · [SKF 6001-2RSH](https://www.skf.com/at/products/rolling-bearings/ball-bearings/deep-groove-ball-bearings/productid-6001-2RSH?failover=true) · [Kendrion KS 10110A00-0001](https://www.kendrion.com/en/productfinder/group/product/brakes/ks-10110a00-0001)

La révision 4 du banc atteint 0 à 60° tous les 5° en pilotant le moteur dans Fusion. La commande 16° donne 4° à la sortie. Fusion ne remonte aucune interférence sur les 13 positions de service ni lors des trois retours testés. Les configurations sacrifiées à −7° et +69° détectent le pion contre la butée métallique. Seuil volumique du script 0,002 mm³. Le rapport JSON conserve les coordonnées du témoin et les contacts hors course.

L’entraxe de pas est **105,507 mm** et l’enroulement sur la poulie de 16 dents **137,55°**, soit environ 6,1 dents en prise au modèle. L’archive a été rouverte avec 71 composants et les deux pivots natifs. Le carter hors vis se dépose par translation extérieure aux 22 positions vérifiées. Le moteur hors palonnier se retire vers l’arrière aux 28 positions contrôlées face à la structure fixe choisie.

Le catalogue Gates limite l’alésage de sa P16-5M-15 standard à 0,313″, soit **7,95 mm**. La pièce du banc CAO est prévue à **12 mm**. Il faut un devis de poulie sur mesure avec section utile validée ou une modification de l’arbre d’entrée et de sa cartouche. Côté 64 dents, une poulie à douille 1210 et bague Ø12 existe. Son moyeu dépasse le volume axial de 20 mm du modèle courant et demande une mise à jour de la CAO. [Gates, catalogue HTD](https://www.gates.com/content/dam/gates/home/knowledge-center/resource-library/catalogs/light-power-and-precision-manual.pdf) · [Stima, TL 64 5M 15](https://www.stima-engineering.com/en/Timing_belt_pulleys_HTD_for_taper_bushes-c219) · [Mädler 62250312, 1210 Ø12](https://www.maedler.de/Article/62250312).

Le socle de banc est ancré par quatre M6. À titre d’ordre de grandeur, un couple de 8,22 N·m repris sur 152 mm d’entraxe représente 54 N de traction totale sur le côté opposé avant précharge, chocs et dissymétries. Pour la V3 en porte-à-faux avant, le moment de 5,68 N·m décalé au bord avant du socle à 93 mm donne environ 4,05 N·m déstabilisants. Le pack de 5,4 kg peut ajouter environ 15,9 N·m de rappel longitudinal seulement si le berceau et le robot partagent un bâti rigide. La tenue latérale, la déformation et l’arrachement des inserts restent à vérifier.

## D — Interfaces des autres axes

| Axe | Emplacement visé | Travail mécanique à qualifier |
| --- | --- | --- |
| J1 | XM430 vertical dans le socle, secteur sous la tourelle | Logement creux, roulement de couronne séparé du servo, retenue, butée d’azimut et boucle anti-torsion |
| J2 | Banc 4:1, frein après courroie | Reprise de la tourelle autour de l’arbre porteur et recalcul de J1 avec le frein de 1,9 kg |
| J3 | XM540, sortie latérale du segment intermédiaire | support, accès et chaîne porteuse à redessiner à partir du STEP. Recalculer un rapport de réduction et la retenue hors tension |
| J4 | XM430, sortie latérale du segment distal | Bride, montage d’un palier opposé et gestion de la gravité en coupure |
| J5 | XC330 sous l’axe de déviation | Plateau et palier séparés, reprise des chocs de main |
| J6 | XM430 dans le berceau de flexion | Levier ou déport à étudier, appui opposé et passage des cosses hors chape |
| J7 | XC330 axé dans le talon de la paume | Couronne et couple de roulis, retenue axiale, fenêtre pour la boucle de câble |
| Main | 15 KST, trois par doigt | Éprouver le doigt de référence puis contrôler capteurs, variation des géométries, inserts et faisceaux des cinq doigts |

Le même bilan de masse, avec charge utile de 100 g et bras horizontal, donne les estimations suivantes. Les distances sont projetées sur l’axe du bras. J5 ne subit ce maximum gravitaire que dans les orientations qui inclinent son axe.

| Axe | Gravité, estimation haute | Cible avec inertie, frottement et facteur 1,35 | Conséquence |
| --- | ---: | ---: | --- |
| J3 | 3,55 N·m | 5,18 N·m | Réduction et dispositif hors tension à étudier avec le XM540 |
| J4 | 2,21 N·m | 3,24 N·m | Marge étroite face à 3,8 N·m de blocage. Prévoir une réduction ou un équilibrage |
| J5 | 1,24 N·m | 1,83 N·m | La prise directe XC330 ne convient pas à la pose défavorable. Étudier une réduction 4:1 et un arbre porté ou un transfert de la masse du poignet |
| J6 | 0,96 N·m | 1,43 N·m | Confirmer le couple continu et un appui opposé au moteur |
| J7 | environ 0,20 N·m en roulis | À recalculer | Hypothèses de déports latéraux de 30 mm pour la main et 80 mm pour la charge |
| J1 | Nul par gravité si son axe est vertical | À recalculer | Inertie d’azimut, frottement, frein et efforts du faisceau à mesurer |

La branche Fusion a été rouverte avec **321 liaisons**, dont les 15 pivots moteurs des doigts et les sept pivots de bras r03. Chacun des 15 moteurs déplace son témoin de 2,32 mm pour une commande de 7°. Aucune interférence volumique de la main n’a été détectée dans les cinq fermetures simultanées de 0 à 45° et les trois poses asymétriques testées. Les 67 contacts externes entre implantations moteur constructeur et structure à HOME sont consignés dans la preuve. Les solides complexes issus de fonctions de base se régénèrent par les sources Python. Une cote de pièce n’est pas toujours une cote de croquis modifiable dans l’interface.

## E — Architecture embarquée

Le module d’alimentation est extérieur, fixé au même bâti que le socle. Batterie candidate RELiON RB24V20 25,6 V, 20 Ah, 512 Wh, 195 × 131 × 171 mm, 5,4 kg, BMS intégré 30 A continus, 60 A en pointe brève et charge 28,4 à 29,2 V. Le montage comporte berceau, sangles, bornes protégées, platine de logique séparée et accès charge. Vérifier l’emplacement des bornes réelles, la visserie M8, la ligne de fusibles et les cotes des convertisseurs. Une alimentation séparée convient au calculateur, avec réserve de 25 W et refroidissement à dimensionner. [RELiON](https://www.relionbattery.com/products/lithium/rb24v20) · [Raspberry Pi 5](https://www.raspberrypi.com/documentation/computers/sbcs.html)

| Rail | Courant à qualifier et implantation |
| --- | --- |
| DYNAMIXEL 11,1 V | 16,3 A somme des blocages, objectif rail 20 A. Candidat TDK‑Lambda i7A4W033A033V‑0C1‑R, entrée 18–60 V, 33 A selon conditions. Module à monter sur carte de puissance et dissipateur, réglage 11,1 V. Vérifier les creux (XM min. 10 V) et les surtensions lors du freinage (XC max. 12 V) aux bornes |
| KST 6 V | 8,7 A somme des blocages. Deux groupes 8 et 7 moteurs (4,64 A et 4,06 A). Candidat deux D36V50F6 fixés sur platine hors main. Vérifier puissance thermique, câblage de l’aller/retour et creux aux KST. Les sorties des régulateurs restent distinctes |
| Frein 24 V | 20,8 W, ~0,87 A. Candidat Mean Well DDR‑60G‑24, entrée 9–36 V. Contrôle matériel de l’énergie, protection de bobine retenue après choix du temps de prise |
| Logique 5 V | Pi 5 via alimentation USB-C compatible, jusqu’à 5 A. Branches logiques séparées par fonctions, arrêt du Pi contrôlé. OpenRB réservé au signal TTL et alimenté localement. La puissance des sept DYNAMIXEL est distribuée hors des ports de la carte (3 A max en commun) |

284,9 W de somme théorique aux sorties (233,1 W moteurs, 20,8 W frein, 25 W Pi, 6 W auxiliaires). Avec un rendement conservateur de 87 %, cela correspond à environ 328 W à la batterie, soit 14,9 A à 22 V. La conception du câblage doit traiter l’appel de courant à la mise sous tension, les coupures, la régénération et les pertes en régime réel. Une réserve de 20 % et 88 % de rendement donnent environ 360 Wh délivrables. Les scénarios de 70 W et 130 W donnent 5,1 h et 2,8 h calculées. La puissance moyenne et l’autonomie se mesurent sur un cycle. [TDK i7A](https://product.tdk.com/en/search/power/switching-power/dc-dc-converter/info?part_no=I7A4W033A033V-0C1-R) · [Mean Well DDR-60](https://www.meanwell.com/Upload/PDF/DDR-60/DDR-60-spec.pdf) · [Pololu D36V50F6](https://www.pololu.com/product/4092) · [ROBOTIS OpenRB-150](https://docs.robotis.com/docs/parts/controller/openrb-150/)

Le Pi 5 reçoit la caméra CSI fixe et un microphone I²S, propose des cibles de mouvement et tient le journal des défauts. L’OpenRB-150 est le candidat de commande du bras. Le microcontrôleur de la main reçoit des commandes différentielles RS-485, émet les 15 PWM via PCA9685 (carte 815, sorties de signal) et surveille tensions et température. Le retour 6 V par doigt se fait dans un répartiteur dédié et non par la carte PCA9685. Le futur capteur de force est un patin instrumenté en bout de doigt, calibré. Le ToF sur la paume sert à l’approche et son absence de détection doit être gérée. Pour HOME, les encodeurs DYNAMIXEL donnent le repère moteur, une mesure sur l’arbre J2 et des index sur les sorties servent au repérage de mécanismes à jeu, réduction ou débrayage. Les KST ne renvoient pas l’angle sur PWM. Un codeur magnétique ou une mesure externe sur banc complète l’essai. [Caméra Module 3](https://www.raspberrypi.com/documentation/accessories/camera.html) · [Adafruit PCA9685](https://www.adafruit.com/product/815)

Un bouton à maintien agit par une chaîne matérielle sur la puissance des moteurs et l’énergie qui relâche le frein. Le contrôleur local impose un délai de perte de commandes, des limites de course, vitesse, courant, tension et température. Le réarmement est manuel, après défaut et coupure. Les courants de démarrage, la chute des axes en coupure et la compatibilité des contacteurs et fusibles DC doivent être éprouvés. Le calculateur embarqué et l’application future suivent le schéma [[06_IA_Logiciel/ARCHITECTURE_IA|d’architecture IA]].

### Faisceau

| Circuit | Architecture et contraintes |
| --- | --- |
| Batterie → coffret | Aller/retour DC dimensionnés sur échauffement et chute de tension, cosse isolée M8, fusible DC au départ, sectionneur et transitoire de précharge si nécessaire |
| Distribution DYNAMIXEL | Distribution équilibrée, sous-groupes de puissance. Connectique TTL constructeur pour chaque référence, retours de masse maîtrisés et bus partagé de signal. Vérifier le courant admissible de chaque broche, connecteur et dérivation |
| Socle → main | Paires puissance indépendantes vers les deux groupes 6 V, boucle de service à chaque axe mobile, paire torsadée RS-485 et référence. Séparer les fils énergie et signaux. Retenir par colliers gainés hors des charnières |
| Main → cinq doigts | Trois sorties PWM par doigt, passage sous chaque phalange, connecteur de service détrompé par branche, ancrages opposés à chaque pivot et protection de bord. Travailler avec le rayon minimal du câble effectivement acheté |

Sur six positions, les tronçons, connecteurs, cartes et batterie n’interfèrent pas avec les solides inclus dans cette passe de CAO. Les boucles mobiles ont fait l’objet d’un contrôle distinct. Les 42 combinaisons de boucle et de pose ont été calculées à partir des ancrages mobiles. Les rayons calculés vont de 1,06 à 20,26 mm, sous les cibles provisoires de 32 à 43 mm. L’enveloppe de la boucle socle–J1 touche le socle et la tourelle dans les six positions. Éloigner les ancrages permet d’augmenter les rayons. Le passage dans le socle et les dégagements du poignet restent à intégrer aux transmissions réelles. Les enveloppes de boucles à HOME sont enregistrées, masquées par défaut. Confirmer le rayon du câble acheté, les boucles par phalange, la torsion et la longueur d’extraction de chaque connecteur.

## F — Fabrication et état de qualification

La commande d’atelier commence par le [[03_Impression_3D/NOTICE_BANCS_V3|coupon, les deux bancs, les nomenclatures et les protocoles]]. Les axes, vis et transmissions structurantes sont métalliques. La tenue des montants FDM, des inserts et du profil de la poulie fait partie des essais. La paume, les trois familles de phalange et les supports électriques ont des géométries d’essai. Les sept solides historiques du socle, de la tourelle, des trois segments et du poignet restent des références de volume pendant le travail des transmissions. Leur kit 3MF r03 reste dans son dossier historique.

| Sous-ensemble | Conçu | Preuve numérique | Impression d’essai | Essai physique ou point bloquant |
| --- | --- | --- | --- | --- |
| Doigt indépendant | Composants, guidages, fixation et butées | Mouvement, interférences et dépose des moteurs échantillonnés | D00–D03 et coupon, pour montage à blanc | Aucun. Cotes du palonnier et des vis, jeu, effort et chaleur à mesurer |
| Banc J2 | Transmission, roulements, frein et arrêt axial représentés | Réduction, poses, butées, sortie carter et moteur contrôlées | J20–J23 pour montage à blanc | Aucun. Profil de courroie, fixations de frein, tenue continue et coupure en charge |
| Main complète | Quinze entraînements et paume révisée | Huit poses de la main, sorties de moteur reconstruites | Paume et phalanges disponibles comme éprouvettes de géométrie | Aucun. Faisceau, assemblage réel et contact dynamique exhaustif restent à valider |
| J1, J2 du bras et J3–J7 | Implantations et architecture des interfaces | STEP et conflits à HOME pour six axes | En attente | Aucun. Dimensions, transmissions, paliers et arrêt des axes porteurs |
| Batterie, électronique et faisceau | Berceau, platines, volumes, bilan de puissance | Six poses et étude des boucles | Coupon et supports d’encombrement pour ajustement uniquement | Aucun. Boucles, alimentation, arrêt et autonomie |

Les 14 géométries d’essai ont chacune un STEP et un 3MF. PrusaSlicer a produit un G-code en fichier temporaire pour chacune avec le profil PETG r03 et recentrage sur un plateau de 220 × 220 mm. Les maillages en millimètres n’ont ni arêtes de bord ni arêtes partagées par plus de deux faces au contrôle. Les six plateaux historiques ont également été retranchés avec leurs 23 pièces r03. Le rapport [Tranchage_Prusa.json](../../../archives/v3/integration-aura-006/Tranchage_Prusa.json) consigne dimensions, empreintes, matériau estimé et durée.

Les notes mises à jour sont le README, le tableau de bord, le dossier de design V3, le README moteurs, le schéma électrique, l’architecture IA, la matrice, le contexte court, les décisions, le journal et les tâches. Le présent rapport et la notice d’atelier sont nouveaux.
