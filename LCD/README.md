# Exercice 3 — Système de contrôle de température

## 🎯 Objectif
Créer un **thermostat multi-états** en MicroPython :
- Réglage de la **température de consigne** avec un potentiomètre (15–35 °C)
- Lecture de la **température ambiante** (DHT20)
- Affichage sur **LCD 16×2** :
  - Ligne 1 : `Set: xx.xC`
  - Ligne 2 : `Ambient: yy.yC`
- Contrôle :
  - Si `Ambient > Set` → LED clignote lentement (0,5 Hz)
  - Si `Ambient > Set + 3` → LED rapide + **buzzer ON** + mot **ALARM** sur le LCD

## ⚙️ Matériel
| Module | Port Grove | Broche Pico | Rôle |
|---|---|---|---|
| Potentiomètre | A0 | GP26/ADC0 | Température de consigne |
| DHT20 | D18 | GP18 | Capteur température |
| LED | D16 | GP16 | Indicateur visuel |
| Buzzer | D20 | GP20 (PWM) | Alarme sonore |
| LCD 16×2 I²C | I2C1 | SDA/SCL | Affichage données |

## ▶️ Utilisation
1. Copier `Exercice3.py`, `lcd1602.py` et `dht20.py` sur le Pico (VS Code → MicroPico → Upload Project to Pico).  
2. Brancher les modules selon le tableau.  
3. Lancer le script → le LCD affiche la consigne et la température.  
4. Tourner le **potentiomètre** pour modifier la consigne.  
5. Chauffer ou refroidir le capteur pour observer les changements d’état.

## 🧠 Détails techniques
- Lecture **non-bloquante** (LED et buzzer fonctionnent pendant les mesures).  
- Mapping ADC → température via règle de trois (15→35 °C).  
- **PWM** du buzzer contrôlé via `duty_u16()` (2000 Hz).  
- LCD rafraîchi toutes les ~1 s.  

## 🧪 Bonus possibles
- Effet **dimmer** : LED s’allume progressivement au lieu de clignoter.  
- **ALARM** clignotant ou défilant sur le LCD.  

## 📁 Fichiers
- `Exercice3.py` — programme principal  
- `lcd1602.py`, `dht20.py` — librairies  
- `photo_montage.png` — schéma ou photo du montage  

## ✅ Résultat attendu
Le LCD affiche la température de consigne et celle mesurée ;  
la LED et le buzzer réagissent automatiquement selon l’écart entre les deux.
