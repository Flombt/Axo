# AURA-009 r04 · Planches couleur Anycubic

Les 53 STL de Fusion r04 v4 sont convertis en 3MF individuels. Les cinq planches couleur regroupent 61 pièces et la planche de calibration contient les sept coupons. Les copies à plat pour le transfert se trouvent dans [miroir USB historique](./).

## Choisir une planche

| Planche 3MF | Pièces | Emprise des pièces XY | Temps estimé | PETG |
| --- | ---: | ---: | ---: | ---: |
| [00 Coupons en PETG](plates/par_couleur/AURA_r04_P00_Coupons.3mf) | 7 | 262,5 × 77,9 mm | 1 h 20 min | 25,09 g |
| [01 Graphite profond](plates/par_couleur/AURA_r04_P01_Graphite.3mf) | 10 | 345,1 × 233,1 mm | 8 h 55 min | 171,89 g |
| [02 Gris perle](plates/par_couleur/AURA_r04_P02_Gris_Perle.3mf) | 17 | 224,9 × 174,3 mm | 4 h 38 min | 78,91 g |
| [03 Blanc céramique](plates/par_couleur/AURA_r04_P03_Blanc_Ceramique.3mf) | 18 | 138,8 × 135,3 mm | 2 h 45 min | 30,45 g |
| [04 Bleu pétrole](plates/par_couleur/AURA_r04_P04_Bleu_Petrole.3mf) | 14 | 144,6 × 165,1 mm | 2 h 01 min | 29,25 g |
| [05 Gris acier](plates/par_couleur/AURA_r04_P05_Gris_Acier.3mf) | 2 | 56,4 × 94,5 mm | 52 min 23 s | 14,82 g |

Total des planches couleur pour 61 pièces, environ 19 h 12 min et 325,32 g de PETG. Les deux finitions satinées de Fusion sont regroupées en gris acier. Les enrouleurs et guides imprimables reprennent le bleu pétrole du corps CAO.

Le [support de cartes J1](a_verifier/AURA_r04_J1_Chariot_Cartes.3mf) constitue la 62e pièce. Son enveloppe de 8,15 mm doit être revue avec les cartes de 8,8 à 9 mm et leurs fiches. [Validation r04](../VALIDATION_FABRICATION.md)

## Transfert sur clé USB

Les projets sont réglés sur le profil de référence Anycubic Kobra 3 Max, buse de 0,4 mm, PETG et plateau PEI texturé. Sélectionne le profil de ton modèle et de ta buse avant l’export final. La planche graphite occupe environ 345 × 233 mm avant les bordures et supports.

Pour lancer une Kobra 3 Max depuis sa prise USB, ouvre la planche 3MF dans le slicer, vérifie le profil et exporte le fichier tranché en .gcode sur la clé. Le transfert se fait sans association réseau. [Guide USB Anycubic Kobra 3 Max](https://wiki.anycubic.com/fr/error-codes/10804-code/k3-max)

Commence par la planche 00 et contrôle les ajustements des axes, roulements, inserts et fixations avant les pièces fonctionnelles.

## Vérifications

Les 59 projets ont été tranchés avec Anycubic Slicer Next 2.0.0.3. Les six planches sauvegardées ont été rouvertes et retranchées. Le contrôle confirme les quantités, les emplacements, l’échelle en millimètres, les triangles du STL source et la présence des trajectoires sur le plateau du profil de référence.

Le moteur de tranchage signale une alerte de température de plateau avec le préréglage PETG d’origine à 75 °C. Certains fichiers signalent aussi le mode time-lapse traditionnel. Vérifie la température adaptée au PETG et à la surface utilisés sur ta machine, puis laisse le time-lapse désactivé pour les essais.

[Inventaire par pièce](inventory.csv) · [Mesures et contrôles par projet](verification.json)
