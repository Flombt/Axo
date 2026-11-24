# Contexte projet · V5-roulis-v1

**24 novembre 2026**

AURA-01 est un bras robotisé expressif de table, imprimable en FDM après qualification. Il vise le mouvement coordonné et la prise de petits objets. Le budget est **150 € maximum**, avec **100 €** comme objectif de conception.

- **Mécanique.** Fusion v1, 154 occurrences. Socle J1 sur deux 608. Deux tangages portés J2/J3, deux roulis longitudinaux entraînés par gaines J2R/J3R, roulis J7 motorisé et cinq doigts à trois phalanges. [Source CAO](../../fusion/AURA-01.f3d) · [Version](../../VERSION.md)
- **Composants.** J2/J3 MG996R, deux MG90S déportés pour les deux roulis, sept SG90 pour J1/J7 et la main. Pico 2 USB, rail externe 5 V à qualifier. [Nomenclature](../../purchases/NOMENCLATURE.md) · [Électronique](../../electronics/README.md)
- **Fonctionnalités prouvées en CAO.** Six axes et cinq voies de doigts. 141 poses atteintes, 33 analyses d’interférence, pince de 17,68 mm dans le meilleur cas sondé. Aucun montage à blanc ni essai physique V5 documenté. [Audit](../../DIAGNOSTIC_ROBOT_COMPLET.md)
- **Blocages.** Descente J2/J3 à −56,68 mm. Quatre passages J1 dont les extrémités s’écartent de 33,31 à 39,45 mm à ±88°. Tenue à la coupure inconnue, limite transitoire 11,3 A face au bloc 10 A envisagé. Étudier les efforts et le réarmement avant commande ou mise sous tension. [Registre](../diagnostic/latest/REGISTRE_PROBLEMES.md)
- **Fabrication et commande.** Les exports STEP/STL/3MF et le firmware cohérents avec la V5 restent à produire. Le kit r05 et sa commande restent des archives qualifiées à des degrés différents. [Fabrication](../../manufacturing/README.md) · [Firmware](../../firmware/README.md) · [Montage](../../assembly/README.md)
- **Ordre de reprise.** Garde au plan et routage, retenue et motorisation, puissance et commande, puis paquet CAO–impression–BOM cohérent, essais d’éprouvettes et montage à blanc. [Feuille de route](../../DIAGNOSTIC_ROBOT_COMPLET.md#15-feuille-de-route-avant-fabrication)

Pour reprendre une modification, partir de [VERSION.md](../../VERSION.md), puis des [règles de maintenance](../../AGENTS.md). Les archives sont accessibles par révision si une preuve historique ou une restauration est nécessaire.
