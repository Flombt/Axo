# AURA-01 V5 · Achats pour la revue design

**Budget cible de 148,98 € TTC livré en France métropolitaine**, avec retrait local du nylon, de l’élastique et des petites fournitures. Le total comprend les plafonds de certains lots et frais de port. Les prix relevés le 24 novembre 2026 et les plafonds sont indiqués ci-dessous. Les pièces imprimées sont hors budget. [Modèle Fusion de la revue](fusion/AURA-01_V5_Revue_Design.f3d)

## Moteurs, commande et roulements

| Pièce | Quantité à acheter | Prix unitaire / lot | Total | Lien |
|---|---:|---:|---:|---|
| Tower Pro SG90 analogique de position, RBS15198 | 7 | 4,19 € au palier de 5 à 19 | 29,33 € | [MakerMind](https://www.makermind.fr/p/tower-pro-sg90-servo-micro-analogique-9g) |
| MG996R **de position 180°**, épaule J2 et coude J3 | 2 | 7,59 € au palier de 2 | 15,18 € | [Atelier de la Robotique](https://www.atelierdelarobotique.fr/produit/servomoteur-numerique-mg996r-15-kg-cm) |
| Raspberry Pi Pico 2 RP2350, 51 × 21 mm | 1 | 7,15 € | 7,15 € | [MakerMind](https://www.makermind.fr/p/raspberry-pi-pico-2-rp2350) |
| Roulements 608.ZZ, 8 × 22 × 7 mm | 2 à monter, 1 lot de 10 à acheter | 3,95 € | 3,95 € | [MakerMind](https://www.makermind.fr/p/10-x-roulements-a-billes-608.zz-8-22-7-mm) |
| Câble USB-A vers micro-B **données** | 1 | plafond 3,00 € | 3,00 € | [MakerMind](https://www.makermind.fr/c/cables/cable-usb/) |
| Port MakerMind | 1 colis | 6,95 € | 6,95 € | [Tarif France](https://www.makermind.fr/c/informations/livraison-et-paiement/) |
| Port Atelier de la Robotique | 1 colis en relais | 4,99 € | 4,99 € | [Tarif France](https://www.atelierdelarobotique.fr/livraison) |
| **Sous-total** | | | **70,55 €** | |

Les sept SG90 se répartissent entre le socle, le roulis du poignet et les cinq doigts. Les deux MG996R de l’Atelier sont la référence économique envisagée pour les emplacements existants. Le gabarit annoncé fait 40,7 × 19,7 × 43 mm. Mesurer les oreilles et le palonnier du lot reçu avant de figer les supports. Si la remise par deux disparaît et que le prix revient à 7,99 € l’unité, le panier cible atteint 149,78 €. Une carte Pico RP2040 déjà disponible peut servir dans la même enveloppe et économise 7,15 €. [SG90 d’origine](https://towerpro.com.tw/product/sg90-analog/) · [MG996R proposé](https://www.atelierdelarobotique.fr/produit/servomoteur-numerique-mg996r-15-kg-cm) · [Cartes Pico](https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html)

## Alimentation et faisceau

| Pièce | Quantité | Montant retenu | Lien |
|---|---:|---:|---|
| Bloc secteur **externe fermé 5 V / 10 A**, AMPUL AM5120 | 1 | 29,00 € estimés à partir du tarif affiché | [AMPUL](https://ampul.eu/fr/alimentations-enfichables/3689-prise-d-alimentation-5v-10a-55x25mm) |
| Cordon secteur européen adapté au bloc si absent du lot | 1 | plafond 2,30 € | [Cordons AMPUL](https://ampul.eu/fr/1529-cables-d-alimentation) |
| Connecteurs polarisés XT60 et distribution isolée à deux pôles | 1 paire + 1 répartiteur par pôle | plafond 3,30 € | [Connecteurs](https://ampul.eu/en/1501-dc-and-xt60-power-connectors) · [Bornes](https://ampul.eu/fr/1306-bornes-de-raccordement-raccords) |
| Fil souple cuivre 1–1,5 mm² pour le tronc fixe | 1 m rouge + 1 m noir | plafond 1,30 € | [Fils AMPUL](https://ampul.eu/en/1503-wires-and-cables-by-the-meter) |
| Fil souple 0,50 mm² pour l’alimentation mobile, 0,25–0,35 mm² aux branches, 0,14–0,25 mm² aux signaux | environ 4 m de conducteurs au total, à recouper au montage | plafond 2,70 € | [Fils AMPUL](https://ampul.eu/en/1503-wires-and-cables-by-the-meter) |
| Connecteurs servo 3 broches, format JR 2,54 mm compatible avec les servos livrés | 9 jeux, avec fils présertis si possible | plafond 3,60 € | [Connectique AMPUL](https://ampul.eu/fr/1207-composants) |
| Coupe-circuit sur l’alimentation moteur, 10 A CC minimum | 1 | plafond 2,20 € | [Interrupteurs AMPUL](https://ampul.eu/fr/1417-interrupteurs-a-bascule) |
| Porte-fusibles avec fusibles et protections des départs | 1 général 10 A, 2 départs MG 2 A, 3 groupes SG de 2/2/3 A | plafond 5,50 € | [Fusibles et supports AMPUL](https://ampul.eu/fr/1247-fusibles) |
| Gaine thermorétractable, maintien souple du faisceau | 1 petit lot | plafond 1,60 € | [Consommables AMPUL](https://ampul.eu/fr/1207-composants) |
| Port AMPUL | 1 colis | enveloppe 8,50 € | [Tarif selon adresse](https://ampul.eu/fr/content/1-livraison-et-paiement) |
| **Sous-total cible** | | **60,00 €** | |

Le 5 V externe alimente les servos. Le Pico reçoit son alimentation par USB avec une masse commune côté basse tension. Le dimensionnement provisoire de 9,5 A suppose 1,6 A par MG996R et 0,9 A par SG90 en pointe. Le courant des unités reçues et la coupure sont à contrôler avant de lancer des mouvements simultanés. Prévoir une sortie CC et des connecteurs réellement prévus pour 10 A. Si le courant admissible de la prise fournie est inférieur ou inconnu, faire équiper la sortie basse tension d’un XT60 compatible par l’atelier. Le bloc secteur reste fermé. [Caractéristiques du bloc](https://ampul.eu/fr/alimentations-enfichables/3689-prise-d-alimentation-5v-10a-55x25mm)

## Quincaillerie et traction à acheter

| Pièce | Quantité | Montant retenu | Lien |
|---|---:|---:|---|
| Boulon M8×55 partiellement fileté, écrou frein et rondelles M8 | 1 + 1 + 2 | plafond 2,35 € | [Vis Express](https://www.vis-express.fr/corps-de-boulon-filetage-partiel-inox-a2-tete-hexagonale-th-din-931-iso-4014-din931iso4014vs4109vs0100/18783-2606230-corps-de-boulon-filetage-partiel-inox-a2-tete-hexagonale-th-m8x55.html) |
| Boulons M5×70 partiellement filetés, écrous frein M5 | 2 + 2 | plafond 3,00 € | [Vis Express](https://www.vis-express.fr/corps-de-boulon-filetage-partiel-tete-hexagonale-th-inox-a4-din-931-din931vs4109vs0100/20693-corps-de-boulon-filetage-partiel-tete-hexagonale-th-m5x70-inox-a4.html) |
| Ancrages M5 pour la planche de support | 4, prévoir M5×35 à M5×40 pour une planche de 20–25 mm | plafond 1,60 € | [Visserie au détail](https://www.bricovis.fr/visserie/vis-pour-metaux/) |
| Tige acier lisse Ø2 mm, axe des quatre doigts longs coupé à 47,56 mm | 1 longueur | plafond 0,89 € en retrait groupé ou à la coupe | [Flash RC](https://www.flashrc.com/fr/corde-a-piano-acier/3149-corde-a-piano-cap-20mm.html) |
| Retrait / envoi groupé de la quincaillerie | 1 | enveloppe 2,11 € | [Modes de retrait et de livraison](https://www.bricovis.fr/questions-frequentes/quels-sont-les-differents-modes-de-livraison-11/) |
| Nylon de pêche Ø0,40 mm pour les cinq tendons | 1 bobine | 2,49 € | [Decathlon LINE 4X4](https://www.decathlon.fr/p/fil-de-peche-line-4x4-250m/_/R-p-194133?c=blanc) |
| Élastique latex rond Ø1 mm pour les cinq rappels, variante 8648696 | 1 lot de 6 m | 5,99 € | [Decathlon](https://www.decathlon.fr/p/elastique-plein-en-latex-pf-pa-se-500-1mm-6m/334221/c36m8648696) |
| **Sous-total cible** | | **18,43 €** | |

Les prix au détail ci-dessus supposent un retrait local ou groupé. Avec les autres montants du tableau, le port AMPUL peut atteindre **9,52 €** avant de franchir 150 €. Un câble USB de données déjà disponible libère 3,00 € de marge. Vérifier le total livré avant validation du panier, notamment pour la tige d’acier si elle doit être expédiée seule.

## Vis et fournitures à réutiliser

| À sortir des coffrets | Quantité à préparer | Où les prendre |
|---|---:|---|
| Vis métriques M2 à appui plat pour les pivots, longueur cible 10 mm | 13 | M2×12 du coffret noir, à raccourcir proprement de 2 mm si nécessaire et à présenter sans forcer |
| M2 courtes et rondelles/écrous M2 pour les micros et les attaches de la main | prévoir 20 à 24 | Coffret Swpeet M2×4/5/6 et vis fournies avec les servos. Retenir la longueur et l’appui après montage à blanc. |
| M3 CHC ×8/12/16/20, écrous et rondelles | prévoir 24 vis, assortiment | Coffret noir pour les têtes cylindriques. Écrous/rondelles des coffrets noir et orange. |
| M4×8/12, rondelles et écrous M4/M5 | 2 vis de butée et un assortiment | Coffrets noir et orange. |

Les vis argentées des coffrets jaune 2 400 et rouge 537 sont autotaraudeuses. Réserver les pivots, vis traversantes et écrous aux vrais filetages métriques, avec une tête adaptée à l’appui. Vérifier le stock restant d’après les boîtes ouvertes. Les longueurs définitives des vis du capot seront fixées avec le modèle validé.
