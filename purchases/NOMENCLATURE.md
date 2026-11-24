# Nomenclature · V5-roulis-v1

**Plafond de 150 €** pour le matériel de mise au point. Le panier économique vise **149,48 € TTC livré** en France métropolitaine aux conditions de port et de retrait du [panier V5](../archives/v5-revue/ACHATS.md). Les prix affichés ci-dessous ont été relevés le 24 novembre 2026. [Modèle avec les deux roulis](../fusion/AURA-01.f3d)

## Pièces ajoutées

Le [budget détaillé](../DIAGNOSTIC_ROBOT_COMPLET.md#11-budget-ttc-pièces-et-couverture) donne **149,48 €** hors filament et corrections et **161,43 €** avec une bobine à 11,95 €. Le prix du lot opérationnel reste à confirmer.

| Fonction | Référence et quantité de travail | Vérification |
|---|---|---|
| Lacet et poignet | 2 × Tower Pro SG90 RBS15198 | Palonniers, course et tenue. |
| Tangages J2/J3 | 2 × MG996R numérique 180° Atelier de la Robotique | Cannelure et pattes, courant et couple continu du lot. |
| Deux roulis longitudinaux | 2 × MakerMind MG90S RBS11204 | Gabarits, course au tambour et effort après gainage. |
| Cinq doigts | 5 × MakerMind SG90 RBS10195 | Bobine, rappel, débattement et maintien. |
| Commande | 1 Pico 2 RP2350, 1 USB données | 11 voies et seuils de signal à valider. |
| Puissance | 1 bloc AM5120 envisagé | Rail, protections et coupure à qualifier. [Architecture](../electronics/README.md) |
| Appuis | 2 roulements 608 (8 × 22 × 7 mm), lot de 10 ZZ chiffré | 2RS en CAO. Présenter les bagues et vérifier le jeu. |
| Quincaillerie | M8×55, deux axes M5, quatre ancrages M5, tige Ø2, M2/M3/M4 | Longueurs, portions lisses, têtes, rondelles, écrous de stock. Les M5×70 du panier dépassent l’enveloppe du gabarit. |
| Transmission et fils | 11 jeux JR estimés, PTFE Ø4/2, nylon Ø0,40, rappels et cuivre | Vérifier le rayon, la longueur et les arrêts après reprise des parcours. |


| Pièce | Quantité | Prix unitaire | Total | Lien |
|---|---:|---:|---:|---|
| MG90S de position à engrenages métalliques, RBS11204 | 2 | 3,95 € | 7,90 € | [MakerMind MG90S](https://www.makermind.fr/p/servomoteur-micro-mg90s) |
| Tube PTFE Ø4 mm extérieur / Ø2 mm intérieur | 2 m, à débiter en quatre gaines | 2,20 €/m | 4,40 € | [MakerMind PTFE au mètre](https://www.makermind.fr/p/tuyau-ptfe-1-metre-2-mm-x-4-mm-pour-extrudeur-bowden-au-metre) |
| Connecteurs servo JR trois broches | 2 jeux en plus des 9 du kit | plafond 0,40 € | 0,80 € | [Connectique AMPUL](https://ampul.eu/fr/1207-composants) |
| **Ajout au matériel de la V5** | | | **13,10 €** | |

Les deux MG90S commandent les tambours du socle. Leurs courses utiles sont de ±60° et ±72°. Contrôler la plage de position réelle du lot et le palonnier fourni. Le nylon Ø0,40 mm du kit sert aussi aux quatre brins de roulis. Prélever dans les coffrets les vis et rondelles M3 des supports et des chapeaux, la petite visserie M2 des servos et des deux butées et leurs écrous. Les paliers fendus, les tambours et les guides sont des pièces imprimées.

## Panier complet à 149,48 €

Pour un achat depuis zéro, choisir **cinq SG90 MakerMind** pour les doigts, soit **7,75 €** au palier de cinq pièces, et **deux Tower Pro SG90** pour le socle et le poignet, soit **8,98 €**. Le total des sept SG90 devient 16,73 €. Les microservos de main restent de position, un par doigt, au même gabarit annoncé de 23 × 12,2 × 29 mm. La référence économique est donnée pour un couple au blocage de 1,5 kgf·cm à 4,8 V. Vérifier le centrage, les oreilles et l’entraînement du palonnier sur un exemplaire avant le montage complet. [SG90 MakerMind](https://www.makermind.fr/p/servomoteur-micro-sg90-9g-pour-modelisme-rc-avion-projets-arduino) · [Tower Pro SG90](https://www.makermind.fr/p/tower-pro-sg90-servo-micro-analogique-9g)

Calcul TTC avec les frais de port inclus dans la base à 148,98 €. On retire 29,33 € pour la ligne des sept SG90, puis on ajoute 16,73 € et les 13,10 € de la modification. **Total cible 149,48 €.** Ce total suppose que le tube et les moteurs arrivent dans le colis MakerMind prévu et que les autres plafonds et retraits du panier V5 sont respectés. Le panier avec sept Tower Pro neufs et les deux axes ajoutés cible **162,08 €**. Si les pièces de la V5 sont déjà achetées, prévoir le seul complément de 13,10 € plus le port d’une éventuelle commande séparée. [Port MakerMind](https://www.makermind.fr/c/informations/livraison-et-paiement/) · [Base de calcul et quincaillerie](../archives/v5-revue/ACHATS.md)

## Alimentation pendant la mise au point

Le bloc fermé **5 V / 10 A** de la V5 est le scénario chiffré pour les essais progressifs, avec mesure du courant et mouvements limités par groupes. L’addition des hypothèses de pointe de 0,90 A pour chacun des neuf micros et 1,60 A pour chacun des deux MG996R donne **11,3 A**. Les appels de courant du lot et le maintien des autres axes doivent être mesurés avant d’autoriser des mouvements simultanés. Dimensionner protections, distribution et connecteurs aux valeurs mesurées. Pour une alimentation dédiée à l’ensemble des axes, le **Mean Well LRS-75-5, 5 V / 14 A** est affiché à **17,09 € TTC** pour le module seul. Chiffrer le port, le coffret et son intégration par une personne qualifiée séparément. [Module TME](https://www.tme.eu/fr/details/lrs-75-5/alimentations-integrees/mean-well/) · [Fiche Mean Well](https://www.meanwell.eu/Upload/PDF/LRS-75/LRS-75-SPEC.PDF)
