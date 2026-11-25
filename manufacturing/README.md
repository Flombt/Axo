# Fabrication · V5-stabilisation

La **V5 Roulis à socle plat** dispose de son [kit pour montage manuel](AURA-01_V5_Roulis_Montage_Manuel.zip) avec un plateau de premiers essais. [Nomenclature, montage et contrôles](../docs/diagnostic/montage_manuel/README.md)

Ce dossier prépare la qualification progressive. Le STEP de l’assemblage et les maillages des pièces proviennent du même document Fusion. Le STEP réimporté dans Fusion contient 156 solides fermés. Les 3MF individuels contiennent leur géométrie orientée en millimètres. Les projets Anycubic enregistrent les réglages et les couches calculées. [STEP](AURA-01.step) · [Vérification STEP](../docs/diagnostic/corrections/step_reouverture.json) · [STL](STL/) · [3MF individuels](3MF/) · [Inventaire par pièce et empreintes](inventaire.json)

## Ordre de travail

1. **Coupons.** Imprimer les éprouvettes de roulements 6000, d’axes, d’empreintes moteurs et d’inserts. Le tableau d’axes compare trous verticaux et horizontaux. Les roues et pignons sont les mêmes solides que ceux du bras.
2. **Doigt.** Le plateau dédié emploie la P3 corrigée et ses supports, à la même hauteur de couche que la main. Retirer les supports, présenter la vis et l’attache du tendon, puis mesurer ouverture et rappel.
3. **Socle.** Vérifier les portées 6000, le passage axial, le jeu et les quatre rehausses. Présenter sur un support rigide avant la fabrication des segments.
4. **Bras.** Contrôler après retrait des supports les paliers d’axe en double cisaillement, les attaches de ressort, les lumières de butée et la dépose des moteurs.
5. **Main.** Poser les cinq voies individuellement. Contrôler jeu, retenues, trous des peignes et maintien des serre-tendons avant un cycle complet.

Les coupons sont à mesurer avec le filament réellement disponible. Sa quantité et sa nature déterminent la fenêtre de température et l’adhésion. Le panier chiffre le filament fourni à 0 €. [Achats](../purchases/NOMENCLATURE.md) · [Montage à blanc](../assembly/README.md)

## Maillages et orientations

**49 références de robot, 62 occurrences**, et **cinq références dédiées d’éprouvettes**. L’inventaire liste les repères, quantités, volumes BRep et maillage, enveloppes et matrices d’orientation. Les formes différentes sous une ancienne référence commune sont exportées séparément. Les maillages ont été contrôlés en volume, fermeture, orientation et réouverture 3MF. Deux coutures locales de tessellation ont été corrigées sur les coques en conservant les sommets utiles de surface. L’écart volumique du capot de cassette découle de la tessellation et reste tracé.

Les axes des pièces porteuses guident l’orientation proposée. Les trous horizontaux, supports proches des bores, surfaces de frottement et attaches de tendon nécessitent inspection en coupe de couches et mesure des coupons. La résistance intercouche et le fluage demandent une épreuve de charge. [Données natives](../docs/diagnostic/corrections/geometrie_neutre.json) · [Reproduction](../tools/preparer_impression.py)

## Projets Anycubic

| Machine | Enveloppe nominale utilisée | Projets |
|---|---|---|
| Kobra 3, buse 0,4 mm | 250 × 250 × 260 mm | [Socle, bras, main et qualification](Anycubic/Kobra_3/) |
| Kobra X, buse 0,4 mm | 260 × 260 × 260 mm | [Socle, bras, main et qualification](Anycubic/Kobra_X/) |
| Kobra 3 Max, buse 0,4 mm | 420 × 420 × 500 mm | [Socle, bras, main et qualification](Anycubic/Kobra_3_Max/) |

Les profils sont présents dans l’installation. L’atelier Anycubic ne montre aucune machine appairée dans ses deux onglets. Vérifier la machine et le type de plaque réel avant une impression autorisée. Anycubic Slicer Next 2.0.0.3 a relu les 108 STL et 3MF individuels et tranché puis réouvert les 17 plateaux. Les fichiers de contrôle indiquent les supports, les temps, les grammes, les avertissements et les emprises. Le moteur signale la température du plateau par rapport au filament et la disponibilité du timelapse sur certains profils. Le coupon permettra de vérifier le réglage du filament réellement en stock. [Résultats par plateau](Anycubic/verification.json) · [Contrôles individuels](Anycubic/individuels.json)

Les vérifications d’atelier commencent par les coupons et le doigt. Une reprise du fichier de fabrication se fait à partir du modèle V5-stabilisation en contrôlant l’empreinte du F3D. Les projets r05 appartiennent aux archives.
