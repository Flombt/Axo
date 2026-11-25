# Firmware · V5-stabilisation

Commande Pico 2 RP2350 à neuf voies. Le PC envoie des valeurs en degrés et les ordres passent par le superviseur local. [Brochage et coupure](../electronics/README.md) · [Enveloppe dans le code](enveloppe.py)

## Démarrage et calibration

Au démarrage, la permission de puissance et l’autorisation de PWM sont à zéro. L’absence de calibration valide laisse les deux inhibées. Le profil est un fichier local `calibration.json` sur le Pico. Il porte la clé `revision` égale à `V5-stabilisation`, le dictionnaire `pwm_us` de paires croissantes `[degrés, microsecondes]` pour chaque GPIO servo et `pitch_adc_u16` de paires `[degrés, lecture ADC]` pour J2/J3. Les courbes doivent être monotones, couvrir leurs courses de consigne et distinguer ouverture, du zéro mécanique et de la fin de course. `rail_adc_v_max` représente la tension équivalente à 65 535 points d’ADC. Mesurer le diviseur à des tensions connues.

Relever les largeurs d’impulsion sur un banc qui n’entraîne que le servo en cours. Présenter ensuite le palonnier et vérifier les positions mécaniques avec les transmissions déchargées. Étalonner les capteurs J2/J3 de façon indépendante. À la mise en service de l’ensemble, placer le bras dans le gabarit de parc, tangages et lacets à zéro, doigts ouverts. Vérifier manuellement les axes dépourvus de retour angulaire. Activer MARCHE, envoyer des PING, puis presser ARM local après relâchement du bouton. Le logiciel vérifie un rail stable et les deux tangages au parc, avant d’exposer la première consigne.

## Protocole USB

| Entrée | Effet |
|---|---|
| `PING` | Répond `PONG`. Envoyer toutes les 100 ms en fonctionnement. Une absence de plus de 350 ms désarme. |
| `MOVE J1 10 J2 4 Servo_I 35` | Vérifie toute la commande, change les cibles ensemble et rampe vers elles. |
| `STATUS` | Renvoie état, cause éventuelle, cibles, consignes émises, tangages mesurés, courant et tension. |
| `STOP` | Retire l’autorisation des impulsions et de puissance, mémorise l’arrêt. |
| `RESET` | Efface l’état de défaut à rail bas, arrêt matériel rétabli. La reprise requiert ensuite MARCHE et ARM. |

Les ordres inconnus, axes répétés, nombres non finis, sorties de course et transitions à garde basse sont refusés. Les retours J2/J3 permettent de relever un écart de suivi et de perdre la permission au-delà du seuil. Le courant total ne suffit pas à reconnaître tous les blocages ou débranchements des sept autres axes. Les seuils et l’arrêt sont à éprouver avec des charges factices avant raccordement complet.

## Reproduction des essais

Lancer `python -B -X utf8 firmware/test_controle.py` depuis la racine. Compiler `enveloppe.py`, `controle.py` et `main.py` avec MicroPython mpy-cross compatible RP2350. Les essais hôte et la compilation ont des preuves distinctes du démarrage sur carte. [Preuve logicielle](../docs/diagnostic/corrections/firmware.json)
