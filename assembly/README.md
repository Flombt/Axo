# Montage et qualification · V5-stabilisation

Cette notice sert au montage à blanc et à la qualification progressive. Les pièces s’identifient par leur repère Fusion et le nombre de corps à imprimer dans l’inventaire. [CAO](../fusion/AURA-01.f3d) · [Inventaire](../manufacturing/inventaire.json) · [Corrections et preuves](../RAPPORT_CORRECTIONS.md)

## Montage à blanc

1. Présenter les éprouvettes de portées, axes, servo et doigt. Relever diamètres dans les deux axes, alésages après retrait des supports, vis traversantes et inserts du lot. Confirmer le serrage sans déformation et le maintien de la bague extérieure dans chaque logement.
2. Installer les quatre entretoises de 90 mm et leur tirant M5 sur un support rigide. Les trous de la platine sont sur un rectangle **129 × 94 mm**. Longueur utile minimale d’un tirant à calculer avec l’épaisseur du support, les deux rondelles et les écrous. Vérifier la portée des quatre pieds et l’accès sous platine avant fermeture.
3. Poser les 6000-ZZ dans les deux logements, celui du dessous avant appui de la platine. Présenter la pile des bagues intérieures, l’entretoise et sa rondelle, puis engager le tube Ø10/8. Les deux colliers reprennent le maintien axial par les bagues intérieures. Enlever le jeu sans serrer sur les flasques. Vérifier le libre passage d’un calibre et la continuité du faisceau défait de ses connecteurs avant de poser la roue et la tourelle.
4. Présenter J2 puis J3. Mesurer le passage des axes M5 côté tête et écrou ainsi que la portée lisse effective dans les deux joues. Les gabarits CAO font environ 57 mm hors tout. À l’essai, la portée lisse couvre les deux appuis et le filet sort de la portée. Engager les vis de butée et vérifier à la main leur capture dans les lumières de chaque roue. Laisser les protections démontées pendant les mesures.
5. Mettre en place la cassette de doigts, le J7 et la paume. Insérer l’axe commun Ø2 des quatre doigts, poser ses retenues, puis la chape du pouce. Passer les cinq brins dans leurs voies et les tubes du guide de poignet avant d’installer les rappels. Repérer tête et retour de chaque doigt. Prévoir une extrémité réglable au tambour et un arrêt captif au doigt. Vérifier que le rappel décharge le tambour quand l’impulsion s’arrête, sans bloquer la phalange.
6. Poser les tiges M5 de compensation et leurs œillets. Monter les ressorts un par un avec le bras immobilisé sur la retenue du banc. Relever la longueur entre œillets aux bornes. Contrôler les retenues filetées des deux axes de ressort. Ajuster la précharge des disques en mesurant l’effort de décollage au lieu de déduire le couple du serrage des écrous.
7. Raccorder le faisceau de puissance et les signaux après contrôle de la masse, de la polarité et des fusibles. Laisser libres les longueurs entre brides des boucles de service. Balayer J1, J2, J3 et J7 à la main sous retenue, et vérifier que les capots ferment sans pincer les fils ou recouvrir les outils. [Électronique et coupure](../electronics/README.md)

## Déposer les moteurs

| Moteur | Gestes avant translation | Direction sondée en CAO |
|---|---|---|
| J1 | Débrancher la fiche et retirer coque, pignon et porte-servo. Accès par-dessous si nécessaire. | −X au neutre dans l’audit de départ |
| J2 | Retirer coque d’épaule, garde et pignon. Reprendre les ressorts sur la retenue et débrider le faisceau avant translation. | +Y de 8 mm puis −X de 32 mm au neutre |
| J3 | Retirer coque, garde, pignon, embout et disque extérieur de friction, bras captif. Déposer les ressorts et la tige qui chargent le support. Débrider les boucles, enlever les quatre M4 et sortir le support de service vers +Y. | +Y au neutre |
| J7 | Retirer coque, capots, palonnier, support et cassette des cinq micros. Protéger les cinq brins lors de la descente. | −Z au neutre |
| SG90 de doigt | Retirer cassette et détendre le brin de la voie. Débrancher ensuite le seul servo concerné. | Cassette −Z, intervention individuelle sur établi |

[J2 en deux mouvements](../docs/diagnostic/corrections/deposes_alternatives.json) · [Support J3](../docs/diagnostic/corrections/support_service_j3.json) · [Couloir J3](../docs/diagnostic/corrections/depose_support_service.json) · [Contre-vérification des poses](../docs/diagnostic/corrections/campagne_fusion.json)

## Essais matériels à préparer

- **FDM et fixation.** Vérifier tube, lubrification admissible, appuis, serrage, tourillons, dents module 0,8, jeu, concentricité et débattement de chaque outil. Examiner les portées et les attaches après essais répétés.
- **Retenue.** Utiliser une retenue de banc indépendante et mesurer le couple de décollage dans les deux sens, à froid puis à chaud, à vide et avec charges inertes de 10 puis 20 g attachées. Mesurer la dérive à l’arrêt et lors d’une perte de couple. Une précharge excessive qui impose trop de couple moteur invalide le réglage.
- **Transmission.** Mesurer le couple continu exploitable de chaque tangage, le courant, l’échauffement, le jeu et la répétabilité à plusieurs positions. Les valeurs commerciales de blocage servent de comparaison. Contrôler l’orientation imprimée, les vis du palonnier et les butées sous l’énergie de fin de course.
- **Faisceau et doigts.** Suivre les rayons, la course libre et les efforts aux deux bornes du câble. Éprouver chaque fil sur un tambour et un doigt avant la cassette complète. Mesurer l’ouverture, le retour et le déplacement des autres doigts au poignet tourné. Vérifier pince et cylindre avec des éprouvettes retenues.
- **Alimentation et reprise.** Qualifier le rail sur charge factice avant connexion des servos. Vérifier courant, creux, surintensité, coupure et reprise avec USB maintenu. À l’arrêt le bras doit rester sous retenue et une charge de test reste attachée à une retenue distincte.
