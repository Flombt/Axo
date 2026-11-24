# Notice des bancs mécatroniques V3

Candidats d’essai AURA‑006 du 22 novembre 2026. Voir [[02_Conception_Fusion/INTEGRATION_MECATRONIQUE_V3|rapport d’intégration]], [[05_Electronique/README_MOTEURS_V3|références moteur]] et [[08_Tests/MATRICE_TESTS|suivi des essais]]. Les dossiers [du doigt](../../../archives/v3/integration-aura-006/01_Doigt/) et [de l’épaule](../../../archives/v3/integration-aura-006/02_Epaule/) contiennent les assemblages Fusion, les pièces à imprimer et leurs visuels. Les fichiers [de vérification](../../../archives/v3/integration-aura-006/) donnent les empreintes, poses et données de tranchage. Recentrer chaque 3MF sur le plateau lors de l’import dans PrusaSlicer.

## Doigt D00–D03

| Quantité | Référence ou fonction | Interface à mesurer |
| ---: | --- | --- |
| 1 + 3 | D00 montage ancré, D01–D03 phalanges blanches, PETG technique pour premiers essais | État du pont autour du chariot, planéité et dimensions du voile autour du logement |
| 3 | KST X06 V6.0, le même modèle que le README | Boîtier 20 × 7 × 16,6 mm, sortie 15T Ø4, pattes à 24 mm d’entraxe. Mesurer longueur et position du câble |
| 3 | Tomas Liu TLS0082, 7075, diamètre 4 mm, 15 dents, positions 4,1 / 6,05 / 8 mm | Hauteur de tête, épaisseur, diamètre au point 8 mm et vis centrale livrée |
| 3 | igus GSM-0304-03, Ø3 × Ø4,5 × 3 mm | Alésage imprimé cible 4,52 mm avant calibration. Confirmer tenue sertie et mouvement après montage |
| 3 | Axe acier rectifié Ø3 × 7,4 mm | Longueur à régler pour supprimer le battement sans précharger |
| 3 | Bague d’arrêt Ø3 et rondelle mince | Garder la vis d’arrêt accessible après montage |
| 3 | Pion de butée acier Ø2, longueur ~6 mm | Confirmer maintien dans phalange et libre passage dans la lumière |
| 6 | Vis de pattes M2 × 4 candidate | Vérifier l’insertion et la tenue du filet imprimé, utiliser inserts coupons si le maintien mesuré l’exige |
| 3 + 3 | Vis centrale KST d’origine et vis de liaison au rayon 8 mm (M1,6 candidate) | Confirmer type et longueur au palonnier mesuré. Couper toute saillie dans la course |
| 2 | Vis traversantes M4 avec rondelles et écrou pour le banc D00 | Reprendre sur support rigide indépendant |
| 3 | Prolongateur PWM 3 conducteurs avec connecteur apparié KST | Confirmer brochage, diamètre sous gaine et rayon de boucle |
| 1 | Alimentation de banc stabilisée 6 V à limitation de courant, contrôleur PWM, capteur externe de course | Rail d’essai mesuré sous charge, arrêt matériel accessible |

1. Imprimer le coupon E04, mesurer ses alésages et identifier les compensations en X/Y. Imprimer D00 sur sa base, les trois phalanges côté dos plat. Contrôler l’accès à chaque vis, enlever uniquement les supports et reprendre les alésages à la cote choisie.
2. Insérer la bague et le pion, puis poser chaque servo par l’ouverture inférieure. Brancher un seul KST à la fois et relever son neutre sans charge avant de caler le palonnier.
3. Avec le moteur non commandé, assembler de la racine au bout. Engager l’axe passif, régler sa retenue et caler le palonnier en position ouverte. Vérifier la liberté avant le serrage. Le câble sort par le dessous et se fixe hors de l’ouverture des deux joues.
4. Sur banc ancré, limiter d’abord chaque axe à 0–10°. Monter par paliers à 45° après contrôle visuel du fil, de la vis du palonnier et des paliers.

### Mesures du doigt

Faire 10 allers-retours pour chaque axe seul à 0/15/30/45°, puis 100 cycles pour le doigt entier. Angle par mesure indépendante, jeu à l’inversion ramené en degrés, écart au même angle par sens, force au dynamomètre à distance mesurée, courant de pointe, courant RMS et température des carters toutes les minutes. Repères provisoires **jeu ≤ 2°**, **répétabilité ≤ 1°** sans charge et retour ouvert sans pincement. À 6 V, comparer à 0,22 A et 0,039 N·m annoncés en nominal pour le KST. Le maximum de 0,58 A concerne le blocage. Approcher la limite sans imposer un blocage prolongé. Fixer la frontière thermique après lecture de la notice motoriste et du matériau retenu. Photographier le montage et archiver le CSV de mesures avant duplication.

## Épaule J2

| Quantité | Référence ou fonction | Interface |
| ---: | --- | --- |
| 4 | J20 socle, J21 levier de charge, J22 cartouche, J23 carter | J20–J22 en matériau structurel FDM qualifié, J23 PETG ou ASA selon atelier. Voir orientation des exports et recontrôler Ø28 après refroidissement |
| 1 | ROBOTIS XM540-W270-T SKU 902-0137-000, palonnier livré HN13-N101 | Face à PCD 22 mm et vis centrale M3 × 8 d’origine. Stator sur équerre métallique et deux vis M2,5 |
| 1 + 1 | Arbres acier Ø12, sortie longueur 200 mm, entrée solidaire de la bride | Ajustement acier/roulements selon fournisseur et service. L’entrée prend l’effort de courroie |
| 4 | SKF 6001‑2RSH, Ø12 × Ø28 × 8 mm | Deux roulements par axe, portée propre et coaxialité au mandrin |
| 2 + 2 | Couvercles externes de J2 et circlips internes de cartouche | Gorges et matière de maintien à qualifier. Si arrachement ou jeu, réaliser les supports d'arrêt en métal |
| 8 | Bagues d’arrêt Ø12 ou circlip extérieur suivant l’emplacement | Arrêt axial de l’axe et appui sur bague intérieure. La gorge et la bague courte côté poulie restent à qualifier |
| 4 | Clavettes acier 4 × 4, longueurs adaptées aux portées | Longueurs CAO par arbre, profil de rainure et section à vérifier avec l’usineur |
| 2 + 1 | Poulies 16/64 dents métalliques, largeur utile 15 mm, courroie Gates 425‑5M‑15 (9293‑0534), 85 dents | Le modèle cible deux alésages Ø12 avec clavette. La P16-5M-15 standard est limitée à 7,95 mm. Pour la 64 dents, vérifier la variante 1210 et l’encombrement axial. Faire arrêter les deux plans avant montage |
| 1 | Kendrion KS 10110A00-0001 24 V, 16 N·m statique, bride acier + moyeu Ø12 | Frein sur arbre entraîné, après la courroie. Plan de montage et entrefer constructeur indispensables |
| 1 + 1 | Plaque de butées acier et pion acier Ø8 | Arc en position 0–60°, contacts possibles hors course. Qualifier la tenue au choc |
| 4 + 2 + 2 | M5 fixation cartouche, M4 équerre servo et M4 carter | Mesurer les longueurs utiles, ajouter écrous ou douilles de retenue métallique appropriés |
| 2 + 4 | M2,5 équerre moteur, M2,5 à profondeur réellement engagée sur le palonnier | Confirmer têtes, rondelles et longueur. Le dessin ROBOTIS limite la prise à 4 mm carter et 2,5 mm palonnier |
| 2 + 4 + 2 | M5 butée, M5 montage frein (plan à confirmer), M5 réaction frein et leurs douilles | Montage à blanc avant d’alimenter le frein, vis de réaction et butée opposées et indépendantes |
| 2 + 4 | M6 levier au moyeu, M6 ancrage du socle avec rondelles + écrous | Reprendre l’effort dans un bâti rigide, avec retenue des masses d’essai |
| 1 | Jauge de force ou masses, thermocouples, capteur d’angle de sortie, voltmètre et pince courant DC | Journal daté et mesures synchronisées |

1. Contrôler le coupon et la pièce J20, dresser la base puis ancrer sur cadre rigide. Vérifier l’alignement des roulements au mandrin avant de monter les entraînements. Poser la plaque de butées et la bride métallique, en vérifiant que chacune des deux vis opposées garde une longueur libre.
2. Poser moyeu, anneaux, roulements et clavettes dans leur ordre de montage, en présentant les arbres à la main. Confirmer les jeux aux deux positions limites. Monter le servo et sa cartouche amovible, vérifier l’alignement des arbres et la profondeur effective des vis. Monter et tendre la courroie avec la méthode Gates correspondant à la transmission retenue, puis poser le carter.
3. Monter le frein sur l’arbre de sortie. Mesurer le couple de retenue à la main sur montage protégé avant toute levée. Raccorder les rails servo et frein séparés. Garder un palan ou une butée de rattrapage sous le levier pendant les essais.

### Mesures J2

- Sans charge, relever jeu à l’inversion, courant, vitesse, position et indication des butées. Réintroduire la charge par moments connus (par exemple 2, 4, 5,68 N·m). Le bras d’essai à 169 mm demande environ 3,43 kg pour 5,68 N·m si le poids propre du levier est nul. Mesurer le moment propre puis retarer. Pour le cas dynamique, un moment de 8,22 N·m correspond à environ 4,96 kg à 169 mm dans la même hypothèse. Employer une fixation de poids traversante qualifiée ou un effort contrôlé. Le levier imprimé est à qualifier avant une telle charge.
- Mesurer la tenue continue à chaud à la charge statique cible pendant 30 minutes ou jusqu’à stabilisation mesurée de la température. Enregistrer température du moteur et support, angle, déformation de la structure, courant RMS et pointe. Si la marge thermique est insuffisante, étudier équilibrage ou autre motorisation avant adaptation au bras.
- Avec une retenue indépendante, mesurer la perte angulaire entre coupure et prise du frein à 0/25/60° et aux trois niveaux de charge retenus. Répéter coupure de batterie, arrêt d’urgence, panne signal et tension insuffisante. Inspecter butées, câble, paliers et maintien des masses après essai.
- Pour l’électrique, travailler avec des charges simulées avant les moteurs. Capturer à l’oscilloscope le min/max des rails (notamment XC ≤12 V), la tension au KST le plus éloigné, le comportement à l’arrêt et le délai de coupure. Valider ensuite les pertes de communication, le redémarrage sans mouvement et le cycle d’autonomie.

## Fabrication et prix

Le profil de tranchage de contrôle est le profil PETG r03, buse 0,4 mm, couches de 0,20 mm, supports sur plateau. Le coupon propose trois cotes de logement Ø28 et des alésages allant de la calibration de vis au montage de la bague du doigt. Les essais matière orientés (traction, flexion, arrachement et fluage) sont requis sur J2. Les axes, pions, vis de réaction, moyeux, couronne, rondelles, supports de frein et poulies critiques sont métalliques. En production, des matériaux renforcés peuvent servir pour les corps porteurs si leur impression et leur tenue sont confirmées sur l’imprimante de l’atelier.

Prix indicatifs en USD affichés chez les fabricants, hors quantité, taxes et livraison. Le XM540 est à 419,90 USD, le XM430 à 269,90 USD, le XC330 à 89,90 USD et le KST à 39,99 USD. Les 22 moteurs représentent **2 429,15 USD** à ces prix. Les trois KST de banc totalisent 119,97 USD. Deux kits de deux palonniers TLS0082 suffisent pour ce banc (34 USD). Le frein industriel, la batterie, les arbres et la tôlerie restent à chiffrer. [XM540](https://en.robotis.com/shop_en/item.php?it_id=902-0137-000) · [XM430](https://en.robotis.com/shop_en/item.php?it_id=902-0124-000) · [XC330](https://en.robotis.com/shop_en/item.php?it_id=902-0171-000) · [KST](https://kstservos.com/products/x06-v6-0-hv-micro-digital-metal-gear-glider-1-8kg-torque-servo-motor) · [TLS0082](https://tomas-liu-studio.com/products/cha-servo-06-horn)

Chiffrer les bancs après choix des tolérances. Pour le robot, ajouter les douze KST restants, les moteurs J1 et J3–J7, la batterie, les mécanismes de retenue nécessaires après étude, les convertisseurs, câbles et capteurs. Évaluer le coût FDM d’après le poids de chaque pièce et le tarif local du filament.

### Électronique embarquée à chiffrer

| Quantité | Pièce | Coût unitaire connu ou statut |
| ---: | --- | --- |
| 1 + 1 | RELiON RB24V20 et chargeur compatible LiFePO₄ 28,4–29,2 V | À chiffrer, confirmer le coût total livré et le couple de serrage des cosses |
| 1 + 1 | TDK i7A4W033A033V‑0C1‑R, carte et dissipateur | Devis et qualification des transitoires |
| 2 | Pololu 4092 D36V50F6 | 39,95 USD affichés |
| 1 | Mean Well DDR‑60G‑24 | À chiffrer |
| 1 + 1 + 1 | Pi 5, alimentation USB-C appropriée et refroidisseur | RAM selon essais de vision et de voix. Capacité et prix à arrêter ensemble |
| 1 + 1 | OpenRB‑150, contrôleur de main avec transceiver RS‑485 | Logique et signal. Ne pas alimenter les sept DYNAMIXEL par l’OpenRB |
| 1 | Adafruit PCA9685 815 | Commande 15 PWM, variante et tarif à confirmer |
| 1 + 1 + 1 | Camera Module 3, microphone I²S, ToF court | Fixation et connecteurs caméra à confirmer. Microphone et ToF à sélectionner |
| 1 lot | Courant, température, index d’arbre J2 et d’origine, rails, arrêt à enclenchement | Liste détaillée après essais de courant, d’interface et d’encombrement |

[RELiON](https://www.relionbattery.com/products/lithium/rb24v20) · [TDK i7A](https://product.tdk.com/en/search/power/switching-power/dc-dc-converter/info?part_no=I7A4W033A033V-0C1-R) · [Pololu 4092](https://www.pololu.com/product/4092) · [Mean Well](https://www.meanwell.com/Upload/PDF/DDR-60/DDR-60-spec.pdf) · [Adafruit](https://www.adafruit.com/product/815).
