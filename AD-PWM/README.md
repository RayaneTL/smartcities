# Exercice 2 — Volume d’une mélodie (potentiomètre)

## 🎯 Objectif
Créer un programme MicroPython qui joue une **mélodie en boucle**, dont le **volume** est contrôlé en temps réel par un **potentiomètre**. *(Bonus : bouton pour changer de mélodie, LED qui clignote au rythme).*  
> D’après l’énoncé “EXERCICE 2 : VOLUME D’UNE MÉLODIE”. 

## ⚙️ Matériel
- Raspberry Pi Pico / Pico W  
- Grove Shield for Pico (recommandé)  
- Potentiomètre (Grove Rotary)  
- Buzzer **passif** (PWM)  
- *(Bonus)* Bouton poussoir, LED + résistance (si hors Grove)

## 🔌 Câblage (Grove)
| Élément | Port | Broche Pico |
|---|---|---|
| Potentiomètre | **A0** | GP26/ADC0 |
| Buzzer passif | **D20** | GP20 (PWM) |
| Bouton (bonus) | **D16** | GP16 |
| LED (bonus) | **D18** | GP18 |

## ▶️ Utilisation
1. Envoyer `Exercice2.py` sur le Pico .  
2. Le programme joue la mélodie en boucle.  
3. Tourner le **potentiomètre** → le **volume** change **instantanément**.  
4. *(Bonus)* Appuyer sur le **bouton (D16)** pour changer de mélodie.  
5. *(Bonus)* La **LED (D18)** clignote sur le tempo.
