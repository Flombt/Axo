# Axo bras final · Capteurs

Variante locale issue de **Axo_bras_final v1**. Le complément forme un module fixe en deux tons, au niveau de la table, dans la largeur du socle. Il ajoute 76 mm derrière la platine et se reprend sur les deux ancrages M5 arrière, entraxe 94 mm. La coque optique correspond à une caméra orientée vers la personne placée côté module.

- [Copie Autodesk Fusion](<Axo bras final - Capteurs.f3d>) · [Copie Blender animée](<Axo bras final - Capteurs.blend>)
- [Ensemble](Images/01_Ensemble.png) · [Caméra et micro](Images/02_Camera_et_micro.png) · [Accès au Pi](Images/03_Acces_Raspberry_Pi.png)
- [Les quatre pièces à imprimer](<Impression 3D/STL/>) · [Projet Kobra 3 Max PLA](<Impression 3D/Axo_Capteurs_Kobra_3_Max_PLA.3mf>)
- [Vérification Fusion](Contr%C3%B4les/validation_fusion.json) · [Contrôle du plateau](Contr%C3%B4les/validation_impression.json)

## Vérifications numériques

Le F3D a été réimporté dans Fusion. Les 154 occurrences du bras, leurs solides et leurs repères, les 153 liaisons et les 20 liens de mouvement ont été comparés à la source. Aucune interférence ajoutée de plus de 0,03 mm³ n’a été détectée dans les 205 poses atteintes, ni entre le module et les gabarits électroniques à l’arrêt. Douze combinaisons de lacet, roulis et prise n’ont pas été atteintes par le solveur et restent hors du bilan. [Rapport Fusion](Contr%C3%B4les/validation_fusion.json)

Les quatre STL sont fermés et le 3MF a été réouvert puis retranché. Anycubic Slicer Next estime **76,8 g de PLA** et **4 h 05** sur un plateau en buse de 0,4 mm et couches de 0,20 mm, supports compris. Le réglage emploie 60 °C en PEI texturé avec 220 °C en première couche puis 210 °C à la buse. Le trancheur signale la température de plateau et la vidéo accélérée. Vérifier la plage de la bobine et le type de plaque avant impression. [Guide PLA Anycubic](https://wiki.anycubic.com/en/filament-and-resin/filament-guide)

## Montage du module

1. Présenter le bac sur la table et aligner ses deux oreilles sur le socle. Dimensionner la longueur des deux vis M5 d’ancrage pour la surépaisseur de 6 mm et conserver les rondelles. Le poids du boîtier repose sur la table. Éliminer le jeu au montage à blanc.
2. Placer le Pi 5 sur les quatre bossages, entraxe 58 × 49 mm. Prévoir quatre M2,5 à tête basse dans les logements sous le bac et quatre écrous ou dispositifs de retenue compatibles PCB. Les vis et leurs têtes doivent rester en retrait du plan de pose. Présenter le refroidisseur actif et connecter la nappe CSI 22 vers 15 broches selon la notice officielle. [Plan du Pi 5](https://pip-assets.raspberrypi.com/categories/892-raspberry-pi-5/documents/RP-008347-DS-1-raspberry-pi-5-mechanical-drawing.pdf?disposition=inline) · [Connexion caméra](https://www.raspberrypi.com/documentation/accessories/camera.html)
3. Insérer la petite carte caméra par l’arrière de sa coque, côté objectif vers le cône. Les quatre logements suivent l’entraxe 21 × 12,5 mm. Prévoir quatre M2 courtes dans les inserts de la coque, puis deux M2 fraisées et leurs inserts pour son dos. Vérifier les longueurs sur le montage réel et garder la nappe libre dans l’ouverture du couvercle, sans torsion ni contact avec la turbine. [Camera Module 3 Wide](https://www.raspberrypi.com/products/camera-module-3/?variant=camera-module-3-wide) · [Active Cooler](https://www.raspberrypi.com/products/active-cooler/)
4. Visser la coque sur le couvercle par-dessous avec deux M3 à tête fraisée. Poser les quatre vis M3 fraisées du couvercle. Les logements d’inserts Ø4,2 mm (M3) et Ø2,96 ou Ø3,1 mm (M2) se qualifient avec les inserts du lot.
5. Enficher le micro USB 3367 dans le port supérieur dégagé. Contrôler l’accès des fiches voisines, l’écoute lorsque le ventilateur tourne et le cadre caméra depuis la place réelle de l’opérateur. [Micro USB de référence](https://www.adafruit.com/product/3367)

Les gabarits électroniques dans la CAO indiquent l’encombrement. Les ajustements du lot, le passage réel des fiches et de la nappe, la température du boîtier et l’audio restent à éprouver. Le plateau PLA sert au montage à blanc. La tenue du matériau se vérifie à température stabilisée avec l’électronique en charge.

## Alimentation et commande futures

Le Pi 5 reçoit sa propre alimentation USB-C 27 W. Il alimente la caméra par la nappe CSI et le micro par USB. Les servos conservent leur alimentation séparée et le Pico 2 assure la commande bas niveau. Le câble de commande Pi–Pico reste côté socle. [Alimentation du Pi 5](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html)

Pour reproduire un geste, le Pi estimera la pose du bras et de la main à l’image, transposera les mouvements sur les axes d’Axo et produira des consignes limitées en amplitude et en vitesse. Une caméra fixe donne une estimation de profondeur qui reste à étalonner. Pour la voix, le Pi transcrira la phrase et la traduira en une commande définie, par exemple « ouvre la main ». Le Pico devra vérifier chaque consigne avant de piloter les moteurs. Le logiciel de vision et de voix, le pilotage complet onze voies et les essais physiques restent à développer ou à qualifier.

## Matériel et budget

Références pour un futur panier. Le relevé GoTronic prend le Pi 5 2 Go comme base de prix et donne **162,15 € TTC pour l’électronique seule**, hors microSD, câblage Pi–Pico, visserie et inserts. Le point relais est affiché gratuit à partir de 120 € pour cette enseigne. Le scénario tout neuf dépasse déjà le plafond de 150 € du projet. Le filament en stock compte pour **0 €**. [Conditions et livraison](https://www.gotronic.fr/faq)

| Quantité | Référence modélisée ou à prévoir | Prix TTC relevé |
|---:|---|---:|
| 1 | [Raspberry Pi 5 2 Go](https://www.gotronic.fr/cat-cartes-raspberry-pi-5-2476.htm) | 83,60 € |
| 1 | [Camera Module 3 Wide SC0874](https://www.gotronic.fr/cat-cameras-2243.htm) | 45,90 € |
| 1 | [Mini micro USB Adafruit 3367](https://www.gotronic.fr/art-microphone-dongle-usb-ada3367-33719.htm) | 6,90 € |
| 1 | [Active Cooler SC1148](https://www.gotronic.fr/art-refroidisseur-pour-raspberry-pi-5-38180.htm) | 6,90 € |
| 1 | [Bloc officiel USB-C 27 W](https://www.gotronic.fr/cat-accessoires-officiels-1565.htm) | 15,90 € |
| 1 | [Nappe CSI 300 mm SC1129](https://www.gotronic.fr/cat-nappes-2245.htm) | 2,95 € |
| 1 + 1 | Carte microSD et câble de données USB Pi–Pico | Stock à vérifier |
| 2 + 4 + 6 + 6 | M5 et rondelles, M2,5, M3 et M2 | Stock à vérifier |
| 6 + 6 | Inserts M3 et M2 | Stock à vérifier |
| 1 lot | PLA déjà disponible | 0 € |
