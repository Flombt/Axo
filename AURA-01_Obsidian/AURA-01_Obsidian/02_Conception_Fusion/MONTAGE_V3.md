---
title: AURA-01 — Kit V3 articulé r02
tags: [mecanique, fusion, montage, impression-3d]
---

# Kit V3 articulé r02 — AURA-009

Révision active du bras de table à quatre servos. Trois segments, dont le dernier est solidaire de l’avant-bras. Poignet motorisé en roulis. Main blanche à cinq doigts, quinze pivots de phalange et une commande par tendons avec rappels élastiques. [[02_Conception_Fusion/MAIN_POIGNET_ECO|Version de départ AURA-008]].

## Fusion et fabrication

La révision est enregistrée séparément dans `Robotic Arm — V1` sous `AURA-01 — V3 articulée — Montage r02`, version Fusion 1. L’ancienne V3 de table r01 (Fusion v2) a été préservée. [Assemblage Fusion en ligne](https://epitech619.autodesk360.com/g/projects/202611211172950976/data/dXJuOmFkc2sud2lwcHJvZDpmcy5mb2xkZXI6Y28uS0w2NDZueTlSV3VLYXF5Z2ZkN196UQ/dXJuOmFkc2sud2lwcHJvZDpkbS5saW5lYWdlOnEzejJrOTBFUjlDbGt0WHA4TFhRNXc) · [Dossier du kit](../../../archives/r02/fusion/README.md).

| Zone | Modification r02 | Preuve |
|---|---|---|
| Pouce et paume | Chape latérale démontable, deux M2×10, pivot dégagé et renvoi lisse du tendon. | Jeux mesurés de 0,54 mm chape/phalange et 3,24 mm phalange/paume au minimum. 72 poses ciblées sur le pouce et l’index. |
| Quatre doigts alignés | Tige en acier Ø2 × 47,5–47,6 mm. Deux rondelles arrêtent ses extrémités. Les 11 autres pivots utilisent une M2×10 et un écrou captif. | Introduction vérifiée en CAO, depuis le pouce déposé. Alésages à toit pointu Ø2,40. |
| Poignet | Bride démontable côté avant, quatre M2×12. Moyeu à clé maintenu à la paume par deux M2×6. | Chemin d’emboîtement vérifié en CAO. Le servo et sa bride se déposent sans retirer le troisième segment. |
| Supports et guides | Canaux dégagés pour l’aiguille, jeux des pivots et accès aux écrous repris. Quatre entretoises M4 de 20 mm sous la platine. | 48 opérations et 598 positions calculées. 29 pièces de robot sur quatre 3MF et un coupon sur un cinquième. |
| Commande | Nano compatible 5 V · USB séparé du rail 5 V servos · un bouton. | Schéma, brochage et compilation AVR. Câblage, calibres de protection et essais électriques sur établi restant à faire. |

## Documents d’atelier

- [Kit complet à la racine du projet](../../../archives/r02/kit/README.md) · [Modèle Blender à la pose de référence](../../../archives/r02/kit/AURA-01_Bras_Robotique_r02.blend)
- [Présentation Blender animée](../../../archives/r02/kit/AURA-01_Bras_Robotique_r02_Presentation.blend) · six clips de 30 secondes au total, tirés des mouvements Fusion r02.
- [Notice de montage A4 paysage](../../../archives/r02/kit/Notice_Montage_AURA-01_r02.pdf)
- [Manuel technique](../../../archives/r02/kit/Manuel_Technique_AURA-01_r02.pdf) · [Dépannage](../../../archives/r02/kit/Depannage_AURA-01_r02.pdf)
- [Inventaire du kit](../../../archives/r02/kit/Inventaire_Kit_AURA-01_r02.csv) · [Achats et budget](../../../archives/v2/README_V2_ELEMENTS_A_ACHETER.md)
- [Panier Amazon.fr et références à valider](../../../archives/r02/kit/ACHATS_AMAZON_R02.md) · cotes relevées en direct dans Fusion r02 v1, conditionnements et points à contrôler avant montage.
- [Vidéo des articulations](../../../archives/r02/kit/AURA-01_Demo_Bras_Poignet_Phalanges_r02.mp4)
- [Données d’interférence et de montage](../../../archives/r02/fusion/Verification_Montage.json) · [Résultats du tranchage](../../../archives/r02/fusion/Verification_Tranchage.json)

## Première validation sur établi

Imprimer un index et un coupon dans le PETG retenu, puis régler le couple de vis et la réouverture. Vérifier les vis du lot de servos et le chemin des tendons avec un montage à blanc. Mesurer surtout le courant et l’échauffement du coude en appui. Ouvrir la course de roulis après contrôle de la boucle T1. La charge utile et la tenue des couches restent à qualifier. [[09_Gestion/TACHES#AURA-009 — Rendre le kit V3 assemblable|Tâche et suites]] · [[08_Tests/MATRICE_TESTS#AURA-009 — Kit V3 r02|Matrice]].
