# AURA-009 de table r05 — Budget Edition

**Révision de développement · Fusion v2.** La r04 v4 sert de référence. La r05 garde la paume et les quinze phalanges de la r04 avec une nouvelle platine, deux segments raccourcis, des axes à double appui et des transmissions RC protégées. Elle compte 105 occurrences, 104 liaisons et 18 couplages. Le projet F3D a été réimporté.

| Fonction | Choix r05 |
|---|---|
| J1 | SG90, pignon 38 / roue 22, deux roulements 608 Ø8 × 22 × 7, ±88° de commande, butées CAO vers ±92,75° |
| J2 | MG996R de position, réduction 3:1 et axe M5 |
| J3 | MG996R de position, réduction 2:1 et axe M5 |
| J7 | Roulis manuel serré par M5. Course CAO ±15°. |
| Main | P et I indépendants, majeur–annulaire–auriculaire ensemble. Cinq logements et trois SG90 installés. |
| Commande | Pico RP2040 USB et rail moteur 5 V / 8 A externe protégé |
| Achats | 149,97 € cible TTC livré avec les enveloppes du panier et le comptage des vis |

Le contrôle Fusion a évalué 85 poses, dont la fermeture des doigts et les combinaisons d’articulations. Il n’a trouvé aucun recouvrement parasite entre les solides rigides examinés. Les quatre contacts de vis de butée dans leurs logements sont conservés. La CAO et les ancrages du faisceau se mesurent au neutre et en course, avec la flexion et le rayon réel à vérifier sur banc.

Le montage reste au stade de prototype. Imprimer les coupons en premier, mesurer les deux torques de retenue, le courant de pointe et la température, puis qualifier chaque doigt et l’arrêt à la coupure. Le premier essai du code sur Pico reste à faire.

[Rapport r05](../../../archives/r05/OPTIMISATION_BUDGET_R05.md) · [Achats](../../../archives/r05/LISTE_ACHATS_R05.md) · [STL et Fusion](../../../archives/r05/fusion/README.md) · [Anycubic](../../../archives/r05/anycubic/README.md) · [[05_Electronique/README_MOTEURS_V3|Moteurs]]
