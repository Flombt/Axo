# Contexte projet · V5-stabilisation

**25 novembre 2026**

AURA-01 est un bras robotique de table FDM destiné à déplacer et saisir de petits objets au banc. Le plafond est de **150 € TTC**, avec **100 €** visés. Le filament en stock vaut **0 €** au panier.

- **Architecture.** Quatre axes de bras et cinq commandes indépendantes de doigts. Les anciens roulis J2R/J3R ont été remplacés par deux liaisons fixes, intégrées aux tourillons. Le lacet traverse un axe Ø10/8 dans deux 6000-ZZ. [CAO](../../fusion/README.md)
- **Plan de pose.** Rehausses sur quatre tirants M5 et nouvelles lumières de butée. Ressorts de compensation à J2/J3 et limite couplée du firmware. La garde rigide calculée reste positive dans le scénario sans courant avec butées intactes. [Calculs](../diagnostic/corrections/calculs.json)
- **Main.** P3 modifiée, écart pouce-index de 3,70 mm dans la meilleure pose native. Les cinq tendeurs, les rappels et les embouts PTFE demandent qualification. [Corrections](../../RAPPORT_CORRECTIONS.md)
- **Puissance.** Pico 2 et neuf PWM. Enveloppe de pointe de 11,30 A, coupure matérielle prévue et bloc externe en basse tension. [Électronique](../../electronics/README.md) · [Firmware compilé](../../firmware/README.md)
- **Impression.** Les maillages, orientations et plateaux PETG proviennent du F3D indiqué dans le manifeste. Les coupons précèdent la fabrication du bras. [Fabrication](../../manufacturing/README.md)
- **Qualification.** Aucune mise en mouvement physique. Valider le lot mécanique, les capteurs, ressorts, visserie, faisceau et la chaîne de coupure. Le panier de travail dépasse 150 € avec les provisions actuelles. [Achats](../../purchases/NOMENCLATURE.md) · [Plan de montage](../../assembly/README.md)

Partir de [VERSION.md](../../VERSION.md) et des [règles](../../AGENTS.md). La V5 roulis v1 reste restaurable par son point de reprise Git et sa référence Fusion. [Archives](../../archives/README.md)

## V5 Roulis à socle plat

Le montage à blanc demandé utilise la variante passive de la V5 Roulis et ses six axes. Les corrections portent sur les butées de descente et la retenue du poignet. La vérification et l’inventaire du kit sont liés au F3D de cette variante. [Dossier du montage manuel](../diagnostic/montage_manuel/README.md)

## Axo bras final · Vision et audio

La copie **Axo bras final - Capteurs** reprend le F3D de **Axo_bras_final v1**. Le Pi 5, la caméra et le micro sont implantés sur un module fixe repris sur deux ancrages M5 du socle. Le calcul de perception et le pilotage moteur restent deux fonctions matérielles distinctes. [CAO, alimentation et essais](<../../Axo bras final - Capteurs/LISEZ_MOI.md>)
