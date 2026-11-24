# Application connectée future

Référence à la [[README#23 — Application future : direction produit|section Application future]] du cahier des charges. Voir l’[[06_IA_Logiciel/ARCHITECTURE_IA|architecture de commande]] et la [[04_Animation_Emotion/ANIMATIONS|bibliothèque des émotions]].

## Parcours MVP

- Connexion au robot ou au simulateur.
- Lecture de l'état `ready / moving / fault / disconnected`.
- Choix d'une émotion avec intensité limitée.
- Stop, HOME, veille et animations réutilisables.
- Personnalisation couleurs et vitesse dans limites sûres.

## Pas encore décidé

- Framework iOS/Android.
- Protocole BLE/Wi-Fi/USB.
- Capteurs et télémétrie.

Le contrôle local doit rester utilisable même sans service d'IA distant.
