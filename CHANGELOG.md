# Évolutions significatives d’AURA-01

## 2026-11-25 · V5-roulis-montage-manuel

- Reprend la V5 Roulis v1 à socle plat. Retouche les lumières de butée J2 et J3 et ajoute la retenue vissée du poignet en montage manuel.
- Vérifie la réimportation F3D, vingt poses passives et quatre projets Anycubic. Ferme deux coutures de maillage de la coque du bras.
- Cadre la présentation Fusion en mode Qualité et rend la configuration manuelle à partir des solides natifs. [Contrôles et montage](docs/diagnostic/montage_manuel/README.md)

## 2026-11-25 · V5-stabilisation

- Réintègre les deux raccords longitudinaux aux pièces de tangage. Reprend l’axe J1 traversant, ses 6000-ZZ, les guides de faisceau et les peignes de poignet.
- Ajoute les rehausses, les butées de tangage et les reprises de compensation, de démontage et de pince.
- Livre le STEP, les maillages, éprouvettes et projets Anycubic issus du modèle stabilisé.
- Implémente neuf voies Pico 2 avec surveillance, enveloppe couplée et reprise volontaire. Compile les trois modules en MicroPython.
- Recompte le panier avec filament à 0 €, documente les essais et conserve la V5 roulis au tag `aura-01-v5-roulis-v1`.

## 2026-11-24 · V5 roulis et organisation du projet

- Deux axes motorisés J2R et J3R, cinq commandes de doigts, six axes de bras et onze servos. La CAO v1 est la source active. [Version](VERSION.md)
- Audit indépendant, absence de paquet de production cohérent pour la V5, vérification sur copie Fusion et trois plateaux historiques. [Rapport](DIAGNOSTIC_ROBOT_COMPLET.md)
- Dossiers actifs regroupés, archives par révision, copies de transfert dédupliquées et vérification en lecture seule. [Réorganisation](docs/REORGANISATION_PROJET.md)

## 2026-11-24 · V5 revue design et r05

- V5 revue avec cinq SG90 de main, poignet motorisé et cassette plus étroite. Variante parent de la V5 roulis. [Archive](archives/v5-revue/README.md)
- r05 Budget Edition avec six servos, trois canaux de main, poignet manuel, Pico USB et dossier Anycubic sur trois machines. [Archive](archives/r05/README.md) · [Commit de référence](https://github.com/Flombt/Axo/commit/ecc2308ec4521cbc6c49ad148433d983fa783578)

## 2026-11-23 au 2026-11-24 · Bras de table r02 à r04

- r02, kit à quatre voies Nano, notice et démonstration de montage. [Archive](archives/r02/README.md)
- r03, articulations portées et faisceau repris, kit tranché et animation de référence. [Archive](archives/r03/README.md)
- r04, socle continu alimenté par collecteur et cinq doigts indépendants. [Archive](archives/r04/README.md)

[Révisions antérieures, bancs et provenance](archives/README.md)
