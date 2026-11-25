# Axe bras final

Le dossier réunit le modèle exact **Axo_bras_final v1**. Le fichier F3D de Fusion et la scène Blender animée se trouvent dans **Modèle 3D**. La vidéo MP4 se trouve à la racine et les trois angles fixes dans **Images**.

## Impression 3D

Les **69 pièces imprimables** correspondent à **58 références**. Les projets **3MF** sont répartis par sous-ensemble et le dossier **G-code** contient un fichier par plateau. Les STL et 3MF individuels sont en millimètres. Les quantités figurent dans `Impression 3D/inventaire.json`.

**Profil des G-code** · Anycubic Kobra 3 Max, buse 0,4 mm, PLA. Les plateaux ont été tranchés puis réouverts et retranchés. Le profil Anycubic sélectionné emploie une plaque PEI texturée à 65 °C et une buse à 220 °C en première couche, puis 210 °C. Comparer avec l’étiquette de la bobine et le plateau réel. Si les réglages diffèrent, adapter le projet 3MF et régénérer le G-code.

| Sous-ensemble | Plateau | Matière | Temps estimé |
|---|---:|---:|---:|
| Bras | 1 | 190.3 g | 12 h 10 |
| Main | 1 | 50.5 g | 4 h 15 |
| Socle | 1 | 236.1 g | 12 h 13 |

Les avis du trancheur sont dans le fichier de vérification joint. Le réglage de la plaque et du filament se vérifie à la première impression.

## Animation et montage

La vidéo Blender dure dix secondes. Les six axes et les cinq doigts sont animés à partir de 81 poses Fusion. L’écart maximal aux consignes est de 0.05°. Le point bas échantillonné de la main dans ce trajet est de 103.7 mm au-dessus de la table. Les gaines sont masquées car la CAO décrit leur forme au repos.

Les fichiers reproduisent la version fournie. Pour un montage manuel, vérifier les vis et roulements existants, la retenue du poignet et la course en descente. La vidéo montre une séquence CAO et le tranchage confirme la préparation numérique des plateaux. Les ajustements et la tenue se vérifient sur les pièces imprimées.
