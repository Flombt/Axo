# Firmware d’atelier AURA-009 r02

Le sketch commande quatre servos de position sur un Nano ATmega328P 5 V. Il utilise Servo et EEPROM. Le bouton D2 lance une séquence après calibration et armement. Les sorties restent désarmées au démarrage. Un bouton déjà maintenu doit d’abord être relâché.

## Affectations

| Axe | Sortie |
|---|---|
| J2 · épaule | D3 |
| J3 · coude | D5 |
| J7 · roulis | D6 |
| T1 · fermeture | D9 |
| Poussoir normalement ouvert | D2 vers GND |

## Vérification du binaire

Arduino CLI 1.6.0 · Arduino AVR Boards 1.8.8 · Servo 1.3.0.

`arduino-cli compile --fqbn arduino:avr:nano:cpu=atmega328 AURA009_Atelier`

`arduino-cli compile --fqbn arduino:avr:nano:cpu=atmega328old AURA009_Atelier`

Compilation réussie pour les deux profils, 6 334 octets de flash et 409 octets de RAM statique. Aucun téléversement ni essai sur robot. Suivre I01, I02 et J01 de la notice pour les premiers essais. Le montage doit avoir sa propre coupure du rail moteurs. STOP coupe les impulsions de commande, le rail conserve sa tension.
