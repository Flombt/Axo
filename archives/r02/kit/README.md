# AURA-01 · Kit V3 articulé r02

[Ouvrir la révision r02 dans Fusion](https://epitech619.autodesk360.com/g/projects/202611211172950976/data/dXJuOmFkc2sud2lwcHJvZDpmcy5mb2xkZXI6Y28uS0w2NDZueTlSV3VLYXF5Z2ZkN196UQ/dXJuOmFkc2sud2lwcHJvZDpkbS5saW5lYWdlOnEzejJrOTBFUjlDbGt0WHA4TFhRNXc)

## Documents

- [Présentation animée dans Blender](AURA-01_Bras_Robotique_r02_Presentation.blend) · six clips successifs, 30 s à 24 images/s. Espace lance la lecture depuis la vue caméra. La scène de présentation conserve la mise à l’échelle de la session Blender. Pour la fabrication, utiliser les STL du kit.
- [Notice de montage A4 paysage](Notice_Montage_AURA-01_r02.pdf) · 26 pages illustrées, du coupon aux premiers mouvements.
- [Manuel technique](Manuel_Technique_AURA-01_r02.pdf) · jeux, schéma électrique, câblage et calibration.
- [Guide de dépannage](Depannage_AURA-01_r02.pdf) · diagnostic, dépose et remplacement par référence.
- [Inventaire](Inventaire_Kit_AURA-01_r02.csv) · CSV UTF-8 avec virgules, quantités, pages, fichiers et liens d’achat connus.
- [Panier Amazon.fr et achats restants](ACHATS_AMAZON_R02.md) · 24 offres vérifiées le 23 novembre 2026, quantités utiles et contrôles à faire sur établi.
- Quatre servos de position, trois MG90S et un MG996R. L’inventaire donne les liens d’achat vérifiés.

## Fabrication

- [Ouvrir le bras dans Blender](AURA-01_Bras_Robotique_r02.blend) · 77 composants et 94 maillages dans la pose de référence. Les liaisons et l’historique CAO restent dans Fusion.
- [Assemblage natif avec liaisons](AURA-01_V3_Articulee_Montage_r02.f3d) · [STEP de l’assemblage](AURA-01_V3_Articulee_Montage_r02.step).
- [STL](STL/) · 19 références, dont cinq types de phalange, et un coupon.
- [Plateaux PrusaSlicer](Plateaux_PrusaSlicer/) · commencer avec `00_Coupon_Jeux.3mf` puis une série d’index IMP-18, IMP-15, IMP-19.
- [Vues Fusion](Vues_Fusion/) · PNG éclatés et montés, plus trois scènes F3D éditables.
- [Firmware Nano](Firmware/AURA009_Atelier/AURA009_Atelier.ino) · [notes de compilation](Firmware/Verification_Logiciel.md).
- [Démonstration Fusion](AURA-01_Demo_Bras_Poignet_Phalanges_r02.mp4) · épaule et coude, roulis du poignet, flexion et ouverture des doigts.

Les plateaux robot regroupent 29 pièces et environ 195 g de PETG dans le profil d’essai. Les segments 2 et 3 reposent sur des faces plus planes dans les STL et 3MF définitifs. Adapter température, adhérence et retrait des supports à l’imprimante.

## Vérifications effectuées

- Ancienne r01, document Fusion v2. Sur dix poses échantillonnées, le jeu à la racine du pouce descendait à 0,27 mm. Aucun chevauchement volumique n’a été reproduit.
- r02. Support de pouce démontable, tige lisse commune aux quatre doigts droits et cassette J7 accessible par l’avant. Alésages Ø2,40 à toit pointu et guides nylon ouverts après correction du maillage. Nouveau renvoi du pouce pour obtenir une traction dans le sens de la flexion.
- 72 poses globales, 72 positions ciblées pouce/index, 48 chemins et 598 positions de montage contrôlés en CAO. Les segments d’épaule et de coude ont aussi été introduits numériquement depuis le dessus à pas de 0,5 mm. [Mesures Fusion](Verification_Montage.json) · [Emboîtements](Verification_Emboitements.json).
- 20 maillages contrôlés, 20 tranchages unitaires et 5 plateaux vérifiés avec PrusaSlicer 2.9.6. [Résultats du tranchage](Verification_Tranchage.json).

L’impression, le montage, les vis et palonniers du lot, la liberté du faisceau, la tenue thermique du coude et la prise d’objet restent à vérifier sur établi. La première impression utile est l’index et le coupon. Les mouvements combinés en CAO ont été évalués par poses échantillonnées. Le programme embarqué fait un cycle séquentiel à vide.
